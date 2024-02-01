import numpy as np
from scipy.integrate import quad

eccentricity = np.sqrt(0.0066943799901413165)


def integrand(phi):
    e = eccentricity
    return 1 / np.sqrt(1 - (e ** 2) * (np.sin(phi) ** 2))


def meridian_distance(phi, a):
    integral, _ = quad(integrand, 0, phi)
    return a * integral


# Example usage:
semi_major_axis = 6378137.0  # WGS84 semi-major axis in meters
# WGS84 eccentricity

latitude = np.radians(43.0)  # Example latitude in radians

if __name__ == '__main__':
    result = meridian_distance(latitude, semi_major_axis)
    print("Meridian Distance:", result)
