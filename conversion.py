import json
import math

class llhRotation():
    def __init__(self, x, y, z, bear):
        self.x = x
        self.y = y
        self.z = z
        self.bear = bear
        #self.conversion-methods()

    def calc_rotation():
        # 2. Rotation Matrix for Bearing
        local_coord = [x, y, z]
        rot_matrix = [[math.cos(bear), math.sin(bear), 0],
                  [-(math.sin(bear)), math.cos(bear), 0],
                  [0, 0, 1]]
        # 3. Rotate Local Coordinates
            # multiply values
        for i in range(3):
            for j in range(3):
                rot_matrix[i][j] *= local_coord[i]
            # rotate matrix
        for i in range(3):
            for j in range(3):
                rot_matrix[i][j], rot_matrix[j][i] == rot_matrix[j][i], rot_matrix[i][j]
        rot_coord = [] * len(local_coord)
        for k in range(3):
            for l in range(3):
                #add up stuff


    #def convert_xyz_llh():

# should be a python method that does llh -> xyz conversion
# from website use llhxyz method and opposite way (xyzllh)