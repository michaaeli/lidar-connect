import socket
import struct
import json
import time
import datetime
import sys


SERVER_HOST = '127.0.0.1'
SERVER_PORT = 3380

def format_json(json_string):
    try:
        # Parse the JSON string into a Python dictionary
        json_data = json.loads(json_string)
        # Convert the Python dictionary back to a JSON string with indentation
        formatted_json = json.dumps(json_data, indent=4)
        return formatted_json
    except json.JSONDecodeError:
        # Handle the case where the input string is not valid JSON
        return "Invalid JSON provided."
    
def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((SERVER_HOST, SERVER_PORT))
    buffer = b''
    while True:
        response = client_socket.recv(1024)
        #print("Received:", response.decode())
        if not response:
            break
        buffer += response
        text = ''.join(chr(byte) for byte in response)
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
            formated_str = format_json(message)
            current_timestamp = time.time()
            dt = datetime.datetime.fromtimestamp(current_timestamp)
            with open('example.txt', 'a') as file:
                file.write("\n")
                file.write (f"Timestamp: {dt} , {current_timestamp}")
                file.write("\n")
                file.write(f"{message}")
                file.write("\n")
                file.write("--------------------------------")
            #print (f"Message = {formated_str}")
            #print ("\n\n\n\n\n\n\n")
            buffer = buffer[message_length:]
        sys.stdout.write("\r" + str(dt1))
        sys.stdout.flush()  # Ensure it gets displayed
        #print(text)  # Output text value

    client_socket.close()

if __name__ == '__main__':
    main()
