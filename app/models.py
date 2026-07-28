from datetime import date, datetime, time

from flask import current_app
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)

from app import db

# ==================================================
# User
# ==================================================


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False,
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash = db.Column(
        db.String(255),
        nullable=True,
    )

    google_id = db.Column(
        db.String(255),
        unique=True,
        nullable=True,
    )

    auth_provider = db.Column(
        db.String(20),
        nullable=False,
        default="local",
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    email_notifications = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
    )

    reminder_days = db.Column(
        db.Integer,
        nullable=False,
        default=7,
    )

    notification_time = db.Column(
        db.Time,
        nullable=False,
        default=time(9, 0),
    )

    timezone = db.Column(
        db.String(50),
        nullable=False,
        default="Asia/Kolkata",
    )

    pets = db.relationship(
        "Pet",
        backref="owner",
        lazy=True,
        cascade="all, delete-orphan",
    )

    # ==========================================
    # Password
    # ==========================================

    def set_password(self, password):
        self.password_hash = generate_password_hash(
            password,
        )

    def check_password(self, password):
        """
        Returns False for Google-only accounts.
        """

        if not self.password_hash:
            return False

        return check_password_hash(
            self.password_hash,
            password,
        )

    # ==========================================
    # Password Reset Token
    # ==========================================

    def get_reset_password_token(self):
        serializer = URLSafeTimedSerializer(
            current_app.config["SECRET_KEY"],
        )

        return serializer.dumps(
            self.id,
            salt="password-reset",
        )

    @staticmethod
    def verify_reset_password_token(
        token,
        expires_sec=3600,
    ):
        serializer = URLSafeTimedSerializer(
            current_app.config["SECRET_KEY"],
        )

        try:
            user_id = serializer.loads(
                token,
                salt="password-reset",
                max_age=expires_sec,
            )

        except Exception:
            return None

        return User.query.get(user_id)

    def __repr__(self):
        return (
            f"<User "
            f"id={self.id} "
            f"username='{self.username}' "
            f"email='{self.email}'>"
        )

    # ==================================================


# Pet
# ==================================================


class Pet(db.Model):
    __tablename__ = "pet"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.String(100),
        nullable=False,
    )

    breed = db.Column(
        db.String(100),
        nullable=True,
    )

    gender = db.Column(
        db.String(20),
        nullable=True,
    )

    age = db.Column(
        db.String(50),
        nullable=True,
    )

    birth_date = db.Column(
        db.Date,
        nullable=True,
    )

    weight = db.Column(
        db.Float,
        nullable=True,
    )

    vaccination_status = db.Column(
        db.String(200),
        nullable=True,
    )

    photo = db.Column(
        db.String(255),
        nullable=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    vaccinations = db.relationship(
        "Vaccination",
        backref="pet",
        lazy=True,
        cascade="all, delete-orphan",
    )

    dewormings = db.relationship(
        "Deworming",
        backref="pet",
        lazy=True,
        cascade="all, delete-orphan",
    )

    vet_visits = db.relationship(
        "VetVisit",
        backref="pet",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="desc(VetVisit.visit_date)",
    )

    # ==========================================
    # Age Helpers
    # ==========================================

    @property
    def age_display(self):

        if not self.birth_date:
            return self.age or "Unknown"

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

        if months == 0:
            return "Less than 1 month"

        if months < 12:
            return "1 month" if months == 1 else f"{months} months"

        years = months // 12

        remaining = months % 12

        if remaining == 0:
            return "1 year" if years == 1 else f"{years} years"

        if years == 1:
            return f"1 year {remaining} months"

        return f"{years} years {remaining} months"

    @property
    def age_in_months(self):

        if not self.birth_date:
            return None

        today = date.today()

        months = (
            (today.year - self.birth_date.year) * 12
            + today.month
            - self.birth_date.month
        )

        if today.day < self.birth_date.day:
            months -= 1

        return max(months, 0)

    @property
    def age_in_years(self):

        months = self.age_in_months

        if months is None:
            return None

        return round(months / 12, 1)

    # ==========================================
    # Life Stage
    # ==========================================

    @property
    def life_stage(self):

        months = self.age_in_months

        if months is None:
            return "Unknown"

        if months < 12:
            return "🐶 Puppy"

        if months < 84:
            return "🦮 Adult"

        return "🐕 Senior"

    # ==========================================
    # Birthday
    # ==========================================

    @property
    def next_birthday(self):

        if not self.birth_date:
            return None

        today = date.today()

        birthday = self.birth_date.replace(
            year=today.year,
        )

        if birthday < today:
            birthday = birthday.replace(
                year=today.year + 1,
            )

        return birthday

    @property
    def days_until_birthday(self):

        birthday = self.next_birthday

        if birthday is None:
            return None

        return (birthday - date.today()).days

    @property
    def birthday_today(self):

        if not self.birth_date:
            return False

        today = date.today()

        return today.month == self.birth_date.month and today.day == self.birth_date.day

    # ==========================================
    # Dashboard Helpers
    # ==========================================

    @property
    def overdue_vaccinations(self):

        today = date.today()

        return [
            vaccination
            for vaccination in self.vaccinations
            if vaccination.next_due < today
        ]

    @property
    def upcoming_vaccinations(self):

        today = date.today()

        return [
            vaccination
            for vaccination in self.vaccinations
            if 0 <= (vaccination.next_due - today).days <= 30
        ]

    def __repr__(self):

        return f"<Pet " f"id={self.id} " f"name='{self.name}'>"

    # ==================================================


# Vaccination
# ==================================================


class Vaccination(db.Model):
    __tablename__ = "vaccination"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    pet_id = db.Column(
        db.Integer,
        db.ForeignKey("pet.id"),
        nullable=False,
        index=True,
    )

    vaccine_name = db.Column(
        db.String(100),
        nullable=False,
    )

    date_given = db.Column(
        db.Date,
        nullable=False,
    )

    next_due = db.Column(
        db.Date,
        nullable=False,
    )

    veterinarian = db.Column(
        db.String(100),
        nullable=True,
    )

    notes = db.Column(
        db.Text,
        nullable=True,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # ==========================================
    # Helpers
    # ==========================================

    @property
    def is_overdue(self):

        return self.next_due < date.today()

    @property
    def is_due_today(self):

        return self.next_due == date.today()

    @property
    def days_until_due(self):

        return (self.next_due - date.today()).days

    @property
    def status(self):

        days = self.days_until_due

        if days < 0:
            return "Overdue"

        if days == 0:
            return "Due Today"

        if days <= 30:
            return "Due Soon"

        return "Up to Date"

    def __repr__(self):

        return f"<Vaccination " f"id={self.id} " f"vaccine='{self.vaccine_name}'>"


# ==================================================
# Deworming
# ==================================================


class Deworming(db.Model):
    __tablename__ = "deworming"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    pet_id = db.Column(
        db.Integer,
        db.ForeignKey("pet.id"),
        nullable=False,
        index=True,
    )

    medicine_name = db.Column(
        db.String(100),
        nullable=False,
    )

    date_given = db.Column(
        db.Date,
        nullable=False,
    )

    next_due = db.Column(
        db.Date,
        nullable=False,
    )

    schedule_used = db.Column(
        db.String(50),
        nullable=False,
    )

    age_at_deworming = db.Column(
        db.String(50),
        nullable=False,
    )

    veterinarian = db.Column(
        db.String(100),
        nullable=True,
    )

    notes = db.Column(
        db.Text,
        nullable=True,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    @property
    def is_overdue(self):

        return self.next_due < date.today()

    @property
    def days_until_due(self):

        return (self.next_due - date.today()).days

    def __repr__(self):

        return f"<Deworming " f"id={self.id} " f"medicine='{self.medicine_name}'>"


# ==================================================
# Vet Visit
# ==================================================


class VetVisit(db.Model):
    __tablename__ = "vet_visit"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    pet_id = db.Column(
        db.Integer,
        db.ForeignKey("pet.id"),
        nullable=False,
        index=True,
    )

    visit_date = db.Column(
        db.Date,
        nullable=False,
    )

    clinic_name = db.Column(
        db.String(150),
        nullable=False,
    )

    veterinarian = db.Column(
        db.String(150),
        nullable=False,
    )

    reason = db.Column(
        db.String(255),
        nullable=False,
    )

    diagnosis = db.Column(
        db.Text,
        nullable=True,
    )

    treatment = db.Column(
        db.Text,
        nullable=True,
    )

    prescription = db.Column(
        db.Text,
        nullable=True,
    )

    follow_up_date = db.Column(
        db.Date,
        nullable=True,
    )

    notes = db.Column(
        db.Text,
        nullable=True,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    @property
    def has_follow_up(self):

        return self.follow_up_date is not None

    @property
    def follow_up_overdue(self):

        if not self.follow_up_date:
            return False

        return self.follow_up_date < date.today()

    @property
    def days_until_follow_up(self):

        if not self.follow_up_date:
            return None

        return (self.follow_up_date - date.today()).days

    def __repr__(self):

        return f"<VetVisit " f"id={self.id} " f"pet_id={self.pet_id}>"

    # ==================================================


class ReminderLog(db.Model):
    __tablename__ = "reminder_logs"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False,
    )

    reminder_type = db.Column(
        db.String(50),
        nullable=False,
    )

    reference_id = db.Column(
        db.Integer,
        nullable=False,
    )

    reminder_date = db.Column(
        db.Date,
        nullable=False,
    )

    sent_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    user = db.relationship(
        "User",
        backref="reminder_logs",
    )


# Model Notes
# ==================================================
#
# Authentication Providers
#
# local      -> Email & Password
# google     -> Google OAuth
# github     -> GitHub OAuth (future)
# microsoft  -> Microsoft OAuth (future)
#
# The User model has been designed so that adding
# additional OAuth providers later requires only
# adding new login routes without changing the
# database schema.
#
# ==================================================
# End of File
# ==================================================
