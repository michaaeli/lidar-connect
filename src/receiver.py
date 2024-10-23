from src.data.detected_objects import DetectedObject

# from data.detected_objects import DetectedObject

from src.coordconversion import Converter

# from coordconversion import Converter
import logging
import queue

logger = logging.getLogger(__name__)


class Receiver:
    """
    Processes queue of detected objects, applies coordinates conversion, pushes results to the result queue.
    **Blocks on empty queue**
    """

    def __init__(
        self,
        processing_queue: queue.Queue,
        converter: Converter,
        result_queue: queue.Queue,
    ):
        self.processing_queue = processing_queue
        self.converter = converter
        self.result_queue = result_queue

        self.stop_signal: bool = False
        self.is_running: bool = False
        self.total_processed_objects: int = 0

    def convert(self):
        data_to_convert: DetectedObject = self.processing_queue.get()
        if self.stop_signal:
            return None
        # result = self.converter.get_final_coords(data_to_convert.x, data_to_convert.y)
        result = self.converter.get_final_coords(data_to_convert.y, data_to_convert.z) # TODO debug
        # TODO check height
        data_to_convert.set_global_coordinates(result[0], result[1], 0.0)
        return data_to_convert

    def process(self):
        converted = self.convert()
        if converted is None:
            return
        self.result_queue.put(converted)
        self.total_processed_objects += 1

    def close(self):
        self.stop_signal = True

    def start_processing(self):
        """
        Processes objects queue until stopped.
        """
        logger.info("Receiver started processing")
        self.is_running = True
        while not self.stop_signal:
            self.process()

        self.is_running = False
        logger.info("Receiver stopped processing")
