HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CLEAR_LINE = "\033[2K\r"


def fg(r: int, g: int, b: int) -> str:
    return f"\033[38;2;{r};{g};{b}m"


def up(n: int) -> str:
    return f"\033[{n}A"


C_KETTLE = fg(160, 90, 40)
C_SHINE = fg(210, 140, 70)
C_WATER_C = fg(90, 160, 220)
C_WATER_W = fg(100, 200, 200)
C_WATER_H = fg(220, 140, 60)
C_WATER_B = fg(240, 80, 40)
C_STEAM = fg(190, 200, 215)
C_STEAM_H = fg(230, 170, 120)
C_HANDLE = fg(120, 60, 20)
C_BASE = fg(140, 75, 30)
C_TEXT = fg(220, 205, 185)
C_DIM = fg(110, 100, 90)
C_GREEN = fg(90, 200, 120)
C_RED = fg(220, 80, 80)
C_GOLD = fg(255, 210, 60)
