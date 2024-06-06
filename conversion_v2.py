import math
import numpy as np
import pyproj

class getLLH():
    def __init__(self, lat, lon, lat2, lon2, x, y):
        self.lat = lat
        self.lon = lon
        self.lat2 = lat2
        self.lon2 = lon2
        self.x = x
        self.y = y

    def get_distance(self):
        distance = math.sqrt(self.x ** 2 + self.y ** 2)
        print("distance: ", distance)
        return distance
        
    def get_bearing(self):
        geodesic = pyproj.Geod(ellps='WGS84')
        fwd_azimuth,back_azimuth,distance = geodesic.inv(self.lon, self.lat, self.lon2, self.lat2)
        print("bearing: ", back_azimuth)
        return fwd_azimuth 
    
    def get_alpha(self):
        alpha = math.degrees(math.atan(self.y/self.x))
        print("alpha: ", alpha)
        return alpha
    
    def get_nw(self, alpha, beta, bear, d):
        north_coord = math.sin(alpha + bear) * d
        west_coord = math.cos(beta - bear) * d
        print("north, west: ", north_coord, west_coord)
        return north_coord, west_coord
    
    def global_coord(self):
        lat_rad = math.radians(self.lat)
        c1 = 360/40008000 #lat angle for 1 meter
        c2 = 360/(40075000) #lon angle for 1 meter
        distance = self.get_distance()
        bearing = self.get_bearing()
        alpha = self.get_alpha()
        beta = 90 - alpha
        north, west = self.get_nw(alpha, beta, bearing, distance)
        obj_coord = [self.lat + north * c1, self.lon + west * c2]
        return obj_coord
        
x = getLLH(40.443322, -79.958631, 40.443868, -79.958409, 62.1792, 114.91)
print(x.global_coord())


# test 1
# lat1 lon1 - (33.824665, -118.002167)
# lat2 lon2 - (33.833730, -118.007635)
# x = 804.672
# y = 1625.437
       