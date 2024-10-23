from src.stream_listener import StreamListener
from src.coordconversion import Converter
from src.read_config import Config
from src.producer import Producer
from src.receiver import Receiver
from src.app import Application
import logging
import queue
import sys


# class Server:
#     def __init__(self, logger, url):
#         self.logger = logger
#         self.logger.info("Server Initialized")
#         self.url = url
#         self.check_status()

#     def check_status(self):
#         try:
#             response = requests.get(self.url)
#             if response.status_code == 201:
#                 print("Server is up.")
#                 return True
#         except Exception:
#             self.logger.error("0 or less entries")
#             raise Exception("Make sure everything is running")

#     def send_objects(self, data):
#         res = requests.post(url=url, json=data)
#         print(res.text)


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
    producer = Producer(cfg.produce_target_url(), "", producer_queue)

    # Start the App
    app = Application(stream_listener, objects_receiver, producer)

    app.run()
