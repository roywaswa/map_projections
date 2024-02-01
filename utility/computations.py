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




