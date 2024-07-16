import asyncio
import socket
import struct
import json
import time
import datetime
import sys
import queue


SERVER_HOST = '127.0.0.1'
SERVER_PORT = 3380


class StreamListener:
    def __init__(self, host, port, q:queue.Queue) -> None:
        self.host = host
        self.port = port
        self.queue = q

        # connect to the stream
        self.socket_client:socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client.connect((host, port))

    def close(self) -> None:
        """Executes graceful stop of connection consumption"""
        # TODO 
        # Close connection
        self.socket_client.close()


    async def consume_stream(self) -> None:
        pass


    async def write_stream_to_file(self) -> None:
        """For debug"""
        # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # client_socket.connect((SERVER_HOST, SERVER_PORT))
        buffer = b''
        while True:
            response = self.socket_client.recv(1024)
            #print("Received:", response.decode())
            if not response:
                break
            buffer += response
            # text = ''.join(chr(byte) for byte in response)
            current_timestamp1 = time.time()
            dt1 = datetime.datetime.fromtimestamp(current_timestamp1)
            while True:
                if (len(buffer) < 8):
                    break
                header = struct.unpack('!H', buffer[0:2])[0]
                if (header != 0xFFAA):
                    print("Invalid packet header")
                    break

                message_length = struct.unpack('!I', buffer[2:6])[0]
                if (len(buffer) < message_length):
                    break  # wait for more data

                tail = struct.unpack('!H', buffer[message_length-2:message_length])[0]
                if tail != 0xEEEE:
                    print ("Invalid tail")
                    break
                message = buffer[6:message_length-2]
                parsed = json.loads(message)

                # Write detected objects
                if len(parsed["object_list"]) > 0:
                    current_timestamp = time.time()
                    dt = datetime.datetime.fromtimestamp(current_timestamp)
                    with open('example.txt', 'a') as file:
                        file.write("\n")
                        file.write (f"Timestamp: {dt} , {current_timestamp}")
                        file.write("\n")
                        file.write(f"{message}")
                        file.write("\n")
                        file.write("--------------------------------")

                buffer = buffer[message_length:]

            sys.stdout.write("\r" + str(dt1))
            sys.stdout.flush()  # Ensure it gets displayed
            #print(text)  # Output text value

        self.socket_client.close()

if __name__ == "__main__":
    q = queue.Queue()
    sl = StreamListener(SERVER_HOST, SERVER_PORT, q)
    asyncio.run(sl.write_stream_to_file())
