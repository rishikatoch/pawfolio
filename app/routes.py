from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user,
)

from app import app, db
from app.models import User, Pet, Vaccination
from app.forms import RegisterForm, LoginForm

from werkzeug.utils import secure_filename

import os

# ==========================
# Register
# ==========================


@app.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = RegisterForm()

    if form.validate_on_submit():

        existing_user = User.query.filter_by(email=form.email.data).first()

        if existing_user:

            flash("Email already registered.", "danger")

            return redirect(url_for("register"))

        user = User(
            username=form.username.data,
            email=form.email.data,
        )

        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully. Please login.", "success")

        return redirect(url_for("login"))

    return render_template(
        "register.html",
        form=form,
    )


# ==========================
# Login
# ==========================


@app.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):

            login_user(user)

            flash("Welcome back!", "success")

            return redirect(url_for("home"))

        flash("Invalid email or password.", "danger")

    return render_template(
        "login.html",
        form=form,
    )


# ==========================
# Logout
# ==========================


@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged out successfully.", "info")

    return redirect(url_for("login"))


# ==========================
# Home
# ==========================


@app.route("/")
@login_required
def home():

    pets = Pet.query.filter_by(user_id=current_user.id).all()

    total_pets = Pet.query.filter_by(user_id=current_user.id).count()

    total_vaccinations = (
        Vaccination.query.join(Pet).filter(Pet.user_id == current_user.id).count()
    )

    due_soon = 0

    return render_template(
        "index.html",
        pets=pets,
        total_pets=total_pets,
        total_vaccinations=total_vaccinations,
        due_soon=due_soon,
    )


# ==========================
# Pet Profile
# ==========================


@app.route("/pet/<int:id>")
@login_required
def pet_profile(id):

    pet = Pet.query.filter_by(id=id, user_id=current_user.id).first_or_404()

    return render_template(
        "pet_profile.html",
        pet=pet,
    )


# ==========================
# Add Pet
# ==========================


@app.route("/add-pet", methods=["GET", "POST"])
@login_required
def add_pet():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        breed = request.form.get("breed", "").strip()
        gender = request.form.get("gender", "").strip()
        age = request.form.get("age", "").strip()
        vaccination_status = request.form.get("vaccination_status", "").strip()
        weight = request.form.get("weight", "").strip()

        photo = request.files.get("photo")

        if not name:
            return render_template("add_pet.html", error="Pet name is required.")

        if not breed:
            return render_template("add_pet.html", error="Breed is required.")

        if not gender:
            return render_template("add_pet.html", error="Gender is required.")

        if not age:
            return render_template("add_pet.html", error="Age is required.")

        if not vaccination_status:
            return render_template(
                "add_pet.html", error="Vaccination status is required."
            )

        if weight == "":
            weight = None
        else:
            try:
                weight = float(weight)
            except ValueError:
                return render_template(
                    "add_pet.html", error="Weight must be a valid number."
                )

        filename = None

        if photo and photo.filename != "":

            filename = secure_filename(photo.filename)

            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        pet = Pet(
            name=name,
            breed=breed,
            gender=gender,
            age=age,
            weight=weight,
            vaccination_status=vaccination_status,
            photo=filename,
            user_id=current_user.id,
        )

        db.session.add(pet)
        db.session.commit()

        flash("Pet added successfully!", "success")

        return redirect(url_for("home"))

    return render_template("add_pet.html")


# ==========================
# Delete Pet
# ==========================


@app.route("/delete/<int:id>")
@login_required
def delete_pet(id):

    pet = Pet.query.filter_by(id=id, user_id=current_user.id).first_or_404()

    db.session.delete(pet)
    db.session.commit()

    flash("Pet deleted successfully.", "success")

    return redirect(url_for("home"))


# ==========================
# Edit Pet
# ==========================


@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_pet(id):

    pet = Pet.query.filter_by(id=id, user_id=current_user.id).first_or_404()

    if request.method == "POST":

        pet.name = request.form.get("name")
        pet.breed = request.form.get("breed")
        pet.gender = request.form.get("gender")
        pet.age = request.form.get("age")

        weight = request.form.get("weight")

        if weight:
            pet.weight = float(weight)
        else:
            pet.weight = None

        pet.vaccination_status = request.form.get("vaccination_status")

        photo = request.files.get("photo")

        if photo and photo.filename != "":

            filename = secure_filename(photo.filename)

            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            pet.photo = filename

        db.session.commit()

        flash("Pet updated successfully!", "success")

        return redirect(url_for("pet_profile", id=pet.id))

    return render_template(
        "edit_pet.html",
        pet=pet,
    )


# ==========================
# Add Vaccination
# ==========================


@app.route("/pet/<int:pet_id>/vaccination/add", methods=["GET", "POST"])
@login_required
def add_vaccination(pet_id):

    pet = Pet.query.filter_by(id=pet_id, user_id=current_user.id).first_or_404()

    if request.method == "POST":

        vaccination = Vaccination(
            pet_id=pet.id,
            vaccine_name=request.form.get("vaccine_name"),
            date_given=request.form.get("date_given"),
            next_due=request.form.get("next_due"),
            veterinarian=request.form.get("veterinarian"),
            notes=request.form.get("notes"),
        )

        db.session.add(vaccination)
        db.session.commit()

        flash("Vaccination added successfully!", "success")

        return redirect(url_for("pet_profile", id=pet.id))

    return render_template(
        "add_vaccination.html",
        pet=pet,
    )


# ==========================
# Delete Vaccination
# ==========================


@app.route("/vaccination/<int:id>/delete")
@login_required
def delete_vaccination(id):

    vaccination = (
        Vaccination.query.join(Pet)
        .filter(Vaccination.id == id, Pet.user_id == current_user.id)
        .first_or_404()
    )

    pet_id = vaccination.pet_id

    db.session.delete(vaccination)
    db.session.commit()

    flash("Vaccination deleted successfully!", "success")

    return redirect(url_for("pet_profile", id=pet_id))


# ==========================
# Edit Vaccination
# ==========================


@app.route("/vaccination/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_vaccination(id):

    vaccination = (
        Vaccination.query.join(Pet)
        .filter(Vaccination.id == id, Pet.user_id == current_user.id)
        .first_or_404()
    )

    if request.method == "POST":

        vaccination.vaccine_name = request.form.get("vaccine_name")

        vaccination.date_given = request.form.get("date_given")

        vaccination.next_due = request.form.get("next_due")

        vaccination.veterinarian = request.form.get("veterinarian")

        vaccination.notes = request.form.get("notes")

        db.session.commit()

        flash("Vaccination updated successfully!", "success")

        return redirect(url_for("pet_profile", id=vaccination.pet_id))

    return render_template(
        "edit_vaccination.html",
        vaccination=vaccination,
    )


# ==========================
# Health Check
# ==========================


@app.route("/health")
def health():
    return {
        "status": "healthy",
        "service": "pawfolio",
    }, 200
