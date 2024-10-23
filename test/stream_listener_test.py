from src.stream_listener import StreamListener
import threading
import unittest
import struct
import socket
import queue
import json
import time

TEST_DATA = '{"cmd":"2001","object_list":[{"height":"1.414932","length":"1.607635","length_type":"00","object_id":"1138815","object_timestamp":"467222","object_type":"2","speed":"0.144000","width":"0.613869","x":"-0.849668","y":"-2.124541","z":"8.138049","zone_id":"null"}],"server_ip":"0.0.0.0","sys_timestamp":1719250538539,"zone_list":[{"zone_id":"11388400","zone_name":"11388SOUTH00","zone_type":"1"}]}'  # noqa


class DataStreamServer:
    """
    Socket stream server. Sends data to socket client.

    """

    def __init__(self, host: str, port: int, package_len: int = 1024) -> None:
        self.host = host
        self.port = port
        self.max_conns = 5
        self.sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.package_len = package_len
        self.total_sent_bytes = 0

        self.conn = None

    def open_send_and_close(self, data) -> None:
        self.open_stream()
        self.send_data(data)
        self.close()

    def open_stream(self) -> None:
        self.sock.bind((self.host, self.port))
        self.sock.listen(self.max_conns)
        conn, addr = self.sock.accept()
        print("addr", addr)
        self.conn = conn

    def send_data(self, data) -> None:
        msg = self._data_to_packed_bytes(data)
        for chunk in msg:
            totalsent = 0
            while totalsent < len(chunk):
                sent = self.conn.send(chunk[totalsent:])
                if sent == 0:
                    raise RuntimeError("socket connection broken")
                totalsent += sent
                self.total_sent_bytes += sent

    def send_test_data_perpetually(self) -> None:
        x, y = 0, 0
        d = 1.5
        # msg = self.socket_stream_server._data_to_packed_bytes(bbb)[0]
        while True:
            t = int(time.time() * 1000)
            x += d
            y += d
            bbb = (
                """{"cmd":"2001","object_list":[{"height":"1.414932","length":"1.607635","length_type":"00","object_id":"1138815","object_timestamp":"467222","object_type":"2","speed":"0.144000","width":"0.613869","x":" """
                + str(x)
                + """ ","y":" """
                + str(y)
                + """ ","z":"8.138049","zone_id":"null"}],"server_ip":"0.0.0.0","sys_timestamp":" """
                + str(t)
                + """ ","zone_list":[{"zone_id":"11388400","zone_name":"11388SOUTH00","zone_type":"1"}]}"""
            )  # noqa
            self.send_data(bbb)
            print("sent msg")
            time.sleep(1)

    def _data_to_packed_bytes(self, data) -> list[bytes]:
        """Transforms data into list of byte packages"""
        # To JSON
        encoded = json.dumps(data)
        # To Bytes
        encoded_bytes = bytes(encoded, "UTF-8")
        # Cast to int every byte
        casted_bytes = [int(b) for b in encoded_bytes]
        # Prepare packages
        result = []
        i, j = 0, min(self.package_len, len(casted_bytes))
        while i < len(casted_bytes):
            chunk = casted_bytes[i:j]
            fstring = "!" + "I" * len(chunk)
            packed = struct.pack(fstring, *chunk)
            msg_len = len(packed)
            # +4 byte length for header and tail, +4 for message length
            packed = (
                struct.pack("!H", 0xFFAA)
                + struct.pack("!I", msg_len + 8)
                + packed
                + struct.pack("!H", 0xEEEE)
            )
            result.append(packed)
            i = j
            j = min(j + self.package_len, len(casted_bytes))

        return result

    def close(self) -> None:
        self.conn.shutdown(socket.SHUT_RDWR)
        self.sock.close()


PACKAGE_LEN = 1024
PORT = 3399


class TestStreamListener(unittest.TestCase):
    def setUp(self) -> None:
        self.host = "localhost"
        self.port = PORT
        self.q = queue.Queue()
        self.socket_stream_server = DataStreamServer(
            self.host, self.port, package_len=PACKAGE_LEN
        )

    def test_encode(self):
        # Arrange
        tc1 = {"msg": "Test message", "expected_len": 1}
        tc2 = {"msg": "T" * (PACKAGE_LEN + 1), "expected_len": 2}
        cases = [tc1, tc2]

        for tc in cases:
            # Act
            bbb = self.socket_stream_server._data_to_packed_bytes(tc["msg"])

            # Assert
            self.assertTrue(len(bbb) == tc["expected_len"])

    def test_send_data(self):
        # Arrange
        msg = "Test message"
        expected_number_of_sent_bytes = len(
            self.socket_stream_server._data_to_packed_bytes(msg)[0]
        )
        self.server_thread = threading.Thread(
            target=self.socket_stream_server.open_send_and_close, args=[msg]
        )

        # Act
        self.server_thread.start()
        time.sleep(1)
        self.listener = StreamListener(self.host, self.port, self.q)
        self.server_thread.join()
        self.listener.close()

        # Assert
        self.assertEqual(
            self.socket_stream_server.total_sent_bytes, expected_number_of_sent_bytes
        )

    def test_receive_data(self):
        # Arrange
        bbb = '{"cmd":"2001","object_list":[{"height":"1.414932","length":"1.607635","length_type":"00","object_id":"1138815","object_timestamp":"467222","object_type":"2","speed":"0.144000","width":"0.613869","x":"-0.849668","y":"-2.124541","z":"8.138049","zone_id":"null"}],"server_ip":"0.0.0.0","sys_timestamp":1719250538539,"zone_list":[{"zone_id":"11388400","zone_name":"11388SOUTH00","zone_type":"1"}]}'  # noqa
        msg = self.socket_stream_server._data_to_packed_bytes(bbb)[0]
        expected_number_of_sent_bytes = len(msg)
        self.server_thread = threading.Thread(
            target=self.socket_stream_server.open_send_and_close, args=[bbb]
        )

        # Act

        # Send
        self.server_thread.start()
        time.sleep(1)
        self.listener = StreamListener(self.host, self.port, self.q)
        self.client_thread = threading.Thread(target=self.listener.consume_stream)
        self.client_thread.start()
        self.server_thread.join()
        self.client_thread.join()

        # Receive & decode

        self.listener.close()

        # Assert
        self.assertEqual(
            self.socket_stream_server.total_sent_bytes, expected_number_of_sent_bytes
        )
        self.assertEqual(self.q.qsize(), 1)


if __name__ == "__main__":
    host = "localhost"
    port = PORT
    q = queue.Queue()
    socket_stream_server = DataStreamServer(host, port, package_len=PACKAGE_LEN)
    socket_stream_server.open_stream()
    try:
        socket_stream_server.send_test_data_perpetually()
    except:
        socket_stream_server.close()
