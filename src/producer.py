from src.data.detected_objects import DetectedObject
import requests as req
import logging
import queue

logger = logging.getLogger(__name__)


class Producer:
    """
    Transports data to remote server
    """

    # TODO IMPLEMENT
    def __init__(
        self, produce_url: str, healthcheck_url: str, queue: queue.Queue
    ) -> None:
        self.url = produce_url
        self.health_url = healthcheck_url
        self.q = queue
        self.stop_signal = False

    def close(self) -> None:
        self.stop_signal = True

    def isalive(self) -> bool:
        r = req.get(self.health_url)
        if r.status_code == 200:
            return True
        return False

    def produce(self) -> None:
        obj: DetectedObject = self.q.get()
        print([obj.lat, obj.lon, obj.h])

    def start(self) -> None:
        logger.info("Producer started")
        while not self.stop_signal:
            self.produce()
        logger.info("Producer finished")
