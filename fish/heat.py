def heat_at(t: float, total: float) -> float:
    if total <= 0:
        return 0.0
    x = min(t / total, 1.0)
    raw = x * x * (3 - 2 * x)
    return min(raw * 0.95, 0.95)
