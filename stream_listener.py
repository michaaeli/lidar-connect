
import asyncio
import websockets

CONN_STR = "ws://localhost/seyondOdWs/stream?connect_id=6"

async def consume_stream():
    uri = "ws://localhost:3380"  # Replace with your WebSocket server URI
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print("Connected to the WebSocket server")
                while True:
                    message = await websocket.recv()
                    print(f"Received message: {message}")
                    # Process the message here
        except websockets.ConnectionClosed:
            print("Connection closed, retrying in 5 seconds...")
            await asyncio.sleep(5)  # Wait before retrying
        except Exception as e:
            print(f"An error occurred: {e}")
            await asyncio.sleep(5)  # Wait before retrying

if __name__ == "__main__":
    asyncio.run(consume_stream())
