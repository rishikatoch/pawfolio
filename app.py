from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pawfolio.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    breed = db.Column(db.String(100))
    gender = db.Column(db.String(20))
    age = db.Column(db.String(50))
    weight = db.Column(db.String(50))
    vaccination_status = db.Column(db.String(200))

@app.route("/")
def home():
    pets = Pet.query.all()
    return render_template("index.html", pets=pets)

@app.route("/add-pet", methods=["GET", "POST"])
def add_pet():
    if request.method == "POST":

        pet = Pet(
            name=request.form.get("pet_name"),
            breed=request.form.get("pet_breed"),
            gender=request.form.get("pet_gender"),
            age=request.form.get("pet_age"),
            weight=request.form.get("pet_weight"),
            vaccination_status=request.form.get("pet_vaccination_status")
        )

        db.session.add(pet)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("add_pet.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)