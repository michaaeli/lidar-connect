from src.data.detected_objects import DetectedObject
import logging
import queue

logger = logging.getLogger(__name__)


class Producer:
    # TODO IMPLEMENT
    def __init__(self, url: str, queue: queue.Queue) -> None:
        self.url = url
        self.q = queue
        self.stop_signal = False

    def close(self) -> None:
        self.stop_signal = True

    def isalive(self) -> bool:
        return NotImplemented

    def produce(self) -> None:
        obj: DetectedObject = self.q.get()
        print([obj.lat, obj.lon, obj.height])

    def start(self) -> None:
        logger.info("Producer started")
        while not self.stop_signal:
            self.produce()
        logger.info("Producer finished")
