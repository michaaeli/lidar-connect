import unittest
from conversion import llhRotation
import numpy as np

class TestCalculations(unittest.TestCase):
    def test_calc_rotation(self):
        # calculation = llhRotation(10 , 20, 4, 90, 60, 120, 30)
        calculation = llhRotation(5, 10, 2, 45, 37.7749, -122.4194, 30)
        np.testing.assert_array_almost_equal(
            calculation.calc_rotation(), 
            [-3.53553391, 10.60660172, 2], 
            decimal=6, 
            err_msg='The rotated coordinates are wrong'
        )
    def test_llhtoxyz(self):
        # calculation = llhRotation(10 , 20, 4, 90, 60, 120, 30)
        calculation = llhRotation(5, 10, 2, 45, 37.7749, -122.4194, 30)
        np.testing.assert_array_almost_equal(
            calculation.llhtoxyz(), 
            [-2706188, -4261080, 3885744], 
            decimal=0, 
            err_msg='The cartesian coordinates are wrong'
        )

if __name__ == '__main__':
    unittest.main()

#coordinates for test
    # 1. "lat": 43.784911565845896, "lng": 77.3601425315789 - top right
    # 2. "lat": 42.33570713319381, "lng": -71.16874694824219 - top left
    # 3. "lat": -33.58778202947038, "lng": -70.45620140178822 - bottom left
    # 4. "lat": -33.58778202947038, "lng": -70.45620140178822 - bottom right


