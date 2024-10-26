import socket

class Client:
    def __init__(self, server: str):
        self.HEADER = 64
        self.PORT = 5050
        self.FORMAT = "utf-8"
        self.DISCONNECT = 'disc'
        self.SERVER = server
        self.ADDR = (self.SERVER, self.PORT)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)
        print(self.client.recv(2048).decode(self.FORMAT))

    def send(self, msg) -> None:
        message = msg.encode(self.FORMAT)
        msg_length = len(msg)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b'  ' * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
        print(self.client.recv(2048).decode(self.FORMAT))
    
    def send_file(self, filename):
        
        send_file = open(filename, "rb")
        data = send_file.read()
        msg_length = len(data)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b'  ' * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(data)


    def close(self):
        self.send(self.DISCONNECT)
        self.client.close()


'''
import socket
s = socket.socket()
s.connect(("localhost", 5000))
filetosend = open("img.png", "rb")
data = filetosend.read(1024)
while data:
    print("Sending...")
    s.send(data)
    data = filetosend.read(1024)
filetosend.close()
s.send(b"DONE")
print("Done Sending.")
print(s.recv(1024))
s.shutdown(2)
s.close()
'''