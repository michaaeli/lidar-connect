import unittest
import struct
import socket
import json

TEST_DATA = {
    "cmd": "2001",
    "object_list": [
            {"height": "1.414932",
             "length": "1.607635",
             "length_type": "00",
             "object_id": "1138815",
             "object_timestamp": "467022",
             "object_type": "2",
             "speed": "0.144000",
             "width": "0.613869",
             "x": "-0.849668",
             "y": "-2.122374",
             "z": "8.128756",
             "zone_id": "null"}
    ],
    "server_ip": "0.0.0.0",
    "sys_timestamp": 1719250538359,
    "zone_list": [
        {"zone_id": "11388400", "zone_name": "11388SOUTH00", "zone_type": "1"}
    ]
}


class DataStreamServer:
    def __init__(self) -> None:
        self.host = "localhost"
        self.port = 3380
        self.max_conns = 5
        self.sock: socket.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.packer: struct.Struct = struct.Struct("!H")

    def open_stream(self) -> None:
        self.sock.bind((self.host, self.port))
        self.sock.listen(self.max_conns)

    def send_data(self, data) -> None:
        msg = self._data_to_json_bytes(data)
        totalsent = 0
        while totalsent < len(msg):
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent += sent

    def _data_to_json_bytes(self, data) -> bytes:
        encoded = json.dumps(data)
        encoded_bytes = bytes(encoded, "UTF-8")

        casted_bytes = [int(b) for b in encoded_bytes]

        bytes_packed = self.packer.pack(*casted_bytes)

        return bytes_packed

    def close(self) -> None:
        self.sock.shutdown(1)
        self.sock.close()


class TestStreamListener(unittest.TestCase):
    def setUp(self) -> None:
        self.socket_stream_server = DataStreamServer()

    def tearDown(self) -> None:
        self.socket_stream_server.close()
        return super().tearDown()

    def test_successful_decode(self):
        # TODO
        b = self.socket_stream_server._data_to_json_bytes(3)
        self.assertTrue(True)


if __name__ == "__main__":
    b = struct.pack("!HHHHHHHH", *b'stringgg')
    print(b)
