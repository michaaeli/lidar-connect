import unittest
import json
from src.data.detected_objects import detected_objects_from_json, convert_system_timestamp_to_datetime


class TestRepack(unittest.TestCase):
    def test_repack_message(self):
        # Arrange
        bbb = b'{"cmd":"2001","object_list":[{"height":"1.414932","length":"1.607635","length_type":"00","object_id":"1138815","object_timestamp":"467222","object_type":"2","speed":"0.144000","width":"0.613869","x":"-0.849668","y":"-2.124541","z":"8.138049","zone_id":"null"}],"server_ip":"0.0.0.0","sys_timestamp":1719250538539,"zone_list":[{"zone_id":"11388400","zone_name":"11388SOUTH00","zone_type":"1"}]}'
        parsed_json = json.loads(bbb)
        time = convert_system_timestamp_to_datetime(1719250538539)
        expected_vals = {"height": 1.414932, "length": 1.607635, "id": 1138815,
                         "object_type": 2, "speed": 0.144000, "width": 0.613869, "x": -0.849668, "y": -2.124541, "z": 8.138049, "time": time}

        # Act
        objects = detected_objects_from_json(parsed_json)

        # Assert
        self.assertEqual(len(objects), 1)
        obj = objects[0]
        for field in expected_vals:
            expected_value = expected_vals[field]
            actual_value = getattr(obj, field)
            self.assertEqual(actual_value, expected_value)


if __name__ == "__main__":
    unittest.main()