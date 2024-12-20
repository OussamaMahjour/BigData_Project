import asyncio
import websockets
import json


def process_transaction(transaction):
    """Process the incoming transaction data."""
    print("Received transaction:", transaction)
    # Add your logic here to process the transaction (e.g., save to database, analyze, etc.)


async def connect_to_mempool():
    url = "wss://blockstream.info/api/v0/mempool/tx"

    try:
        async with websockets.connect(url) as websocket:
            print("Connected to Blockstream mempool WebSocket!")

            while True:
                try:
                    message = await websocket.recv()
                    # Decode the transaction data
                    transaction = json.loads(message)
                    process_transaction(transaction)
                except websockets.exceptions.ConnectionClosed as e:
                    print(f"Connection closed: {e}")
                    break
                except json.JSONDecodeError as e:
                    print(f"Failed to decode JSON: {e}")
    except Exception as e:
        print(f"Error connecting to WebSocket: {e}")

if __name__ == "__main__":
    asyncio.run(connect_to_mempool())
