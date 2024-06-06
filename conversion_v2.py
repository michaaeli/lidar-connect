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

    def get_distance(self):
        distance = math.sqrt(self.x ** 2 + self.y ** 2)
        print("distance: ", distance)
        return distance
        
    def get_bearing(self):
        geodesic = pyproj.Geod(ellps='WGS84')
        fwd_azimuth,back_azimuth,distance = geodesic.inv(self.lon, self.lat, self.lon2, self.lat2)
        #back_azimuth = -1 * back_azimuth
        print("bearing: ", fwd_azimuth)
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
        c1 = 360/40008000 #lat angle for 1 meter
        c2 = 360/40075000 #lon angle for 1 meter
        distance = self.get_distance()
        bearing = self.get_bearing()
        alpha = self.get_alpha()
        beta = 90 - alpha
        north, west = self.get_nw(alpha, beta, bearing, distance)
        obj_coord = [self.lat + north * c1, self.lon + west * c2]
        return obj_coord
    
    def experimental(self):
        az = self.get_bearing()
        alpha = math.degrees(math.atan(self.y/self.x))
        print(f"alpha = {alpha}")
        d = math.sqrt(self.x*self.x + self.y*self.y)
        x = math.cos(math.radians(alpha-az))*d
        y = math.sin(math.radians(alpha-az))*d
        print(f"x = {x} \ny = {y}")

        lat, lon = xy2latlon(x, y, self.lat, self.lon)
        return [lat, lon]
    
    def experimental2(self):
        az = self.get_bearing()
        print(f"az: {az}")
        d = math.sqrt(self.x*self.x + self.y*self.y)
        final_bearing = az
        cos_alpha = self.x/d
        alpha = np.rad2deg(np.arccos(cos_alpha))
        print(f"alpha: {alpha}")
        final_bearing += 90 - alpha
        print(f"final_bearing: {final_bearing}")


        return compute_destination_point(self.lat, self.lon, d, final_bearing)

        
x = getLLHx = getLLH(33.745058, -117.937491, 33.746808, -117.937509, -199.949, 401.4216)
#print(x.global_coord())
print(x.experimental2())


# test 1
# lat1 lon1 - (40.443323, -79.958623)
# lat2 lon2 - (40.444011, -79.958346)
# x = 61.8744
# y = 111.252
       

# test 2
# x = getLLH(40.443893, -79.95858, 40.444363, -79.958519, 30, 50)
# Expected 40.444327, -79.958183
# Actual   40.444394, -79.958062


# test 2
# x = getLLH(40.443893, -79.95858, 40.444363, -79.958519, 50, 70)
# Expected 40.444484, -79.957933
# Actual   40.444394, -79.958062
#          40.443123, -79.958499

# test 3
# x = getLLH(33.730979, -117.937358, 33.736142, -117.943838, -1142.63, 1110.45)
# Expected 33.737889, -117.946033
# Actual   33.730433665414175, -117.95457518440682

# test 4
# x = getLLH(33.745058, -117.937491, 33.746808, -117.937509, -199.949, 401.4216)
# Expected 33.748647, -117.939685
# Actual   33.748652468209535, -117.9396908489785