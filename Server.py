import asyncio
import websockets

clients = {}  # {websocket: username}
last_client_time = None  # Time when last client connected

async def broadcast(message):
    for ws in list(clients):
        try:
            await ws.send(message)
        except:
            pass

async def disconnect_all_clients():
    for ws in list(clients):
        try:
            await ws.close()
        except:
            pass
    clients.clear()
    print("[SERVER] Server disconnected due to inactivity.")

async def monitor_inactivity():
    global last_client_time
    while True:
        await asyncio.sleep(5)  # Check every 5 seconds
        if last_client_time:
            elapsed = asyncio.get_event_loop().time() - last_client_time
            if elapsed > 10:  
                await disconnect_all_clients()
                last_client_time = None

async def handle_client(websocket):
    global last_client_time
    try:
        username = await websocket.recv()
        clients[websocket] = username
        last_client_time = asyncio.get_event_loop().time()  # Reset timer on new client

        print(f"[NEW CONNECTION] {username} connected")
        await broadcast(f"{username} joined the chat!")

        async for msg in websocket:
            full_msg = f"{username}: {msg}"
            print(full_msg)
            await broadcast(full_msg)

    except websockets.ConnectionClosed:
        pass
    finally:
        if websocket in clients:
            left_username = clients[websocket]
            print(f"{left_username} disconnected")
            del clients[websocket]
            await broadcast(f"{left_username} left the chat!")

async def main():
    server = websockets.serve(handle_client, "localhost", 6789)
    print("WebSocket server running on ws://localhost:6789")
    
    await asyncio.gather(
        server,
        monitor_inactivity()
    )

asyncio.run(main())
