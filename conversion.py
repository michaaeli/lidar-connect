import math
import numpy as np
import pyproj
from local_coords_to_global import xy2latlon, compute_destination_point

class getLLH():
    def __init__(self, lat, lon, lat2, lon2, x, y):
        self.lat = lat
        self.lon = lon
        self.lat2 = lat2
        self.lon2 = lon2
        self.x = x
        self.y = y
        
    def get_bearing(self):
        geodesic = pyproj.Geod(ellps='WGS84')
        fwd_azimuth,back_azimuth,distance = geodesic.inv(self.lon, self.lat, self.lon2, self.lat2)
        return fwd_azimuth 
    
    def experimental2(self):
        az = self.get_bearing()
        d = math.sqrt(self.x*self.x + self.y*self.y)
        final_bearing = az
        cos_alpha = self.x/d
        alpha = np.rad2deg(np.arccos(cos_alpha))
        final_bearing += 90 - alpha

        return compute_destination_point(self.lat, self.lon, d, final_bearing)



