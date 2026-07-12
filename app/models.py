from app import db

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    breed = db.Column(db.String(100))
    gender = db.Column(db.String(20))
    age = db.Column(db.String(50))
    weight = db.Column(db.String(50))
    vaccination_status = db.Column(db.String(200))

    