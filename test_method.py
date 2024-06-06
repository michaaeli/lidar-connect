import math

class point_convert():
    def __init__(self, lat1, lon1, lat2, lon2):
        self.lat1 = lat1
        self.lon1 = lon1
        self.lat2 = lat2
        self.lon2 = lon2

    def find_point(self):
        latx = (self.lat2 - self.lat1)/2

