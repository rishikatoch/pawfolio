from app import db


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(100))
    gender = db.Column(db.String(20))
    age = db.Column(db.String(50))
    weight = db.Column(db.Float)
    vaccination_status = db.Column(db.String(200))
    photo = db.Column(db.String(255))

    vaccinations = db.relationship(
        "Vaccination",
        backref="pet",
        lazy=True,
        cascade="all, delete-orphan"
    )


class Vaccination(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    pet_id = db.Column(
        db.Integer,
        db.ForeignKey("pet.id"),
        nullable=False
    )

    vaccine_name = db.Column(db.String(100), nullable=False)

    date_given = db.Column(db.String(50), nullable=False)

    next_due = db.Column(db.String(50), nullable=False)

    notes = db.Column(db.Text)

    veterinarian = db.Column(db.String(100))