from src.data.detected_objects import DetectedObject
from src.coordconversion import Converter
from src.receiver import Receiver
from datetime import datetime
import numpy as np
import threading
import unittest
import queue
import time


class TestReceiver(unittest.TestCase):
    def setUp(self):
        self.processing_queue = queue.Queue()
        self.converter = Converter(33.727375, -117.876614, 33.730769, -117.876566)
        self.result_queue = queue.Queue()

    def test_convert(self):
        # coordinates for test: 33.727375, -117.876614, 33.730769, -117.876566, (x,y): (375.8184, 289.865)
        # result = [33.72994163364332, -117.87251332772777]

        # Arrange
        data = DetectedObject(123, 375.8184, 289.865, 0, datetime.now(), 3)
        self.processing_queue.put(data)
        calculation = Receiver(self.processing_queue, self.converter, self.result_queue)
        # Act
        is_close = np.isclose(
            calculation.convert(), [33.72994163364332, -117.87251332772777]
        )
        # Assert
        self.assertTrue(np.all(is_close))

    def test_process(self):
        # Arrange
        receiver = Receiver(self.processing_queue, self.converter, self.result_queue)

        data = DetectedObject(123, 375.8184, 289.865, 0, datetime.now(), 3)
        self.processing_queue.put(data)

        # Act
        receiver.process()
        result = self.result_queue.get()

        # Assert
        is_close = np.isclose(result, [33.72994163364332, -117.87251332772777])
        self.assertTrue(np.all(is_close))

    def test_async_operation(self):
        # Arrange
        receiver = Receiver(self.processing_queue, self.converter, self.result_queue)
        data = DetectedObject(123, 375.8184, 289.865, 0, datetime.now(), 3)
        reciever_thread = threading.Thread(target=receiver.start_processing)

        # Act
        reciever_thread.start()
        self.processing_queue.put(data)
        self.processing_queue.put(data)
        self.processing_queue.put(data)

        time.sleep(0.1)

        # Assert
        self.assertEqual(receiver.is_running, True)
        self.assertEqual(receiver.total_processed_objects, 3)

        # Stop processing
        receiver.close()
        self.processing_queue.put(data)
        self.processing_queue.put(data)

        reciever_thread.join()
        self.assertEqual(receiver.total_processed_objects, 3)
        self.assertEqual(receiver.is_running, False)


if __name__ == "__main__":
    unittest.main()
