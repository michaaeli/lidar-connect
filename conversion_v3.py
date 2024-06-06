import math
import numpy as np
import pyproj

class convert():
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
        print("bearing: ", fwd_azimuth)
        return fwd_azimuth 
    
    def get_alpha(self):
        alpha = math.degrees(math.atan(self.y/self.x))
        print("alpha: ", alpha)
        return alpha
    
    def get_final_coords(self):
        d = self.get_distance()
        alpha = self.get_alpha()
        bearing = self.get_bearing()
        beta = 90-alpha
        x_final = math.cos(math.radians(alpha - bearing)) * d
        y_final = math.sin(math.radians(alpha - bearing)) * d
        return x_final, y_final

    def local2latlon(x, y, z, origin):
        return

    def local_to_global(self):
        x, y = self.get_final_coords()
        z = 0
        [lat, lon] = self.local2latlon(x, y, z)
        return [lat, lon]


    


    

x = convert(40.443893, -79.958580, 40.444393, -79.959053, 170, 50)
print(x.get_final_coords())
print(x.local_to_global())

#manual bearing func
    # def azimuth(lat1, lon1, lat2, lon2):
    #     d_lon = math.radians(lon2 - lon1)
    #     lat1 = math.radians(lat1)
    #     lat2 = math.radians(lat2)
    #     y = math.sin(d_lon) * math.cos(lat2)
    #     x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(d_lon)
    #     az = math.atan2(y, x)
    #     az = math.degrees(az)
    #     return az