from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app: Flask = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///mydatabase.db"  # "mysql:" + os.env("DB_USERNAME") + os.env("DB_PASSWORD")  os.env("DB_LOCATION")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db: SQLAlchemy = SQLAlchemy(app)