import yaml


class Config:
    def __init__(self) -> None:
        with open("config.yml", "r") as f:
            self.data = yaml.safe_load(f)

    def get_connection_info(self):
        url = self.data["rest"]["url"]
        port = self.data["rest"]["port"]
        return url, port

    def get_lidar_pos(self):
        lat1 = self.data["lidar_coords"]["lat1"]
        lon1 = self.data["lidar_coords"]["lon1"]
        lat2 = self.data["lidar_coords"]["lat2"]
        lon2 = self.data["lidar_coords"]["lon2"]
        return [lat1, lon1, lat2, lon2]
