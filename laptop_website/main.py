from config import app, db
from flask import request, send_file, jsonify
import os
from Meshroom_CLI import main as run_mesh


MESH_OUTPUT_FOLDER = "output"
IMAGE_FOLDER = "images"
OUTPUT_MESH_FILENAME = "texturedMesh.obj"

@app.route("/")
def home():
    return ""

@app.route("/api", methods=["POST"])
def scan():
    #user_id = request.form['user']
    #client = Client(server="192.168.2.201")
    #client.connect()

    #run_mesh()

    return send_file(f"{MESH_OUTPUT_FOLDER}{os.sep}{OUTPUT_MESH_FILENAME}", attachment_filename="object.obj", as_attachment=True)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)