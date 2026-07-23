from datetime import date

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

    # Existing field (kept for compatibility)
    age = db.Column(db.String(50))

    # New field (this will replace "age" in the future)
    birth_date = db.Column(db.Date, nullable=True)

    weight = db.Column(db.Float)

    vaccination_status = db.Column(db.String(200))

    photo = db.Column(db.String(255))

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    vaccinations = db.relationship(
        "Vaccination", backref="pet", lazy=True, cascade="all, delete-orphan"
    )

    @property
    def age_display(self):
        """
        Returns:
        - 3 months
        - 8 months
        - 1 year
        - 2 years 4 months

        Falls back to the old 'age' field if birth_date
        hasn't been entered yet.
        """

        if not self.birth_date:
            return self.age if self.age else "Unknown"

        today = date.today()

        months = (
            (today.year - self.birth_date.year) * 12
            + today.month
            - self.birth_date.month
        )

        if today.day < self.birth_date.day:
            months -= 1

        if months < 0:
            return "Unknown"

        if months < 12:
            if months == 1:
                return "1 month"
            return f"{months} months"

        years = months // 12
        remaining_months = months % 12

        if remaining_months == 0:
            if years == 1:
                return "1 year"
            return f"{years} years"

        if years == 1:
            return f"1 year {remaining_months} months"

        return f"{years} years {remaining_months} months"

    @property
    def life_stage(self):
        """
        Returns:
        🐶 Puppy
        🦮 Adult
        🐕 Senior
        """

        if not self.birth_date:
            return "Unknown"

        today = date.today()

        months = (
            (today.year - self.birth_date.year) * 12
            + today.month
            - self.birth_date.month
        )

        if today.day < self.birth_date.day:
            months -= 1

        if months < 12:
            return "🐶 Puppy"

        if months < 84:
            return "🦮 Adult"

        return "🐕 Senior"

    @property
    def next_birthday(self):
        if not self.birth_date:
            return None

        today = date.today()

        birthday = self.birth_date.replace(year=today.year)

        if birthday < today:
            birthday = birthday.replace(year=today.year + 1)

        return birthday

    @property
    def days_until_birthday(self):
        if not self.next_birthday:
            return None

        return (self.next_birthday - date.today()).days

    @property
    def birthday_today(self):
        if not self.birth_date:
            return False

        today = date.today()

        return today.month == self.birth_date.month and today.day == self.birth_date.day


class Vaccination(db.Model):
    __tablename__ = "vaccination"

    id = db.Column(db.Integer, primary_key=True)

    pet_id = db.Column(db.Integer, db.ForeignKey("pet.id"), nullable=False)

    vaccine_name = db.Column(db.String(100), nullable=False)

    date_given = db.Column(db.Date, nullable=False)

    next_due = db.Column(db.Date, nullable=False)

    notes = db.Column(db.Text)

    veterinarian = db.Column(db.String(100))
