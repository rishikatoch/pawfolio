import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
)

# ==================================================
# Configuration
# ==================================================

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ==================================================
# Upload Folders
# ==================================================

BASE_UPLOAD_FOLDER = os.path.join(
    app.root_path,
    "static",
    "uploads",
)

PET_UPLOAD_FOLDER = os.path.join(
    BASE_UPLOAD_FOLDER,
    "pets",
)

os.makedirs(PET_UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = PET_UPLOAD_FOLDER

# ==================================================
# Extensions
# ==================================================

db = SQLAlchemy(app)

migrate = Migrate(app, db)

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"

login_manager.login_message = "Please login first."

# ==================================================
# Models
# ==================================================

from app import models  # noqa: E402

# ==================================================
# Login Loader
# ==================================================


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))


# ==================================================
# Routes
# ==================================================

from app.routes import auth  # noqa: E402,F401
from app.routes import main  # noqa: E402,F401
from app.routes import pets  # noqa: E402,F401
from app.routes import vaccinations  # noqa: E402,F401
