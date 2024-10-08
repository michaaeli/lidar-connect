from typing import List
from datetime import datetime

OBJECT_TYPE_NAME_MAP = {
    0: "Unknown",
    1: "pedestrian",
    2: "cyclist",
    3: "car",
    4: "truck",
    5: "bus",
}


class DetectedObject:
    def __init__(
        self,
        id: int,
        x: float,
        y: float,
        z: float,
        time: datetime,
        object_type: int,
        width: float = 0,
        length: float = 0,
        height: float = 0,
        speed: float = 0,
    ) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.time = time
        self.object_type = object_type
        self.object_name = OBJECT_TYPE_NAME_MAP[object_type]
        self.width = width
        self.length = length
        self.height = height
        self.speed = speed

    def get_position(self) -> List[float]:
        """Returns local x,y,z coordinates"""
        return [self.x, self.y, self.z]

    def set_global_coordinates(
        self, latitude: float, longitude: float, height: float
    ) -> None:
        """Assign global Latitude/Longitude/Height coordinates"""
        self.lat = latitude
        self.lon = longitude
        self.h = height

    def to_json(self) -> str:
        """Converts object to JSON"""  # TODO
        return ""

    def __str__(self) -> str:
        return f"ID: {self.id}\nObject Type: {self.object_name}\nSpeed: {self.speed}\nWidth: {self.width}\n \
        Length: {self.length}\nHeight: {self.height}\nTime: {self.time}"


def convert_system_timestamp_to_datetime(ts: int) -> datetime:
    return datetime.fromtimestamp(ts / 1000)


def detected_objects_from_json(parsed_json_object: dict) -> list[DetectedObject]:
    """Repacks message from hardware into list of detected objects"""
    objects = []
    if (
        "sys_timestamp" not in parsed_json_object
        or "object_list" not in parsed_json_object
    ):
        return []
    time = convert_system_timestamp_to_datetime(
        int(parsed_json_object["sys_timestamp"])
    )
    for obj in parsed_json_object["object_list"]:
        id = int(obj["object_id"])
        x = float(obj["x"])
        y = float(obj["y"])
        z = float(obj["z"])
        type = int(obj["object_type"])
        width = float(obj["width"])
        length = float(obj["length"])
        height = float(obj["height"])
        speed = float(obj["speed"])

        objects.append(
            DetectedObject(id, x, y, z, time, type, width, length, height, speed)
        )
    return objects
