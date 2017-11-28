import math


def area(r: int, h: int) -> int:
    A = 2 * math.pi * r * (h + r)
    return A


def volumen(r: int, h: int) -> int:
    V = (math.pi * r**2) * h
    return V