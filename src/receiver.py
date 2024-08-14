from src.conversion import ConvertObject
from data.detected_objects import DetectedObject
from src.read_config import Config
import datetime
import logging
import queue

class Data():
    #TODO Implement
    def __init__(self) -> None:
        pass

    #TODO Implement
    def get_data(self) -> DetectedObject:
        return None


class Receiver():
    def __init__(self, logger, data_source : Data, converter : ConvertObject, result_queue : queue.Queue):
        self.logger = logger
        self.logger.info("Receiver initialized")
        self.data_source = data_source
        self.converter = converter 
        self.result_queue = result_queue

    def convert(self):
        data_to_convert = self.data_source.get_data()
        #test code

        result = self.converter.get_final_coords(data_to_convert.x, data_to_convert.y)
        data_to_convert.set_global_coordinates(result[0],result[1], 0.0)
        if(result[0]!=float or result[1]!=float):
            self.logger.error("not a float")
        return result

    def enqueue(self):
        self.result_queue.put(self.convert())
        if(self.result_queue.qsize()<=0):
            self.logger.error("0 or less entries")
        else:
            self.logger.info("new entry queued")
        return self.result_queue 
    
    def process(self):
        self.convert()
        self.enqueue()



