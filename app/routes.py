from app import app, db
from app.models import Pet
from flask import Flask, render_template, request, redirect, url_for

@app.route("/")
def home():
    pets = Pet.query.all()
    print("PETS:", pets)
    return render_template("index.html", pets=pets)

@app.route("/add-pet", methods=["GET", "POST"])
def add_pet():
    if request.method == "POST":

        name = request.form.get("pet_name", "").strip()
        breed = request.form.get("pet_breed", "").strip()
        gender = request.form.get("pet_gender", "").strip()
        age = request.form.get("pet_age", "").strip()
        vaccination_status = request.form.get("pet_vaccination_status", "").strip()
        weight = request.form.get("pet_weight", "").strip()

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

        pet = Pet(
            name=name,
            breed=breed,
            gender=gender,
            age=age,
            weight=weight,
            vaccination_status=vaccination_status
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
