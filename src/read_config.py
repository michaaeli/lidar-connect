import yaml


class Config:
    def __init__(self) -> None:
        with open("config.yml", "r") as f:
            self.data = yaml.safe_load(f)
            self.datastream_host = self.data["data_stream"]["host"]
            self.datastream_port = self.data["data_stream"]["port"]
            self.lidar_lat = self.data["lidar_coords"]["lidar_lat"]
            self.lidar_lon = self.data["lidar_coords"]["lidar_lon"]
            self.ref_lat = self.data["lidar_coords"]["ref_lat"]
            self.ref_lon = self.data["lidar_coords"]["ref_lon"]
            self.target_url = self.data["producer"]["target_url"]

    def stream_host(self) -> str:
        return self.datastream_host

    def stream_port(self) -> str:
        return self.datastream_port

    def get_lidar_pos(self):
        """
        Returns lidar location Lat,Lon with callibration point Lat,Lon
        """
        return [self.lidar_lat, self.lidar_lon, self.ref_lat, self.ref_lon]

    def get_json_lidar_position(self):
        lidar = "{" + f'"lat":{self.lidar_lat},"lon":{self.lidar_lon}' + "}"
        ref = "{" + f'"lat":{self.ref_lat},"lon":{self.ref_lon}' + "}"
        return "{" + f'"lidar":{lidar}, "ref":{ref}' + "}"

    def produce_target_url(self):
        return self.target_url


if __name__ == "__main__":
    c = Config()
    p = c.stream_port()
    print(p, type(p))
