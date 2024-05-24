import unittest
from conversion import llhRotation
import numpy

class TestCalculations(unittest.TestCase):
    def test_calc_rotation(self):
        # calculation = llhRotation(10 , 20, 4, 90, 60, 120, 30)
        # self.assertEqual(calculation.calc_rotation(), [-1598559.793, 2768786.781, 5500503.115], 'The rotated coordinates are wrong')
        arr = np.array([-3.53553391, 10.60660172,  2])
        calculation = llhRotation(5, 10, 2, 45, 37.7749, -122.4194, 30)
        self.assertEqual(calculation.calc_rotation(), [-3.53553391, 10.60660172,  2], 'The rotated coordinates are wrong')

if __name__ == '__main__':
    unittest.main()


