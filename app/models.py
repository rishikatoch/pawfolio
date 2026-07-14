from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    pets = db.relationship(
        "Pet", backref="owner", lazy=True, cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Pet(db.Model):
    __tablename__ = "pet"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    breed = db.Column(db.String(100))

    gender = db.Column(db.String(20))

    age = db.Column(db.String(50))

    weight = db.Column(db.Float)

    vaccination_status = db.Column(db.String(200))

    photo = db.Column(db.String(255))

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    vaccinations = db.relationship(
        "Vaccination", backref="pet", lazy=True, cascade="all, delete-orphan"
    )


class Vaccination(db.Model):
    __tablename__ = "vaccination"

    id = db.Column(db.Integer, primary_key=True)

    pet_id = db.Column(db.Integer, db.ForeignKey("pet.id"), nullable=False)

    vaccine_name = db.Column(db.String(100), nullable=False)

    date_given = db.Column(db.String(50), nullable=False)

    next_due = db.Column(db.String(50), nullable=False)

    notes = db.Column(db.Text)

    veterinarian = db.Column(db.String(100))
