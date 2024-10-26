from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

app: Flask = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///mydatabase.db"  # "mysql:" + os.env("DB_USERNAME") + os.env("DB_PASSWORD")  os.env("DB_LOCATION")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db: SQLAlchemy = SQLAlchemy(app)