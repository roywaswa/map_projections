import math
from utility import computations as comp

import pytest


class TestBaseClass:

    @pytest.fixture(params=[
        (2, 37), (-2, 37), (-2, -37), (2, -37)
    ], ids=["1st quadrant", "2nd quadrant", "3rd quadrant", "4th quadrant"])
    def convert(self, request):
        from geodConvert.geodetic_to_utm import GeodeticToUTM
        print(f"request.param: {request.param[0]}, {request.param[1]}")
        return GeodeticToUTM(request.param[0], request.param[1])

    def test_convert(self, convert):
        assert convert.convert() == "test"

    def test_reverse(self, convert):
        assert convert.reverse() == "test"

    def test_central_meridian(self, convert):
        central_meridian = convert.central_meridian
        assert central_meridian == (
                6 * math.floor(convert.longitude / 6) + 3)

    def test_zone(self, convert):
        expected_zone = f"{math.floor((convert.longitude + 180) / 6) + 1}"
        expected_hemisphere = "N" if convert.latitude > 0 else "S"
        zone = convert.zone
        assert zone == f"{expected_zone}{expected_hemisphere}"

    def test_first_eccentricity_squared(self, convert):
        first_eccentricity_squared = convert.first_eccentricity_squared
        assert first_eccentricity_squared == ((convert.SEMI_MAJOR_AXIS ** 2 - convert.SEMI_MINOR_AXIS ** 2) /
                                              convert.SEMI_MAJOR_AXIS ** 2)

    def test_second_eccentricity_squared(self, convert):
        second_eccentricity_squared = convert.second_eccentricity_squared
        assert (second_eccentricity_squared == (convert.SEMI_MAJOR_AXIS ** 2 - convert.SEMI_MINOR_AXIS ** 2) /
                convert.SEMI_MINOR_AXIS ** 2)

    def test_longitude_rad(self, convert):
        longitude_rad = convert.longitude_rad
        assert longitude_rad == math.radians(convert.longitude)

    def test_latitude_rad(self, convert):
        latitude_rad = convert.latitude_rad
        assert latitude_rad == math.radians(convert.latitude)

    def test_radius_of_curvature_in_prime_vertical(self, convert):
        class_value = convert.radius_of_curvature_in_prime_vertical
        expected_value = comp.compute_radius_of_curvature_in_the_prime_vertical(
            semi_major_axis=convert.SEMI_MAJOR_AXIS,
            first_eccentricity_squared=convert.first_eccentricity_squared,
            latitude_rad=convert.latitude_rad
        )
        assert class_value == expected_value

    def test_meridian_distance(self, convert):
        class_value = convert.meridian_distance
        expected_value = comp.compute_meridian_distance(
            semi_major_axis=convert.SEMI_MAJOR_AXIS,
            first_eccentricity_squared=convert.first_eccentricity_squared,
            latitude_rad=convert.latitude_rad
        )
        assert class_value == expected_value

    def test_get_A(self, convert):
        class_value = convert._get_A()
        expected_value = (convert.longitude - convert.central_meridian) * math.cos(convert.latitude_rad)
        assert class_value == expected_value

    def test_get_T(self, convert):
        class_value = convert._get_T()
        expected_value = math.tan(convert.latitude_rad) ** 2
        assert class_value == expected_value

    def test_get_C(self, convert):
        class_value = convert._get_C()
        expected_value = convert.second_eccentricity_squared * (math.cos(convert.latitude_rad) ** 2)
        assert class_value == expected_value



