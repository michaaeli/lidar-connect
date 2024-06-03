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
        return back_azimuth 
    
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
        c1 = 360/40008000 #lat angle for 1 meter
        c2 = 360/40007000 #lon angle for 1 meter
        distance = self.get_distance()
        bearing = self.get_bearing()
        alpha = self.get_alpha()
        beta = 90 - alpha
        north, west = self.get_nw(alpha, beta, bearing, distance)
        obj_coord = [self.lat + north * c1, self.lon + west * c2]
        return obj_coord
        
x = getLLH(40.442871, -79.957895, 40.444236, -79.956874, 209.215, 788.579)
print(x.global_coord())


# test 1
# lat1 lon1 - (40.443323, -79.958623)
# lat2 lon2 - (40.444011, -79.958346)
# x = 61.8744
# y = 111.252
       