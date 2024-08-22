from stream_listener import StreamListener
from receiver import Receiver
from producer import Producer
import threading
import logging
import time

logger = logging.getLogger(__name__)


class Application:
    """
    Runs StreamListener, Receiver, Producer in separate threads
    """

    def __init__(
        self, stream_listener: StreamListener, receiver: Receiver, producer: Producer
    ):
        self.listener = stream_listener
        self.receiver = receiver
        self.producer = producer

    def close(self) -> None:
        # TODO Join queue
        self.listener.close()
        self.receiver.close()
        self.producer.close()

    def run(self) -> None:
        listener_thread = threading.Thread(target=self.listener.wrapped_consume)
        receiver_thread = threading.Thread(target=self.receiver.start_processing)
        producer_thread = threading.Thread(target=self.producer.start)

        listener_thread.start()
        receiver_thread.start()
        producer_thread.start()

        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Received KeyboardInterrupt, stopping the app...")
                self.close()
                break

        listener_thread.join()
        receiver_thread.join()
        producer_thread.join()

        logger.info("App finished execution")


if __name__ == "__main__":
    app = Application()
