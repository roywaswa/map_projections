import math

from geodConvert.base import ConversionBase
from utility.computations import compute_meridian_distance
from utility import computations


class UTMToGeodetic(ConversionBase):

    def __init__(self, easting, northing, zone):
        super().__init__()
        self.easting = easting
        self.northing = northing
        self.zone = zone
        self.hemisphere = self.zone[-1]
        self.central_meridian = int(zone[:-1]) * 6 - 183
        self.central_meridian_rad = math.radians(self.central_meridian)

    @property
    def meridian_length(self):
        meridian_at_center = compute_meridian_distance(
            self.SEMI_MAJOR_AXIS,
            self.first_eccentricity_squared,
            self.central_meridian_rad)
        return meridian_at_center + (self.northing / self.SCALE_FACTOR)

    @property
    def foot_point_latitude(self):
        return computations.compute_foot_point_latitude(
            semi_major_axis=self.SEMI_MAJOR_AXIS,
            northing=self.northing, second_eccentricity_squared=self.second_eccentricity_squared,
            first_eccentricity_squared=self.first_eccentricity_squared,
            scale_factor=self.SCALE_FACTOR
        )

    def _get_latitude(self, params):
        lat_1 = params["lat_1"]
        e_2 = params["e_2"]
        c_1 = params["c_1"]
        t_1 = params["t_1"]
        n_1 = params["n_1"]
        d = params["d"]

        r_1 = self.SEMI_MAJOR_AXIS * (1 - self.first_eccentricity_squared) / (
                (1 - self.first_eccentricity_squared * (math.sin(self.foot_point_latitude) ** 2)
                 ) ** 1.5)
        latitude = (
                lat_1 - (n_1 * math.tan(lat_1) / r_1) * (
                (d ** 2) / 2 - (5 + 3 * t_1 + 10 * c_1 - 4 * (c_1 ** 2) - 9 * (e_2 ** 2)) * (d ** 4) / 24 +
                (61 + 90 * t_1 + 298 * c_1 + 45 * (t_1 ** 2) - 252 * (e_2 ** 2) - 3 * (c_1 ** 2))
        ))
        return latitude

    def _get_longitude(self, params):
        lon_0 = self.central_meridian_rad
        lat_1 = params["lat_1"]
        e_2 = params["e_2"]
        c_1 = params["c_1"]
        t_1 = params["t_1"]
        d = params["d"]
        longitude = lon_0 + (
                d - (1 + 2 * t_1 + c_1) * (d ** 3) / 6 +
                (5 - 2 * c_1 + 28 * t_1 - 3 * c_1 + 8 * e_2 + 24 * (t_1 ** 2) * (d ** 5) / 120)
        ) / math.cos(lat_1)
        return longitude

    def convert(self):
        easting = self.easting
        northing = self.northing
        zone = int(self.zone[:-1])
        if self.hemisphere == "S":
            northing = 10000000 - northing

        a = self.SEMI_MAJOR_AXIS
        e = math.sqrt(self.first_eccentricity_squared)
        e1sq = self.first_eccentricity_squared
        k0 = self.SCALE_FACTOR

        arc = northing / k0
        mu = arc / (a * (1 - math.pow(e, 2) / 4.0 - 3 * math.pow(e, 4) / 64.0 - 5 * math.pow(e, 6) / 256.0))

        ei = (1 - math.pow((1 - e * e), (1 / 2.0))) / (1 + math.pow((1 - e * e), (1 / 2.0)))

        ca = 3 * ei / 2 - 27 * math.pow(ei, 3) / 32.0
        cb = 21 * math.pow(ei, 2) / 16 - 55 * math.pow(ei, 4) / 32
        cc = 151 * math.pow(ei, 3) / 96
        cd = 1097 * math.pow(ei, 4) / 512
        phi1 = mu + ca * math.sin(2 * mu) + cb * math.sin(4 * mu) + cc * math.sin(6 * mu) + cd * math.sin(8 * mu)

        n0 = a / math.pow((1 - math.pow((e * math.sin(phi1)), 2)), (1 / 2.0))
        r0 = a * (1 - e * e) / math.pow((1 - math.pow((e * math.sin(phi1)), 2)), (3 / 2.0))
        fact1 = n0 * math.tan(phi1) / r0

        _a1 = 500000 - easting
        dd0 = _a1 / (n0 * k0)
        fact2 = dd0 * dd0 / 2

        t0 = math.pow(math.tan(phi1), 2)
        Q0 = e1sq * math.pow(math.cos(phi1), 2)
        fact3 = (5 + 3 * t0 + 10 * Q0 - 4 * Q0 * Q0 - 9 * e1sq) * math.pow(dd0, 4) / 24
        fact4 = (61 + 90 * t0 + 298 * Q0 + 45 * t0 * t0 - 252 * e1sq - 3 * Q0 * Q0) * math.pow(dd0, 6) / 720

        lof1 = _a1 / (n0 * k0)
        lof2 = (1 + 2 * t0 + Q0) * math.pow(dd0, 3) / 6.0
        lof3 = (5 - 2 * Q0 + 28 * t0 - 3 * math.pow(Q0, 2) + 8 * e1sq + 24 * math.pow(t0, 2)) * math.pow(dd0, 5) / 120
        _a2 = (lof1 - lof2 + lof3) / math.cos(phi1)
        _a3 = _a2 * 180 / math.pi

        latitude = 180 * (phi1 - fact1 * (fact2 + fact3 + fact4)) / math.pi
        h = self.hemisphere
        if self.hemisphere == "S":
            latitude = -latitude

        longitude = ((zone > 0) and (6 * zone - 183.0) or 3.0) - _a3

        return {
            "latitude": latitude, "longitude": longitude
        }

    def reverse(self):
        pass
