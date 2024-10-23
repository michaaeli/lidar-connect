import yaml


class Config:
    def __init__(self) -> None:
        with open("config.yml", "r") as f:
            self.data = yaml.safe_load(f)
            self.datastream_host = self.data["data_stream"]["host"]
            self.datastream_port = self.data["data_stream"]["port"]
            self.lat1 = self.data["lidar_coords"]["lat1"]
            self.lon1 = self.data["lidar_coords"]["lon1"]
            self.lat2 = self.data["lidar_coords"]["lat2"]
            self.lon2 = self.data["lidar_coords"]["lon2"]
            self.target_url = self.data["producer"]["target_url"]

    def stream_host(self) -> str:
        return self.datastream_host

    def stream_port(self) -> str:
        return self.datastream_port

    def get_lidar_pos(self):
        """
        Returns lidar location Lat,Lon with callibration point Lat,Lon
        """
        return [self.lat1, self.lon1, self.lat2, self.lon2]

    def produce_target_url(self):
        return self.target_url


if __name__ == "__main__":
    c = Config()
    p = c.stream_port()
    print(p, type(p))
