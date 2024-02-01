import math


def dms_to_dd(dms: str):
    """Converts a string in the format of degrees, minutes, seconds to a float in decimal degrees. \n
    The format of the string should be: "degrees-minutes-seconds". \n

    Args:
        dms (str): A string in the format of degrees, minutes, seconds.

    Returns:
        float: A float in decimal degrees.
    """

    dms = dms.split("-")
    d = float(dms[0])
    m = float(dms[1])
    s = float(dms[2])

    dd = d + m / 60 + s / 3600

    return dd


def degrees_to_radians(degrees: float):
    """Converts degrees to radians.

    Args:
        degrees (float): A float in degrees.

    Returns:
        float: A float in radians.
    """

    return degrees * math.pi / 180


def radians_to_degrees(radians: float):
    """Converts radians to degrees.

    Args:
        radians (float): A float in radians.

    Returns:
        float: A float in degrees.
    """

    return radians * 180 / math.pi



