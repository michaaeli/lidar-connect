from conversion import ConvertObject
from data.detected_objects import DetectedObject
from read_config import Config
import datetime
import logging

class Receiver():
    def __init__(self, logger, data_source, converter, result_queue):
        self.logger = logger
        self.logger.info("Receiver initialized")
        self.data_source = data_source
        self.converter = converter
        self.result_queue = result_queue

    def convert(self):
        self.data_source = Data()
        data_to_convert = self.data_source.get_data()
        #test code
        # coords = Config()
        # lidar_pos = coords.get_lidar_pos()
        coords = Config()
        lidar_pos = coords.get_lidar_pos()
        self.converter = ConvertObject(self.logger, lidar_pos[0], lidar_pos[1], lidar_pos[2], lidar_pos[3])

        result = self.converter.get_final_coords(data_to_convert.x, data_to_convert.y)
        data_to_convert.set_global_coordinates(result[0],result[1], 0.0)
        if(result[0]!=float or result[1]!=float):
            self.logger.error("not a float")
        return result
    
    def enqueue(self):
        self.result_queue.append(self.convert())
        if(len(self.result_queue)<=0):
            self.logger.error("0 or less entries")
        else:
            self.logger.info("new entry queued")
        return self.result_queue 
    
class Data():
    def __init__(self) -> None:
        pass

    def get_data(self):
        data = DetectedObject(123, 12, 12, 0, datetime.datetime.now(), 3)
        if(len(list)<3):
            self.logger.error("at least 1 entry missing")
        return data

# test 3
# x = getLLH(33.730979, -117.937358, 33.736142, -117.943838, -1142.63, 1110.45)
# Expected 33.737889, -117.946033
# Actual   33.730433665414175, -117.95457518440682
if __name__ == "__main__":
    
    coords = Config()
    lidar_pos = coords.get_lidar_pos()
    
    data1 = (lidar_pos[0], lidar_pos[1], lidar_pos[2], lidar_pos[3])
    arr = []
    i = ConvertObject(lidar_pos[0], lidar_pos[1], lidar_pos[2], lidar_pos[3])

    x = Receiver(data1, i, arr)
    print(x.convert())
    print(x.enqueue())

