import asyncio
import websockets
import os

clients = set()

async def handle_client(websocket, path):
    clients.add(websocket)
    try:
        async for message in websocket:
            # Broadcast message to all clients
            await asyncio.wait([client.send(message) for client in clients if client != websocket])
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        clients.remove(websocket)

PORT = int(os.environ.get("PORT", 5000))
start_server = websockets.serve(handle_client, "0.0.0.0", PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
