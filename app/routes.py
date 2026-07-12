from app import app, db
from app.models import Pet
from flask import Flask, render_template, request, redirect, url_for

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

@app.route("/delete/<int:id>")
def delete_pet(id):
    pet = Pet.query.get_or_404(id)
    db.session.delete(pet)
    db.session.commit()
    return redirect(url_for("home"))
