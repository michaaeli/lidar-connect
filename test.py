import unittest
from conversion import llhRotation
import numpy as np

class TestCalculations(unittest.TestCase):
    #coordinates for test
    # 1. "lat": 43.784911565845896, "lng": 77.3601425315789 - top right
    def test_conversion1(self):
        calculation = llhRotation(43.784911565845896, 77.3601425315789, 0, 0)
        np.testing.assert_array_almost_equal(
            calculation.llhtoxyz(), 
            [1009217, 4500271, 4390869], 
            decimal=0, 
            err_msg='The conversion is incorrect'
        )
        np.testing.assert_array_almost_equal(
            calculation.xyztollh([1009217, 4500271, 4390869]), 
            [43.78491, 77.36015, -0.6], 
            decimal=0, 
            err_msg='The conversion is incorrect'
        )
    # 2. "lat": 42.33570713319381, "lng": -71.16874694824219 - top left
    def test_conversion2(self):
        calculation = llhRotation(42.33570713319381, -71.16874694824219, 0, 0)
        np.testing.assert_array_almost_equal(
            calculation.llhtoxyz(), 
            [1524166, -4469215, 4273242], 
            decimal=0, 
            err_msg='The conversion is incorrect'
        )
        np.testing.assert_array_almost_equal(
            calculation.xyztollh([1524166, -4469215, 4273242]), 
            [42.33571, 288.83126, -0.2], 
            decimal=0, 
            err_msg='The conversion is incorrect'
        )
    # 3. "lat": -33.58778202947038, "lng": -70.45620140178822 - bottom left
    def test_conversion3(self):
        calculation = llhRotation(-33.58778202947038, -70.45620140178822, 0, 0)
        np.testing.assert_array_almost_equal(
            calculation.llhtoxyz(), 
            [1779247, -5012259, -3508449], 
            decimal=0, 
            err_msg='The conversion is incorrect'
        )
        np.testing.assert_array_almost_equal(
            calculation.xyztollh([1779247, -5012259, -3508449]), 
            [-33.58778, 289.5438, 0.1], 
            decimal=0, 
            err_msg='The conversion is incorrect'
        )
    # 4. "lat": -37.714454390841574, "lng": 85.8736388610805 - bottom right
    def test_conversion4(self):
        calculation = llhRotation(-37.714454390841574, 85.8736388610805, 0, 0)
        np.testing.assert_array_almost_equal(
            calculation.llhtoxyz(), 
            [363515, 5038784, -3880420], 
            decimal=0, 
            err_msg='The conversion is incorrect'
        )
        np.testing.assert_array_almost_equal(
            calculation.xyztollh([363515, 5038784, -3880420]), 
            [-37.71445, 85.87364, -0.3], 
            decimal=0, 
            err_msg='The conversion is incorrect'
        )

if __name__ == '__main__':
    unittest.main()




