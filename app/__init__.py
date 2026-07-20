import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")

# ==========================
# Secret Key
# ==========================

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# ==========================
# Upload Folder
# ==========================

UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ==========================
# Database
# ==========================

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

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

from app import models  # noqa: E402


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))


# ==========================
# Routes
# ==========================

from app import routes  # noqa: E402,F401
