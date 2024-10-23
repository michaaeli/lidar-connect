from src.data.detected_objects import detected_objects_from_json
# from data.detected_objects import detected_objects_from_json
import datetime
import logging
import socket
import struct
import queue
import json
import time
import sys


BUFFER_SIZE = 1024


logger = logging.getLogger(__name__)


class StreamListener:
    def __init__(self, host: str, port: int, result_q: queue.Queue) -> None:
        self.host = host
        self.port = port
        self.result_q = result_q
        self.buf_size = BUFFER_SIZE

        # connect to the stream
        self.socket_client: socket.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
        self.socket_client.connect((host, port))

    def close(self) -> None:
        """Executes graceful stop of connection consumption"""
        # TODO test
        self.socket_client.shutdown(1)
        logger.error("Sent shutdown signal to the socket")
        # Close connection
        self.socket_client.close()
        logger.error("Closed the socket")

    def wrapped_consume(self) -> None:
        try:
            self.consume_stream()
        except Exception as e:
            logger.error("wrapped_consume",e)
            self.close()

    def consume_stream(self) -> None:
        logger.info("StreamListener started consuming")
        self.buffer = b""
        while True:  # TODO maybe add stop signal
            # Receive data from socket
            try:
                response = self.socket_client.recv(self.buf_size)
            except Exception as e:
                # logger.error("consume_stream",e)
                logger.error("consume_stream")
                return

            # Handle exit conditions
            if not response:  # TODO think
                break

            # Append received data to the buffer
            self.buffer += response

            # Decode as many full messages as availabe in buffer
            messages_list = self.__decode_buffer()

            # Repack all detected objects from all messages
            for msg in messages_list:
                objects = detected_objects_from_json(msg)
                # Push detected objects to result queue
                for obj in objects:
                    self.result_q.put(obj)

        logger.info("StreamListener stopped consuming")

    def __decode_buffer(self) -> list[object]:
        messages = []
        # Decode as many full messages as availabe in buffer
        while True:
            # Process currently available data
            if len(self.buffer) < 8:
                break
            header = struct.unpack("!H", self.buffer[0:2])[0]
            if header != 0xFFAA:
                print("Invalid packet header")
                break

            message_length = struct.unpack("!I", self.buffer[2:6])[0]
            if len(self.buffer) < message_length:
                break  # wait for more data

            tail = struct.unpack("!H", self.buffer[message_length-2:message_length])[0]  # fmt: skip
            if tail != 0xEEEE:
                print("Invalid tail")
                break
            message = self.buffer[6:message_length-2]  # fmt: skip
            parsed = json.loads(message)
            # parsed = json.loads(parsed) 

            # Write detected message
            messages.append(parsed)

            # Update buffer
            self.buffer = self.buffer[message_length:]
        return messages

    async def __write_stream_to_file(self) -> None:
        """For debug"""
        buffer = b""
        while True:
            # Receive data from socket
            response = self.socket_client.recv(self.buf_size)

            # Handle exit conditions
            if not response:
                break

            # Append received data to the buffer
            buffer += response

            current_timestamp1 = time.time()
            dt1 = datetime.datetime.fromtimestamp(current_timestamp1)

            # Decode as many full messages as availabe in buffer
            while True:
                # Process currently available data
                if len(buffer) < 8:
                    break
                header = struct.unpack("!H", buffer[0:2])[0]
                if header != 0xFFAA:
                    print("Invalid packet header")
                    break

                message_length = struct.unpack("!I", buffer[2:6])[0]
                if len(buffer) < message_length:
                    break  # wait for more data

                tail = struct.unpack("!H", buffer[message_length-2:message_length])[  # fmt: skip
                    0
                ]
                if tail != 0xEEEE:
                    print("Invalid tail")
                    break
                message = buffer[6:message_length-2]  # fmt: skip
                parsed = json.loads(message)

                # Write detected objects
                if len(parsed["object_list"]) > 0:
                    current_timestamp = time.time()
                    dt = datetime.datetime.fromtimestamp(current_timestamp)
                    with open("example.txt", "a") as file:
                        file.write("\n")
                        file.write(f"Timestamp: {dt} , {current_timestamp}")
                        file.write("\n")
                        file.write(f"{message}")
                        file.write("\n")
                        file.write("--------------------------------")

                # Update buffer
                buffer = buffer[message_length:]

            sys.stdout.write("\r" + str(dt1))
            sys.stdout.flush()  # Ensure it gets displayed
            # print(text)  # Output text value

        self.socket_client.close()


# if __name__ == "__main__":
#     q = queue.Queue()
#     sl = StreamListener("127.0.0.1", 3380, q)
#     asyncio.run(sl.__write_stream_to_file())
