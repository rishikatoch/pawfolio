import os

from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
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
# Google OAuth
# ==================================================

app.config["GOOGLE_CLIENT_ID"] = os.getenv("GOOGLE_CLIENT_ID")

app.config["GOOGLE_CLIENT_SECRET"] = os.getenv("GOOGLE_CLIENT_SECRET")

# ==================================================
# Mail Configuration
# ==================================================

app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")

app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))

app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "True").lower() == "true"

app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL", "False").lower() == "true"

app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")

app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

# ==================================================
# Upload Folder
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

os.makedirs(
    PET_UPLOAD_FOLDER,
    exist_ok=True,
)

app.config["UPLOAD_FOLDER"] = PET_UPLOAD_FOLDER

# ==================================================
# Extensions
# ==================================================

db = SQLAlchemy(app)

migrate = Migrate(app, db)

mail = Mail(app)

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"

login_manager.login_message = "Please login first."

oauth = OAuth(app)
# ==================================================
# Google OAuth Registration
# ==================================================

google = oauth.register(
    name="google",
    client_id=app.config["GOOGLE_CLIENT_ID"],
    client_secret=app.config["GOOGLE_CLIENT_SECRET"],
    server_metadata_url=(
        "https://accounts.google.com/" ".well-known/openid-configuration"
    ),
    client_kwargs={
        "scope": "openid email profile",
    },
)

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
from app.routes import deworming  # noqa: E402,F401
from app.routes import main  # noqa: E402,F401
from app.routes import pets  # noqa: E402,F401
from app.routes import vaccinations  # noqa: E402,F401
from app.routes import vet_visit  # noqa: E402,F401
