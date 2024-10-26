from config import app, db
from flask import request, send_file
import RPi.GPIO as GPIO
from picamera2 import Picamera2, Preview
import os
from PIL import Image
from client import Client

picam2 = Picamera2()

@app.route("/")
def home():
    return ""

@app.route("/on", methods=["GET", "POST"])
def on():
    GPIO.output(8, 1)
    return "on"

@app.route("/off", methods=["GET", "POST"])
def off():
    GPIO.output(8, 0)
    return "off"

@app.route("/run-scan", methods=["POST"])
def scan():
    # Activate Turn Table
    images = []
    for i in range(1, 6):
        picam2.start_and_capture_file(f"{i}.jpg")
        images.append(Image.open(f"{i}.jpg"))
        images[-1].tobytes("xbm", "rgb")

    picam2.stop()
    client = Client(server="192.168.2.201")
    send_message = ""
    for image in images:
        send_message += f"-{image}"
        
    client.send("img" + send_message)
    

if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(8, GPIO.OUT)
    with app.app_context():
        db.create_all()

    app.run(debug=True)