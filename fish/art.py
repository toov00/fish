from fish.ansi import C_GOLD, C_RED, C_WATER_B, C_WATER_C, C_WATER_H, C_WATER_W, RESET

FRAME_HEIGHT = 6

# Same width (9) for stable redraws; wiggle swaps eye vs tail apostrophe.
_FISH_RIGHT = "><(((((°>"
_FISH_RIGHT2 = "><((((('>"
_FISH_LEFT = "<°)))))><"
_FISH_LEFT2 = "<')))))><"

_SWIM_CYCLE = 20
_MAX_X = 8
_FISH_GUTTER = "    "


def water_col(heat: float) -> str:
    if heat < 0.25:
        return C_WATER_C
    if heat < 0.55:
        return C_WATER_W
    if heat < 0.80:
        return C_WATER_H
    return C_WATER_B


def _swim(tick: int) -> tuple[bool, int]:
    t = tick % _SWIM_CYCLE
    half = _SWIM_CYCLE // 2
    denom = max(1, half - 1)
    if t < half:
        facing_right = True
        x = min(_MAX_X, (t * _MAX_X) // denom)
    else:
        facing_right = False
        u = t - half
        x = max(0, ((half - 1 - u) * _MAX_X) // denom)
    return facing_right, x


def _pick_fish(tick: int, facing_right: bool) -> str:
    alt = (tick % 2) == 1
    if facing_right:
        return _FISH_RIGHT2 if alt else _FISH_RIGHT
    return _FISH_LEFT2 if alt else _FISH_LEFT


def _bubble_row(g: str, tick: int, *, upper: bool) -> str:
    phase = (tick + (0 if upper else 2)) % 3
    a = f"{g}·{RESET}"
    b = f"{g}o{RESET}"
    c = f"{g}·{RESET}"
    d = f"{g}.{RESET}"
    if phase == 0:
        return f"  {a}    {b}     {c}    {d}"
    if phase == 1:
        return f"    {b}     {a}    {d}     {c}"
    return f"  {c}     {d}    {a}     {b}"


def build_frame(heat: float, tick: int) -> list[str]:
    wc = water_col(heat)
    g = C_GOLD
    facing_right, x = _swim(tick)
    lead = " " * x
    fish = _pick_fish(tick, facing_right)
    swim = f" {_FISH_GUTTER}{lead}{wc}{fish}{RESET}"

    return [
        _bubble_row(g, tick, upper=True),
        "  ",
        swim,
        "  ",
        _bubble_row(g, tick + 2, upper=False),
        "  ",
    ]


def whistle_frame(tick: int, exit_code: int = 0) -> list[str]:
    wc = water_col(1.0)
    g = C_GOLD
    facing_right, x = _swim(tick)
    lead = " " * x
    fish = _pick_fish(tick, facing_right)
    swim = f" {_FISH_GUTTER}{lead}{wc}{fish}{RESET}"
    accent = g if exit_code == 0 else C_RED
    tail = (
        f"{g}*{RESET} {g}*{RESET}"
        if exit_code == 0
        else f"{C_RED}x{RESET} {C_RED}x{RESET}"
    )
    top = f"  {accent}{tail}{RESET}"

    return [
        top,
        _bubble_row(g, tick + 1, upper=True),
        swim,
        "  ",
        f"    {g}o{RESET}     {g}·{RESET}     {g}o{RESET}",
        "  ",
    ]
