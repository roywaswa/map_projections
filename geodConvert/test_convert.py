import math

from geodConvert.utm_to_geodetic import UTMToGeodetic
from utility import computations as comp

import pytest


class TestGeodeticToUTM:

    @pytest.fixture(params=[
        (2, 37), (-2, 37), (-2, -37), (2, -37)
    ], ids=["1st quadrant", "2nd quadrant", "3rd quadrant", "4th quadrant"])
    def convert(self, request):
        from geodConvert.geodetic_to_utm import GeodeticToUTM
        print(f"request.param: {request.param[0]}, {request.param[1]}")
        return GeodeticToUTM(request.param[0], request.param[1])

    @pytest.mark.skip
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
        flattening = 1 / convert.INVERSE_FLATTENING
        assert first_eccentricity_squared == (2 * flattening) - flattening ** 2

    def test_second_eccentricity_squared(self, convert):
        second_eccentricity_squared = convert.second_eccentricity_squared
        flattening = 1 / convert.INVERSE_FLATTENING
        first_eccentricity_squared = (2 * flattening) - flattening ** 2
        expected_second_eccentricity_squared = first_eccentricity_squared / (1 - first_eccentricity_squared)
        assert (second_eccentricity_squared == expected_second_eccentricity_squared)

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
        expected_value = ((convert.longitude_rad - math.radians(convert.central_meridian)) *
                          math.cos(convert.latitude_rad))
        assert class_value == expected_value

    def test_get_T(self, convert):
        class_value = convert._get_T()
        expected_value = math.tan(convert.latitude_rad) ** 2
        assert class_value == expected_value

    def test_get_C(self, convert):
        class_value = convert._get_C()
        expected_value = convert.second_eccentricity_squared * (math.cos(convert.latitude_rad) ** 2)
        assert class_value == expected_value


class TestUTMToGeodetic:

    @pytest.fixture(params=[
        (308069.42, 5451364.52, '42N'),
        (756735.50, 9287970.13, '36S'),
        (291251.26, 4014160.33, '15N'),
        (455315.51, 6711880.57, '19S')
    ], ids=["Q1", "Q2", "Q3", "Q4"])
    def convert(self, request):
        from geodConvert.utm_to_geodetic import UTMToGeodetic
        print(f"request.param: {request.param[0]}, {request.param[1]}")
        return UTMToGeodetic(request.param[0], request.param[1], request.param[2])

    @pytest.mark.parametrize("easting, northing, zone, expected", [
        (308069.42, 5451364.52, '42N', {'latitude': 49.1850261, 'longitude': 66.3660333}),
        (756735.50, 9287970.13, '36S', {'latitude': -6.43641, 'longitude': 35.321131}),
        (291251.26, 4014160.33, '15N', {'latitude': 36.249813, 'longitude': -95.323303}),
        (455315.51, 6711880.57, '19S', {'latitude': -29.72244, 'longitude': -69.46202}),
    ], ids=["Q1", "Q2", "Q3", "Q4"])
    def test_convert(self, expected, easting, northing, zone):
        utm_geo = UTMToGeodetic(easting, northing, zone)
        computed = utm_geo.convert()
        assert math.isclose(computed['latitude'], expected['latitude'], abs_tol=0.0001)
        assert math.isclose(computed['longitude'], expected['longitude'], abs_tol=0.0001)

    def test_foot_point_latitude(self, convert):
        expected = comp.compute_foot_point_latitude(
            semi_major_axis=convert.SEMI_MAJOR_AXIS,
            northing=convert.northing, second_eccentricity_squared=convert.second_eccentricity_squared,
            first_eccentricity_squared=convert.first_eccentricity_squared,
            scale_factor=convert.SCALE_FACTOR
        )
        assert convert.foot_point_latitude == expected
