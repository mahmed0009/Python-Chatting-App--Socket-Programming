import asyncio
import websockets

clients = {}  # {websocket: username}


async def broadcast(message, sender_ws=None):
    for ws in clients:
        if ws != sender_ws:
            try:
                await ws.send(message)
            except:
                pass


async def handle_client(websocket):
    try:
        username = await websocket.recv()
        clients[websocket] = username
        print(f"[NEW CONNECTION] {username} connected")

        await broadcast(f"{username} joined the chat!", websocket)

        async for msg in websocket:
            full_msg = f"{username}: {msg}"
            print(full_msg)
            await broadcast(full_msg, websocket)

    except websockets.ConnectionClosed:
        pass
    finally:
        if websocket in clients:
            left_username = clients[websocket]
            print(f"{left_username} disconnected")
            del clients[websocket]
            await broadcast(f"{left_username} left the chat!")

async def main():
    async with websockets.serve(handle_client, "localhost", 6789):
        print("WebSocket server running on ws://localhost:6789")
        await asyncio.Future()  # run forever

asyncio.run(main())