import unittest
from receiver import Receiver, Data
from data.detected_objects import DetectedObject
from conversion import ConvertObject
from datetime import datetime
from unittest.mock import Mock
import logging
import numpy as np

class DataSource():
    def __init__(self) -> None:
        pass

class TestReceiver():
    def setUp(self):
        self.logger = Mock()
        self.data = DataSource()
        self.converter = Mock()
        self.result_queue = Mock()

    def test_convert(self):
        #coordinates for test: 33.727375, -117.876614, 33.730769, -117.876566, (x,y): (375.8184, 289.865), result = [33.72994163364332, -117.87251332772777]
        calculation = Receiver(logging.logger("test"), self.data, self.converter, self.result_queue)

        mock_data = DetectedObject(123, 12, 12, 0, datetime.now(), 3)
        self.data.get_data.return_value = mock_data

        conversion = ConvertObject(logging.getLogger('test'), 33.727375, -117.876614, 33.730769, -117.876566)

        np.testing.assert_array_almost_equal(
            conversion.convert(), 
            [33.72994163364332, -117.87251332772777], 
            decimal=0, 
            err_msg='The conversion is incorrect'
        )

if __name__ == '__main__':
    unittest.main()
    



        
