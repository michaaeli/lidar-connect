import json
import math
import numpy as np
import pyproj

class llhRotation():
    def __init__(self, lat, lon, h, bear):
        self.lat = lat
        self.lon = lon
        self.h = h
        self.bear = math.radians(bear)
        
        self.converted_lidar = self.llhtoxyz()

    def local_to_global(self, x, y, z):
        coord_sum = self.calc_rotation(x, y, z) + self.converted_lidar
        final_coord = self.xyztollh(coord_sum)
        return final_coord

    def calc_rotation(self, x, y, z):
        local_coord = np.array([x, y, z])
        rot_matrix = np.array([[math.cos(self.bear), -(math.sin(self.bear)), 0],
                      [math.sin(self.bear), math.cos(self.bear), 0],
                      [0, 0, 1]])
        for i in range(3):
            rot_matrix[:, i] *= local_coord[i]
        rot_coord = np.sum(rot_matrix, axis = 1)
        return rot_coord
    
    def llhtoxyz(self):
        transformer = pyproj.Transformer.from_crs(
            {"proj":'latlong', "ellps":'WGS84', "datum":'WGS84'},
            {"proj":'geocent', "ellps":'WGS84', "datum":'WGS84'},
            )
        x, y, z = transformer.transform(self.lon,self.lat,self.h,radians = False)
        lidar_coord = np.array([x, y, z])
        return lidar_coord
    
    def xyztollh(self, coord):
        transformer2 = pyproj.Transformer.from_crs(
            {"proj":'geocent', "ellps":'WGS84', "datum":'WGS84'},
            {"proj":'latlong', "ellps":'WGS84', "datum":'WGS84'},
            )
        lon, lat, h = transformer2.transform(coord[0],coord[1],coord[2],radians=False)
        if(lon>0):
            lon = 360-lon
        else:
            lon = lon
        final_coord = [lat, lon, h]
        return final_coord 
    
    @staticmethod
    def get_bearing(lat1, lon1, lat2, lon2):
        geodesic = pyproj.Geod(ellps='WGS84')
        fwd_azimuth,back_azimuth,distance = geodesic.inv(lon1, lat1, lon2, lat2)
        return fwd_azimuth 

    
test = llhRotation(34.077786, -117.702655, 40, 0)
print(test.local_to_global(0, 1303.57, 0))

print(test.get_bearing(34.077786, -117.702655, 34.080581, -117.710441))


# (0,0,-40)