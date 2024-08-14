import unittest
from src.receiver import Receiver
from data.detected_objects import DetectedObject
from src.conversion import ConvertObject
from datetime import datetime
from unittest.mock import Mock
import logging
import numpy as np
import queue


class TestReceiver(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger("test")
        self.data = Mock()
        self.converter = ConvertObject(
            self.logger, 33.727375, -117.876614, 33.730769, -117.876566
        )
        self.result_queue = queue.Queue()

    def test_convert(self):
        # coordinates for test: 33.727375, -117.876614, 33.730769, -117.876566, (x,y): (375.8184, 289.865)
        # result = [33.72994163364332, -117.87251332772777]

        # Arrange
        mock_data = DetectedObject(123, 375.8184, 289.865, 0, datetime.now(), 3)
        self.data.get_data.return_value = mock_data
        calculation = Receiver(
            self.logger, self.data, self.converter, self.result_queue
        )
        # Act
        is_close = np.isclose(
            calculation.convert(), [33.72994163364332, -117.87251332772777]
        )
        # Assert
        print(calculation)
        print(is_close)
        print(np.all(is_close))
        self.assertTrue(np.all(is_close))

    def test_enqueue(self):
        # Arrange
        mock_data = DetectedObject(123, 375.8184, 289.865, 0, datetime.now(), 3)
        self.data.get_data.return_value = mock_data
        calculation = Receiver(
            self.logger, self.data, self.converter, self.result_queue
        )
        q = calculation.enqueue()
        # Act
        is_close = np.isclose(q.get(), [33.72994163364332, -117.87251332772777])
        # Assert
        self.assertTrue(np.all(is_close))

    def test_process(self):
        # Arrange
        receiver = Receiver(self.logger, self.data, self.converter, self.result_queue)
        # data = Mock(spec=Data)

        detected_object = DetectedObject(123, 375.8184, 289.865, 0, datetime.now(), 3)
        self.data.get_data.return_value = detected_object

        # Act
        receiver.process()
        result = self.result_queue.get()

        # Assert
        self.data.get_data.assert_called_with()
        is_close = np.isclose(result, [33.72994163364332, -117.87251332772777])
        self.assertTrue(np.all(is_close))


if __name__ == "__main__":
    unittest.main()
