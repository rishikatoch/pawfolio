from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Pet

from werkzeug.utils import secure_filename
import os

@app.route("/")
def home():
    pets = Pet.query.all()
    print("PETS:", pets)
    return render_template("index.html", pets=pets)

@app.route("/pet/<int:id>")
def pet_profile(id):
    pet = Pet.query.get_or_404(id)
    return render_template("pet_profile.html", pet=pet)


@app.route("/add-pet", methods=["GET", "POST"])
def add_pet():
    if request.method == "POST":

        name = request.form.get("pet_name", "").strip()
        breed = request.form.get("pet_breed", "").strip()
        gender = request.form.get("pet_gender", "").strip()
        age = request.form.get("pet_age", "").strip()
        vaccination_status = request.form.get("pet_vaccination_status", "").strip()
        weight = request.form.get("pet_weight", "").strip()
        photo = request.files.get("pet_photo")

        if not name:
            return render_template("add_pet.html", error="Pet name is required.")

        if not breed:
            return render_template("add_pet.html", error="Breed is required.")

        if not gender:
            return render_template("add_pet.html", error="Gender is required.")

        if not age:
            return render_template("add_pet.html", error="Age is required.")

        if not vaccination_status:
            return render_template("add_pet.html", error="Vaccination status is required.")

        if weight == "":
            weight = None
        else:
            try:
                weight = float(weight)
            except ValueError:
                return render_template(
                    "add_pet.html",
                    error="Weight must be a valid number."
                )

            print("UPLOAD_FOLDER =", app.config["UPLOAD_FOLDER"])
            print("photo =", photo)

        filename = None

        if photo and photo.filename:
            filename = secure_filename(photo.filename)
            photo.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

        pet = Pet(
            name=name,
            breed=breed,
            gender=gender,
            age=age,
            weight=weight,
            vaccination_status=vaccination_status,
            photo=filename
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

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_pet(id):
    pet = Pet.query.get_or_404(id)

    if request.method == "POST":
        pet.name = request.form.get("pet_name")
        pet.breed = request.form.get("pet_breed")
        pet.gender = request.form.get("pet_gender")
        pet.age = request.form.get("pet_age")

        weight = request.form.get("pet_weight")

        if weight:
            pet.weight = float(weight)
        else:
            pet.weight = None

        pet.vaccination_status = request.form.get("pet_vaccination_status")

        db.session.commit()

        return redirect(url_for("home"))

    return render_template("edit_pet.html", pet=pet)
