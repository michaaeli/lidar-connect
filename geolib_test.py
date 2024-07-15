import unittest
from geolib import compute_destination_point

class TestGeolib(unittest.TestCase):
    def test_compute_destimation_point(self):
        # Arrange
        ALLOWED_DELTA = 0.000001

        """Should get the destination point to a given point, distance and bearing"""
        tc1 = {"lat": 52.518611, "lon": 13.408056, "dist": 15000, "bearing":180, 
               "expected_lat": 52.383712759112186, "expected_lon": 13.408056}
        tc2 = {"lat": 52.518611, "lon": 13.408056, "dist": 15000, "bearing":135, 
               "expected_lat": 52.42312025947117, "expected_lon": 13.56447370636139}
        tc3 = {"lat": 52.518611, "lon": 13.408056, "dist": 15000, "bearing":135, 
               "expected_lat": 52.42312025947117, "expected_lon": 13.56447370636139}

        """Should not exceed maxLon or fall below minLon"""
        tc4 = {"lat": 18.5075232, "lon": 73.8047121, "dist": 50000000, "bearing":0, 
               "expected_lat": 71.83167384063478, "expected_lon": -106.19528790000001}

        """Should leave longitude untouched if bearing is 0 or 180"""
        tc5 = {"lat": 18.5075232, "lon": 73.8047121, "dist": 500, "bearing":0, 
               "expected_lat": 18.512019808029596, "expected_lon": 73.8047121}
        tc6 = {"lat": 18.5075232, "lon": 73.8047121, "dist": 500, "bearing":180, 
               "expected_lat": 18.50302659197041, "expected_lon": 73.8047121}
        cases = [tc1, tc2, tc3, tc4, tc5, tc6]


        for tc in cases:
            # Action
            actual_lat, actual_lon = compute_destination_point(tc["lat"], tc["lon"], tc["dist"], tc["bearing"])
            
            # Assert
            self.assertAlmostEqual(actual_lat, tc["expected_lat"], delta=ALLOWED_DELTA)
            self.assertAlmostEqual(actual_lon, tc["expected_lon"], delta=ALLOWED_DELTA)