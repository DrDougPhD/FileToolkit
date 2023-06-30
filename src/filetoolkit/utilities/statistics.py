def moving_average(avg: float, n: int, value: float) -> float:
    return (value + n * avg) / (n + 1)
