from src.geolib import compute_destination_point
# from geolib import compute_destination_point
import numpy as np
import pyproj
import math


class Converter:
    """
    Converts local XYZ coordinates to global Lat/Lon/Height coordinates.
    """

    def __init__(self, lat, lon, lat2, lon2):
        self.lat = lat
        self.lon = lon
        self.lat2 = lat2
        self.lon2 = lon2
        self.az = self.get_bearing()

    def get_bearing(self):
        geodesic = pyproj.Geod(ellps="WGS84")
        fwd_azimuth, back_azimuth, distance = geodesic.inv(
            self.lon, self.lat, self.lon2, self.lat2
        )
        return fwd_azimuth

    def get_final_coords(self, x, y) -> list[float]:
        """Returns [lat, lon]"""
        d = math.sqrt(x * x + y * y)
        final_bearing = self.az
        cos_alpha = x / d
        alpha = np.rad2deg(np.arccos(cos_alpha))
        final_bearing += 90 - alpha
        return compute_destination_point(self.lat, self.lon, d, final_bearing)
