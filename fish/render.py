import sys
from typing import Optional

from fish.ansi import CLEAR_LINE, C_TEXT, RESET, up
from fish.art import FRAME_HEIGHT, build_frame, water_col, whistle_frame

TOTAL_LINES = FRAME_HEIGHT + 1


def progress_bar(heat: float, width: int = 28) -> str:
    filled = int(heat * width)
    bar = "█" * filled + "░" * (width - filled)
    pct = int(heat * 100)
    wc = water_col(heat)
    return f"  {wc}{bar}{RESET} {C_TEXT}{pct:3d}%{RESET}"


def render(
    heat: float,
    tick: int,
    *,
    done: bool = False,
    exit_code: Optional[int] = None,
) -> None:
    if done and tick > 0:
        code = 0 if exit_code is None else exit_code
        frame_lines = whistle_frame(tick, exit_code=code)
    else:
        frame_lines = build_frame(heat, tick)

    out: list[str] = []

    if tick > 0:
        out.append(up(TOTAL_LINES))

    for line in frame_lines:
        out.append(CLEAR_LINE + line)

    if not done:
        out.append(CLEAR_LINE + progress_bar(heat))
    else:
        out.append(CLEAR_LINE)

    sys.stdout.write("\n".join(out))
    try:
        sys.stdout.flush()
    except BrokenPipeError:
        return
