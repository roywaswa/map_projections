from geodConvert.base import ConversionBase, GeodeticConversionParameters
import math
from utility.conversion import degrees_to_radians
from utility import computations as comp


class GeodeticToUTM(ConversionBase):
    def __init__(self, latitude, longitude):
        """
        GeodeticToUTM constructor \n

        The class takes two parameters: latitude and longitude, both of which have to be in decimal degrees. \n

        :type latitude: Float :type longitude:
        :param latitude:
        :param longitude:
        """
        super().__init__()
        self.latitude = latitude
        self.longitude = longitude
        self.central_meridian = 6 * math.floor(self.longitude / 6) + 3
        self.meridian_origin = self.central_meridian - 3
        self.meridian_origin_rad = degrees_to_radians(self.meridian_origin)
        self.longitude_rad = degrees_to_radians(self.longitude)
        self.latitude_rad = degrees_to_radians(self.latitude)
        self.meridian_distance = comp.compute_meridian_distance(
            semi_major_axis=self.SEMI_MAJOR_AXIS,
            first_eccentricity_squared=self.first_eccentricity_squared,
            latitude_rad=self.latitude_rad
        )
        self.radius_of_curvature_in_prime_vertical = comp.compute_radius_of_curvature_in_the_prime_vertical(
            semi_major_axis=self.SEMI_MAJOR_AXIS,
            first_eccentricity_squared=self.first_eccentricity_squared,
            latitude_rad=self.latitude_rad
        )
        self.central_meridian_rad = degrees_to_radians(self.central_meridian)

    @property
    def zone(self):
        """
        Calculate the zone using the following formula:
        zone = floor((lon + 180) / 6) + 1
        :return: int
        """
        utm_zone = math.floor((self.longitude + 180) / 6) + 1
        if self.latitude < 0:
            return f"{utm_zone}S"
        else:
            return f"{utm_zone}N"

    @staticmethod
    def _get_easting(ecp: dict):
        """
        Calculate easting using the following formula:
        E = E0 + k0 * N * (A + (1 - T + C) * A^3 / 6 + (5- 18 * T + T^2 + 72 * C - 58 * e^2) * A^5 / 120)
        :return: float
        """
        first_approx = ecp["A"] + (1 - ecp["T"] + ecp["C"]) * (ecp["A"] ** 3) / 6
        second_approx = (5 - 18 * ecp["T"] + (ecp["T"] ** 2) + 72 * ecp["C"] - 58 * ecp["e2"]) * (ecp["A"] ** 5) / 120
        easting = (ecp["k0"] * ecp["N"] * (first_approx + second_approx))
        return easting

    @staticmethod
    def _get_northing(ncp: dict):
        """
        Calculate northings using the following formula: N = N0 + k0 * (M - M0 + N * tan(lat) * (A^2 / 2 + (5 - T + 9
        * C + 4 * C^2) * A^4 / 24 + (61 - 58 * T + T^2 + 600 * C - 330 * e^2) * A^6 / 720)) :param ncp: :return:
        """
        northing = (ncp["N0"] + ncp["k0"] * (ncp["M"] - ncp["M0"] + ncp["N"] * math.tan(ncp["lat"]) * (
                (ncp["A"] ** 2) / 2 + (5 - ncp["T"] + 9 * ncp["C"] + 4 * (ncp["C"] ** 2)) * (ncp["A"] ** 4) / 24 +
                (61 - 58 * ncp["T"] + (ncp["T"] ** 2) + 600 * ncp["C"] - 330 * ncp["e2"]) * (ncp["A"] ** 6) / 720)))
        return northing

    def _get_conversion_parameters(self) -> GeodeticConversionParameters:
        return GeodeticConversionParameters(
            second_eccentricity_squared=self.second_eccentricity_squared,
            radius_of_curvature_in_prime_vertical=self.radius_of_curvature_in_prime_vertical,
            T=self._get_T(),
            C=self._get_C(),
            A=self._get_A(),
            meridian_length=self.meridian_distance,
        )

    def _get_A(self):
        """
        Calculate A using the following formula:
        A = (lon - lon0) * cos(lat)
        :return: float
        """
        return (self.longitude_rad - self.meridian_origin_rad) * math.cos(self.latitude_rad)

    def _get_T(self, ):
        """
        Calculate T using the following formula:
        T = tan(lat)^2
        :return: float
        """
        return math.tan(self.latitude_rad) ** 2

    def _get_C(self):
        """
        Calculate C using the following formula:
        C = e'^2 * cos(lat)^2
        :return: float
        """
        return self.second_eccentricity_squared * (math.cos(self.latitude_rad) ** 2)

    def convert(self):
        parameters = {
            "E0": 500000,
            "N0": 0 if self.latitude > 0 else 10000000,
            "k0": 0.9996,
            "M0": comp.compute_meridian_distance(
                semi_major_axis=self.SEMI_MAJOR_AXIS,
                first_eccentricity_squared=self.first_eccentricity_squared,
                latitude_rad=0
            ),
            "lat": self.latitude_rad,
            "M": self.meridian_distance,
            "A": self._get_A(),
            "T": self._get_T(),
            "C": self._get_C(),
            "N": self.radius_of_curvature_in_prime_vertical,
            "e2": self.second_eccentricity_squared
        }
        print(parameters)
        easting = self._get_easting(parameters)
        northing = self._get_northing(parameters)
        return {
            "easting": easting,
            "northing": northing,
            "zone": self.zone
        }

    def reverse(self):
        return "test"
