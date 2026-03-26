import os
import shutil
import subprocess
import sys
import time


def _terminal_bell(times: int = 1, gap_s: float = 0.05) -> None:
    for i in range(max(0, times)):
        sys.stdout.write("")
        sys.stdout.flush()
        if i + 1 < times:
            time.sleep(max(0.0, gap_s))


def play_done_sound(*, enabled: bool = True) -> None:
    if not enabled:
        return

    afplay = shutil.which("afplay")
    mac_sound = "/System/Library/Sounds/Glass.aiff"
    if afplay and os.path.isfile(mac_sound):
        subprocess.run(
            [afplay, mac_sound],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        return

    paplay = shutil.which("paplay")
    linux_sound = "/usr/share/sounds/freedesktop/stereo/complete.oga"
    if paplay and os.path.isfile(linux_sound):
        subprocess.run(
            [paplay, linux_sound],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        return

    _terminal_bell(times=2, gap_s=0.06)
