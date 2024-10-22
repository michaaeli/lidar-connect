from http.server import BaseHTTPRequestHandler, HTTPServer
from src.data.detected_objects import (
    DetectedObject,
    detected_objects_list_to_json_bytes,
)
import requests as req
import threading
import logging
import queue

logger = logging.getLogger(__name__)

# ATTENTION: This is for quick demo purpouses only!
# To use in production, replace this module with a module that sends data to a backend through socket


class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, return_q: list, lidar_pos: str, *args, **kwargs):
        # Store dynamic data in the handler instance
        self.return_q = return_q
        self.lidar_pos = bytes(lidar_pos, "utf-8")
        super().__init__(*args, **kwargs)

    def do_GET(self):
        print(self.path)
        if self.path == "/":
            # Custom endpoint logic
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            try:
                self.wfile.write(detected_objects_list_to_json_bytes(self.return_q))
                self.return_q.clear()
            except Exception as e:
                logger.error(e)
        elif self.path == "/lidar":
            print(self.lidar_pos)
            # Custom endpoint logic
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            try:
                self.wfile.write(self.lidar_pos)
            except Exception as e:
                logger.error(e)
        else:
            # Default 404 response for unknown paths
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error": "Not Found"}')

    def do_OPTIONS(self):
        # Handle preflight requests for CORS (OPTIONS method)
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


class Producer:
    """
    Transports data to remote server
    """

    # TODO IMPLEMENT
    def __init__(
        self,
        produce_url: str,
        healthcheck_url: str,
        queue: queue.Queue,
        lidar_pos: str,
    ) -> None:
        self.url = produce_url
        self.health_url = healthcheck_url
        self.q = queue
        self.stop_signal = False
        self.lidar_pos = lidar_pos

        self.host = "localhost"
        self.port = 5000
        self.server_q = []
        self.server = HTTPServer(
            (self.host, self.port),
            lambda *args, **kwargs: CustomHTTPRequestHandler(
                self.server_q, self.lidar_pos, *args, **kwargs
            ),
        )

    def close(self) -> None:
        self.stop_signal = True
        self.server.shutdown()

    def isalive(self) -> bool:
        r = req.get(self.health_url)
        if r.status_code == 200:
            return True
        return False

    def produce(self) -> None:
        obj: DetectedObject = self.q.get()
        # print(obj)
        self.server_q.append(obj)

    def start(self) -> None:
        thread = threading.Thread(target=self.server.serve_forever)
        thread.start()
        logger.info("Producer started")
        while not self.stop_signal:
            self.produce()
        logger.info("Producer finished")
