from test.stream_listener_test import DataStreamServer, TEST_DATA, PACKAGE_LEN
from src.stream_listener import StreamListener
import threading
import queue
import time


class PerpetualObjectsProducer(DataStreamServer):
    """
    Produces 1 detected object with `time_interval` until gets interrupted by keyboard or by client signal.
    """

    def __init__(
        self, host: str, port: int, package_len: int = 1024, time_interval: int = 1
    ) -> None:
        """`time_interval` in seconds"""
        super().__init__(host, port, package_len)
        self.interval = time_interval
        self.interrupt = False

    def serve_perpetually(self, data):
        """
        Opens connection, waits for the client,
        sends 1 test message every `time_interval` until gets interrupted, closes connection.
        **Blocks until interrupted.**
        """
        # Blocks until client connects
        self.open_stream()
        # Send message every `time_interval` until interrupted
        while True:
            try:
                self.send_data(data)
                if self.interrupt:
                    break
                time.sleep(self.interval)
            except KeyboardInterrupt:  # TODO catch client termination signal
                break
        # Close connection when interrupted
        self.close()


if __name__ == "__main__":
    # Set up server
    host, port = "localhost", 3399
    server = PerpetualObjectsProducer(host, port, package_len=PACKAGE_LEN)
    server_thread = threading.Thread(target=server.serve_perpetually, args=[TEST_DATA])

    # Start serving
    server_thread.start()

    # Start client
    q = queue.Queue()
    client = StreamListener(host, port, q)
    client_thread = threading.Thread(target=client.wrapped_consume)
    client_thread.start()

    # Execute until KeyboardInterrupt:
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            server.interrupt = True
            break

    server_thread.join()
    client_thread.join()
