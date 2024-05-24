import json
import math
import numpy as np
import pyproj

class llhRotation():
    def __init__(self, x, y, z, bear, lat, lon, h):
        self.x = x
        self.y = y
        self.z = z
        self.bear = bear
        self.lat = lat
        self.lon = lon
        self.h = h
        #self.conversion-methods()
        self.xyztollh()

    def calc_rotation(self):
        local_coord = np.array([self.x, self.y, self.z])
        bear_rad = math.radians(self.bear)
        rot_matrix = np.array([[math.cos(bear_rad), -(math.sin(bear_rad)), 0],
                      [math.sin(bear_rad), math.cos(bear_rad), 0],
                      [0, 0, 1]])
        for i in range(3):
            rot_matrix[:, i] *= local_coord[i]
        rot_coord = np.sum(rot_matrix, axis = 1)
        print(rot_coord)
        return rot_coord

    def llhtoxyz(self):
        transformer = pyproj.Transformer.from_crs(
            {"proj":'latlong', "ellps":'WGS84', "datum":'WGS84'},
            {"proj":'geocent', "ellps":'WGS84', "datum":'WGS84'},
            )
        x, y, z = transformer.transform(self.lon,self.lat,self.h,radians = False)
        lidar_coord = np.array([x, y, z])
        return lidar_coord

    def translateToGlobal(self):
        rot_coord = self.calc_rotation()
        lidar_coord = self.llhtoxyz()
        combined_coord = rot_coord + lidar_coord 
        return combined_coord

    def xyztollh(self):
        global_coord = self.translateToGlobal()
        transformer2 = pyproj.Transformer.from_crs(
            {"proj":'geocent', "ellps":'WGS84', "datum":'WGS84'},
            {"proj":'latlong', "ellps":'WGS84', "datum":'WGS84'},
            )
        lon, lat, h =transformer2.transform(global_coord[0],global_coord[1],global_coord[2],radians=False)
        final_coord = [lat, lon, h]
        return final_coord 

test = llhRotation(5, 10, 2, 45, 37.7749, -122.4194, 30)
print(test)
