from src.stream_listener import StreamListener
from src.coordconversion import Converter
from src.read_config import Config
from src.producer import Producer
from src.receiver import Receiver
from src.app import Application
import logging
import queue
import sys


logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Init config
    cfg = Config()

    # Init logger
    logging.basicConfig(filename="lidar-connect.log", level=logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stdout))

    # Init Stream Listener
    processing_queue = queue.Queue()
    stream_listener = StreamListener(
        cfg.stream_host(), cfg.stream_port(), processing_queue
    )

    # Init Receiver
    converter = Converter(*cfg.get_lidar_pos())
    producer_queue = queue.Queue()
    objects_receiver = Receiver(processing_queue, converter, producer_queue)

    # Init Producer
    producer = Producer(cfg.produce_target_url(), "", producer_queue, cfg.get_json_lidar_position())

    # Start the App
    app = Application(stream_listener, objects_receiver, producer)

    app.run()
