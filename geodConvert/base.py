import math
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class GeodeticConversionParameters:
    second_eccentricity_squared: float
    radius_of_curvature_in_prime_vertical: float
    T: float
    C: float
    A: float
    meridian_length: float


class ConversionBase(ABC):
    ELLIPSOID = "WGS 84"
    SEMI_MAJOR_AXIS = 6378137.0
    SEMI_MINOR_AXIS = 6356752.3142
    INVERSE_FLATTENING = 298.257223563

    @property
    def first_eccentricity_squared(self):
        """
        Calculate the first eccentricity squared using the following formula:
        e^2 = (a^2 - b^2) / a^2
        :return: float
        """
        flattening = 1 / self.INVERSE_FLATTENING
        return (2 * flattening) - flattening ** 2
    @property
    def second_eccentricity_squared(self):
        """
        Calculate the second eccentricity squared using the following formula:
        e'^2 = (a^2 - b^2) / b^2
        :return: float
        """
        sec_e = self.first_eccentricity_squared/(1-self.first_eccentricity_squared)
        return sec_e

    @abstractmethod
    def convert(self, *args, **kwargs):
        return "test"

    @abstractmethod
    def reverse(self, *args, **kwargs):
        return "test"
