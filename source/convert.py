def sum(ls: list) -> float:
    """sum of all numbers in list"""
    total: float = 0
    for num in ls:
        if type(num) is float or type(num) is int:
            total += num
    return total


def convert(coordinates: list) -> float:
    coordinates[0], coordinates[1], coordinates[2] = (
        float(coordinates[0]),
        float(coordinates[1]) / 60,
        float(coordinates[2]) / 3600,
    )
    return sum(coordinates) if coordinates[3] == "N" else -sum(coordinates)


def dms2wgs(dms: list) -> tuple:
    return convert(dms[0]), convert(dms[1])


if __name__ == "__main__":
    print(dms2wgs([[47, 13, 18.57, "N"], [1, 34, 48.61, "W"]]))
