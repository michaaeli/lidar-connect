import unittest
from receiver import Receiver, Data
from data.detected_objects import DetectedObject
from conversion import ConvertObject
from datetime import datetime
from unittest.mock import Mock
from unittest.mock import MagicMock
import logging
import numpy as np
import queue

class TestReceiver(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger("test")
        self.data = Mock()
        self.converter = ConvertObject(self.logger, 33.727375, -117.876614, 33.730769, -117.876566)
        self.result_queue = queue.Queue()

    def test_convert(self):
        #coordinates for test: 33.727375, -117.876614, 33.730769, -117.876566, (x,y): (375.8184, 289.865), result = [33.72994163364332, -117.87251332772777]
    
        #Arrange
        mock_data = DetectedObject(123, 375.8184, 289.865, 0, datetime.now(), 3)
        self.data.get_data.return_value = mock_data
        calculation = Receiver(self.logger, self.data, self.converter, self.result_queue)
        #Act
        is_close = np.isclose(
            calculation.convert(), 
            [33.72994163364332, -117.87251332772777]
        )
        #Assert 
        print(calculation)
        print(is_close)
        print(np.all(is_close))
        self.assertTrue(np.all(is_close))

    def test_enqueue(self):
        #Arrange
        mock_data = DetectedObject(123, 375.8184, 289.865, 0, datetime.now(), 3)
        self.data.get_data.return_value = mock_data
        calculation = Receiver(self.logger, self.data, self.converter, self.result_queue)
        q = calculation.enqueue()
        #Act
        is_close = np.isclose(
            q.get(), 
            [33.72994163364332, -117.87251332772777]
        )
        #Assert
        self.assertTrue(np.all(is_close))

    def test_process(self):
        # #Arrange
        # mock_data = DetectedObject(123, 375.8184, 289.865, 0, datetime.now(), 3)
        # self.data.get_data.return_value = mock_data
        # calculation = Receiver(self.logger, self.data, self.converter, self.result_queue)
        # #Act
        # #Assert
        
        receiver = Receiver(self.logger, self.data, self.converter, self.result_queue)
        self.mock_detected_object = Mock(spec=DetectedObject)
        self.mock_detected_object.x = 375.8184
        self.mock_detected_object.y = 289.865
        self.mock_detected_object.set_global_coordinates = Mock()

        self.converter = Mock(spec=ConvertObject)
        self.converter.get_final_coords.return_value = (33.72994163364332, -117.87251332772777)
        # Arrange

        # Act
        receiver.process()

        # Assert
        self.data.get_data.assert_called_once()
        self.converter.get_final_coords.assert_called_once_with(375.8184, 289.865)
        self.mock_detected_object.set_global_coordinates.assert_called_once_with(33.72994163364332, -117.87251332772777, 0.0)
        self.assertEqual(self.result_queue.qsize(), 1)
        self.logger.info.assert_called_with("new entry queued")

    

if __name__ == '__main__':
    unittest.main()
    



        
