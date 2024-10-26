import socket
import threading 
from Meshroom_CLI import main as run_mesh
import os

HEADER = 64
# the first message to the server has to be exactly 64 bytes

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) # auto gets ip
ADDR = (SERVER, PORT)

FORMAT = "utf-8"

DISCONNECT_MESSAGE = "disc"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

image_count = 1

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

            
            print(f"[{addr} MSG: {msg}]")
            if msg[:3] == "img":
                image_count = 1
            elif msg == "done":
                if image_count == 18:
                    run_mesh()
                    
            elif image_count <= 18:
                with open(f"images{os.sep}image{image_count}.jpg", "rb") as file:
                    file.write(msg)
                image_count += 1
                conn.send("[IMG RECV]".encode(FORMAT))
                continue
            conn.send("[MSG RECV]".encode(FORMAT))
            
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

'''
import socket
s = socket.socket()
s.bind(("localhost", 5000))
s.listen(1)
c,a = s.accept()
filetodown = open("img.png", "wb")
while True:
   print("Receiving....")
   data = c.recv(1024)
   if data == b"DONE":
           print("Done Receiving.")
           break
   filetodown.write(data)
filetodown.close()
c.send("Thank you for connecting.")
c.shutdown(2)
c.close()
s.close()
'''