def CompareTwoRange(x1: int, x2: int, y1: int, y2: int) -> bool:
    if (x1 >= y1 and x1 < y2) or (y1 >= x1 and y1 < x2):
        return True
    return False