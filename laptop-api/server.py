# import asyncio
# import websockets

# async def echo(websocket):
#     async for message in websocket:
#         await websocket.send(message)

# async def main():
#     async with websockets.serve(echo, "localhost", 8765):
#         await asyncio.Future()  # run forever

# asyncio.run(main())

import socket
import threading 

HEADER = 64
# the first message to the server has to be exactly 64 bytes

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) # auto gets ip
ADDR = (SERVER, PORT)

FORMAT = "utf-8"

DISCONNECT_MESSAGE = "disc"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION: {addr} connected]")
    conn.send("[CONNECTED]".encode(FORMAT))
    
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                conn.send("[DISCONNECTED]".encode(FORMAT))
            else:
                conn.send("[MSG RECV]".encode(FORMAT))
            
            print(f"[{addr} MSG: {msg}]")
            
    conn.close()
    print(f"[{addr} DISC]")

def start():
    server.listen()
    print(f"[SERVER ON {SERVER}]")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target= handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS: {threading.activeCount() - 1}]")
print("[STARTING...]")
start()