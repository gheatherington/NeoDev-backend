# import socket

# class Client:
#     def __init__(self):
#         self.HEADER = 64
#         self.PORT = 5050
#         self.FORMAT = "utf-8"
#         self.DISCONNECT = 'disc'
#         self.SERVER = "192.168.5.102"
#         self.ADDR = (self.SERVER, self.PORT)
#         self.images = []

#         self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#     def recv(self, msg) -> None:
#         self.client.connect(self.ADDR)
#         print(self.client.recv(2048).decode(self.FORMAT))
#         message = msg.encode(self.FORMAT)
#         msg_length = len(msg)
#         send_length = str(msg_length).encode(self.FORMAT)
#         send_length += b' ' * (self.HEADER - len(send_length))
#         self.client.send(send_length)
#         self.client.send(message)
#         print(self.client.recv(2048).decode(self.FORMAT))

#     def close(self):
#         self.send(self.DISCONNECT)
#         self.client.close()

import socket
import os

class Client:
    def __init__(self):
        self.HEADER = 2048
        self.PORT = 5050
        self.FORMAT = "utf-8"
        self.DISCONNECT = 'disc'
        self.SERVER = "192.168.5.102"
        self.ADDR = (self.SERVER, self.PORT)
        self.IMAGE_FOLDER = "images"  # Folder to store received images
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        
        # Ensure the folder exists to store images
        os.makedirs(self.IMAGE_FOLDER, exist_ok=True)

    def connect(self):
        self.client.connect(self.ADDR)
        print(self.client.recv(2048).decode(self.FORMAT))  # Print server welcome message
        client.receive_images()

    def receive_images(self, image_count=18):
        for i in range(1, image_count + 1):
            # Receive the length of the incoming image data (64-byte header)
            img_length = int(self.client.recv(self.HEADER).decode(self.FORMAT).strip())
            
            # Receive the image data in chunks until fully received
            img_data = self.client.recv(img_length)

            # Save the image to the specified folder
            image_path = os.path.join(self.IMAGE_FOLDER, f"image{i}.jpg")
            with open(image_path, "wb") as img_file:
                img_file.write(img_data)
            
            print(f"[RECEIVED] Image {i} saved as {image_path}")


# Usage
client = Client()
client.connect()
