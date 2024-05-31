import math
import numpy as np
import pyproj

class getLLH():
    def __init__(self, lat, lon, h):
        self.lat = lat
        self.lon = lon
        self.h = h
        
    def get_bearing(lat1, lon1, lat2, lon2):
        geodesic = pyproj.Geod(ellps='WGS84')
        fwd_azimuth,back_azimuth,distance = geodesic.inv(lon1, lat1, lon2, lat2)
        return back_azimuth 
    

       