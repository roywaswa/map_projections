import math

import pytest
from utility import computations as comp


class TestComputationModule:

    @pytest.mark.parametrize("lat, expected", [(0, 6378137), (45, 6388838.290121148), (-30, 6383480.9176901085)])
    def test_compute_radius_of_curvature_in_the_prime_vertical(self, lat, expected):
        comp_value = comp.compute_radius_of_curvature_in_the_prime_vertical(
            6378137,
            0.0066943799901413165,
            math.radians(lat)
        )
        assert comp_value == expected

    @pytest.mark.parametrize("lat, expected", [(0, 0), (43, 4762719.884244631), (40, 4429529.03049117)])
    def test_compute_meridian_distance(self, lat, expected):
        comp_value = comp.compute_meridian_distance(
            6378137,
            0.0066943799901413165,
            math.radians(lat)
        )
        assert comp_value == expected





