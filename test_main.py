import pytest
from main import start_conversion


class TestMainFunction:

    @pytest.mark.parametrize("lat, lon, expected", [
        (49.1850261, 66.3660333, {'easting': round(308069.42, 1), 'northing': round(5451364.52, 1), 'zone': '42N'}),
        (-6.43641, 35.321131, {'easting': round(756735.50, 1), 'northing': round(9287970.13, 1), 'zone': '36S'}),
        (36.249813, -95.323303, {'easting': round(291251.26, 1), 'northing': round(4014160.33, 1), 'zone': '15N'}),
        (-29.72244,-69.46202, {'easting': round(455315.51, 1), 'northing': round(6711880.57,1), 'zone': '19S'}),
        ], ids=["Q1", "Q2", "Q3", "Q4"])
    def test_main(self, lat, lon, expected):
        assert start_conversion(lat, lon) == expected
