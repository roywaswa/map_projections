import math


def compute_radius_of_curvature_in_the_prime_vertical(semi_major_axis, first_eccentricity_squared, latitude_rad):
    """
    Calculate the radius of curvature of the prime vertical using the following formula:
    N = a / sqrt(1 - e^2 * sin^2(lat))
    :param semi_major_axis: float
    :param first_eccentricity_squared: float
    :param latitude_rad: float
    :return: float
    """
    denominator = math.sqrt(1 - first_eccentricity_squared * (math.sin(latitude_rad) ** 2))
    return semi_major_axis / denominator


def compute_meridian_distance(semi_major_axis, first_eccentricity_squared, latitude_rad):
    """
    Calculate the meridian distance using the following formula:
    M = a * ((1 - e^2 / 4 - 3 * e^4 / 64 - 5 * e^6 / 256) * lat - (3 * e^2 / 8 + 3 * e^4 / 32 + 45 * e^6 / 1024) *
    sin(2 * lat) + (15 * e^4 / 256 + 45 * e^6 / 1024) * sin(4 * lat) - (35 * e^6 / 3072) * sin(6 * lat))
    :param semi_major_axis: float
    :param first_eccentricity_squared: float
    :param latitude_rad: float
    :return: float
    """
    return semi_major_axis * (
            (1 - first_eccentricity_squared / 4 - 3 * (first_eccentricity_squared ** 2) / 64 - 5 * (
                    first_eccentricity_squared ** 3) / 256) * latitude_rad -
            (3 * first_eccentricity_squared / 8 + 3 * (
                    first_eccentricity_squared ** 2) / 32 + 45 * (
                     first_eccentricity_squared ** 3) / 1024) * math.sin(2 * latitude_rad) +
            (15 * (first_eccentricity_squared ** 2) / 256 + 45 * (
                    first_eccentricity_squared ** 3) / 1024) * math.sin(4 * latitude_rad) -
            (35 * (first_eccentricity_squared ** 3) / 3072) * math.sin(6 * latitude_rad))


def compute_foot_point_latitude(
        semi_major_axis, first_eccentricity_squared, second_eccentricity_squared,
        northing,
        **kwargs
):
    scale_factor = kwargs["scale_factor"] if kwargs["scale_factor"] else 0.9996
    e_1 = (1 - math.sqrt(1 - first_eccentricity_squared)) / (
            1 + math.sqrt(1 - first_eccentricity_squared))

    m = compute_meridian_distance(
        semi_major_axis,
        first_eccentricity_squared,
        math.radians(0)
    ) + northing / scale_factor

    u = m / (semi_major_axis * (
            1 - (second_eccentricity_squared / 4) -
            (3 * (second_eccentricity_squared ** 2) / 64) -
            (5 * (second_eccentricity_squared ** 3) / 256)
    ))
    print({
        'u': u,
        'm': m,
        'e_1': e_1
    })
    foot_lat = (u +
                (3 * e_1 / 2 - 27 * (e_1 ** 3) / 32) * math.sin(2 * u) +
                (21 * (e_1 ** 3) / 16 - 55 * (e_1 ** 4) / 32) * math.sin(4 * u) +
                (151 * (e_1 ** 3) / 96) * math.sin(6 * u) +
                (1097 * (e_1 ** 4) / 512) * math.sin(8 * u)
                )
    return foot_lat
