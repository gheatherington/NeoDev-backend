from config import app, db
import RPi.GPIO as GPIO

@app.route("/")
def home():
    return ""

@app.route("/on", methods=["GET", "POST"])
def on():
    GPIO.output(8, 1)

@app.route("/off", methods=["GET", "POST"])
def off():
    GPIO.output(8, 0)

if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(8, GPIO.OUT)
    with app.app_context():
        db.create_all()

    app.run(debug=True)