from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="templates", static_folder="static")

app.config["SQLALCHEMY_DATABASE_URI"] ="postgresql://pawfolio:password@postgres:5432/pawfolio"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from app import models
from app import routes
