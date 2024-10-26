import socket

class Client:
    def __init__(self):
        self.HEADER = 64
        self.PORT = 5050
        self.FORMAT = "utf-8"
        self.DISCONNECT = 'disc'
        self.SERVER = "192.168.5.102"
        self.ADDR = (self.SERVER, self.PORT)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)
        print(self.client.recv(2048).decode(self.FORMAT))

    def send(self, msg) -> None:
        message = msg.encode(self.FORMAT)
        msg_length = len(msg)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
        print(self.client.recv(2048).decode(self.FORMAT))

    def close(self):
        self.send(self.DISCONNECT)
        self.client.close()