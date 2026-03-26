import subprocess
import threading
import time

from fish.ansi import C_DIM, HIDE_CURSOR, RESET, SHOW_CURSOR
from fish.render import render
from fish.sound import play_done_sound

_FRAME_SLEEP_RUNNING = 0.15
_FRAME_SLEEP_DONE = 0.14
_DONE_FRAMES = 14
_NO_ESTIMATE_ASYMPTOTE_S = 8.0
_NO_ESTIMATE_HEAT_CAP = 0.85


def run_with_kettle(
    cmd: list[str],
    *,
    sound: bool = True,
) -> int:
    print(HIDE_CURSOR, flush=True)

    start = time.time()
    tick = 0
    proc_result: dict[str, int] = {}

    def run_proc() -> None:
        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
            proc_result["code"] = result.returncode
        except FileNotFoundError:
            proc_result["code"] = 127
        except Exception:
            proc_result["code"] = 1

    thread = threading.Thread(target=run_proc, daemon=True)
    thread.start()

    try:
        while thread.is_alive():
            elapsed = time.time() - start
            heat = min(
                _NO_ESTIMATE_HEAT_CAP,
                1.0 - 1.0 / (1.0 + elapsed / _NO_ESTIMATE_ASYMPTOTE_S),
            )

            render(heat, tick, done=False)
            tick += 1
            time.sleep(_FRAME_SLEEP_RUNNING)

        thread.join()
        exit_code = proc_result.get("code", 0)

        play_done_sound(enabled=sound)

        for i in range(_DONE_FRAMES):
            render(1.0, i + 1, done=True, exit_code=exit_code)
            time.sleep(_FRAME_SLEEP_DONE)

    except KeyboardInterrupt:
        elapsed = time.time() - start
        heat = min(
            _NO_ESTIMATE_HEAT_CAP,
            1.0 - 1.0 / (1.0 + elapsed / _NO_ESTIMATE_ASYMPTOTE_S),
        )
        render(heat, tick, done=True, exit_code=130)
        print(f"\n\n  {C_DIM}interrupted{RESET}")
        return 130
    finally:
        try:
            print(SHOW_CURSOR, end="", flush=True)
        except BrokenPipeError:
            pass

    print()
    return exit_code


def boil_timer(
    seconds: float,
    *,
    sound: bool = True,
) -> int:
    print(HIDE_CURSOR, flush=True)

    start = time.time()
    tick = 0

    try:
        while True:
            elapsed = time.time() - start
            if elapsed >= seconds:
                break
            heat = min(elapsed / seconds, 1.0) if seconds > 0 else 0.0
            render(heat, tick, done=False)
            tick += 1
            time.sleep(_FRAME_SLEEP_RUNNING)

        for i in range(_DONE_FRAMES):
            render(1.0, i + 1, done=True, exit_code=0)
            time.sleep(_FRAME_SLEEP_DONE)

        play_done_sound(enabled=sound)

    except KeyboardInterrupt:
        elapsed = time.time() - start
        heat = min(elapsed / seconds, 1.0) if seconds > 0 else 0.0
        render(heat, tick, done=True, exit_code=130)
        print(f"\n\n  {C_DIM}interrupted{RESET}")
        return 130
    finally:
        print(SHOW_CURSOR, end="", flush=True)

    print()
    return 0
