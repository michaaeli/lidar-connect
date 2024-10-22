from datetime import datetime
from typing import List

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
        object_width: float = 0,
        object_length: float = 0,
        object_height: float = 0,
        speed: float = 0,
    ) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.time = time
        self.object_type = object_type
        self.object_name = OBJECT_TYPE_NAME_MAP[object_type]
        self.object_width = object_width
        self.object_length = object_length
        self.object_height = object_height
        self.speed = speed

        self.lat = 0
        self.lon = 0
        self.h = 0

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
        res = "{"
        res += (
            f"""
            "id":{self.id},
            "object_type":{self.object_type},
            "object_name":"{self.object_name}",
            "object_width": {self.object_width},
            "object_length": {self.object_length},
            "object_height": {self.object_height},
            "speed": {self.speed},
            "lat":{self.lat},
            "lon":{self.lon},
            "h":{self.h},
            "time":"{self.time}" """
            + "}"
        )
        return res

    def __str__(self) -> str:
        return f"ID: {self.id}\nObject Type: {self.object_name}\nSpeed: {self.speed}\nWidth: {self.object_width}\n \
        Length: {self.object_length}\nHeight: {self.object_height}\nTime: {self.time}"


def convert_system_timestamp_to_datetime(ts: int) -> datetime:
    return datetime.fromtimestamp(ts / 1000)


def detected_objects_to_json(objects: List[DetectedObject]) -> str:
    """Packs list of DetectedObjects into json string"""
    result = """{"objects": ["""
    encoded = []
    for obj in objects:
        encoded.append(obj.to_json())
    result += str.join(",", encoded)
    result += "]}"

    return result


def detected_objects_list_to_json_bytes(objects: List[DetectedObject]) -> bytes:
    return bytes(detected_objects_to_json(objects), "utf-8")


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
