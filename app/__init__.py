import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__, template_folder="templates", static_folder="static")

# ==========================
# Secret Key
# ==========================

app.config["SECRET_KEY"] = "change-this-to-a-random-secret-key"

# ==========================
# Upload Folder
# ==========================

UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ==========================
# Database
# ==========================

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://pawfolio:password@postgres:5432/pawfolio"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ==========================
# Login Manager
# ==========================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"

login_manager.login_message = "Please login first."

# ==========================
# Import Models
# ==========================

from app import models


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))


# ==========================
# Routes
# ==========================

from app import routes
