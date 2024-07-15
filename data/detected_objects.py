from typing import List
import datetime
OBJECT_TYPE_NAME_MAP = {
    0: "Unknown",
    1: "pedestrian",
    2: "cyclist",
    3: "car",
    4: "truck",
    5: "bus"
}

class DetectedObject:
    def __init__(self, id:int, x:float,y:float,z:float, time:datetime, object_type:int, width:float=0,length:float=0,height:float=0, speed:float=0) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.time = time,
        self.object_type = object_type
        self.object_name = OBJECT_TYPE_NAME_MAP[object_type]
        self.width = width
        self.length = length
        self.height = height
        self.speed = speed
    
    def get_position(self) -> List[float]:
        """Returns local x,y,z coordinates"""
        return [self.x, self.y, self.z]
    
    def set_global_coordinates(self, latitude:float, longitude:float, height:float) -> None:
        """Assign global Latitude/Longitude/Height coordinates"""
        self.lat = latitude
        self.lon = longitude
        self.h = height

    def to_json(self) -> str:
        """Converts object to JSON""" #TODO
        return ""
    
    def __str__(self) -> str:
        return f"ID: {self.id}\nObject Type: {self.object_name}\nSpeed: {self.speed}\nWidth: {self.width}\nLength: {self.length}\nHeight: {self.height}\nTime: {self.time}"
