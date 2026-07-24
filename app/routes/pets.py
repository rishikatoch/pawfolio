from datetime import date
import os
import uuid

from flask import (
    flash,
    redirect,
    render_template,
    request,
    url_for,
    current_app,
)
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from app import app, db
from app.models import Pet

# ==========================================================
# Configuration
# ==========================================================

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "gif",
    "webp",
}


# ==========================================================
# Helper Functions
# ==========================================================


def allowed_file(filename):
    """
    Check whether uploaded file extension is allowed.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_pet_photo(photo):
    """
    Save uploaded image using UUID filename.

    Returns:
        filename (str) on success
        None on failure
    """

    if not photo:
        return None

    if photo.filename == "":
        return None

    if not allowed_file(photo.filename):
        return None

    extension = secure_filename(photo.filename).rsplit(".", 1)[1].lower()

    filename = f"{uuid.uuid4().hex}.{extension}"

    upload_folder = current_app.config["UPLOAD_FOLDER"]

    os.makedirs(upload_folder, exist_ok=True)

    try:

        photo.save(os.path.join(upload_folder, filename))

        return filename

    except Exception:

        return None


def delete_pet_photo(filename):
    """
    Delete pet image from disk safely.
    """

    if not filename:
        return

    path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        filename,
    )

    try:

        if os.path.exists(path):
            os.remove(path)

    except Exception:
        pass


# ==========================================================
# Pet Profile
# ==========================================================


@app.route("/pet/<int:pet_id>")
@login_required
def pet_profile(pet_id):

    pet = Pet.query.filter_by(
        id=pet_id,
        user_id=current_user.id,
    ).first_or_404()

    vaccinations = pet.vaccinations if hasattr(pet, "vaccinations") else []
    dewormings = pet.dewormings if hasattr(pet, "dewormings") else []

    return render_template(
        "pet_profile.html",
        pet=pet,
        vaccinations=vaccinations,
        dewormings=dewormings,
        today=date.today(),
    )


# ==========================================================
# Add Pet
# ==========================================================


@app.route("/add_pet", methods=["GET", "POST"])
@login_required
def add_pet():

    if request.method == "POST":

        name = request.form.get("name", "").strip()

        breed = request.form.get("breed", "").strip()

        gender = request.form.get("gender", "").strip()

        birth_date = request.form.get("birth_date", "").strip()

        weight = request.form.get("weight", "").strip()

        vaccination_status = request.form.get(
            "vaccination_status",
            "",
        ).strip()

        # ------------------------------------------
        # Validation
        # ------------------------------------------

        if not name:

            return render_template(
                "add_pet.html",
                error="Pet name is required.",
                now=date.today(),
            )

        if not breed:

            return render_template(
                "add_pet.html",
                error="Breed is required.",
                now=date.today(),
            )

        if gender not in [
            "Male",
            "Female",
        ]:

            return render_template(
                "add_pet.html",
                error="Invalid gender selected.",
                now=date.today(),
            )

        parsed_birth_date = None

        if birth_date:

            try:

                parsed_birth_date = date.fromisoformat(birth_date)

                if parsed_birth_date > date.today():

                    return render_template(
                        "add_pet.html",
                        error="Birth date cannot be in the future.",
                        now=date.today(),
                    )

            except ValueError:

                return render_template(
                    "add_pet.html",
                    error="Invalid birth date.",
                    now=date.today(),
                )

        parsed_weight = None

        if weight:

            try:

                parsed_weight = float(weight)

                if parsed_weight <= 0:

                    return render_template(
                        "add_pet.html",
                        error="Weight must be greater than zero.",
                        now=date.today(),
                    )

            except ValueError:

                return render_template(
                    "add_pet.html",
                    error="Invalid weight.",
                    now=date.today(),
                )

        photo = request.files.get("photo")

        filename = None

        if photo and photo.filename:

            if not allowed_file(photo.filename):

                return render_template(
                    "add_pet.html",
                    error="Only JPG, JPEG, PNG, GIF and WEBP images are allowed.",
                    now=date.today(),
                )

            filename = save_pet_photo(photo)

            if filename is None:

                return render_template(
                    "add_pet.html",
                    error="Unable to save uploaded image.",
                    now=date.today(),
                )

        # ------------------------------------------
        # Create Pet
        # ------------------------------------------

        pet = Pet(
            user_id=current_user.id,
            name=name,
            breed=breed,
            gender=gender,
            birth_date=parsed_birth_date,
            weight=parsed_weight,
            vaccination_status=vaccination_status,
            photo=filename,
        )

        try:

            db.session.add(pet)
            db.session.commit()

        except Exception:

            db.session.rollback()

            if filename:
                delete_pet_photo(filename)

            return render_template(
                "add_pet.html",
                error="Unable to save pet. Please try again.",
                now=date.today(),
            )

        flash(
            "Pet added successfully!",
            "success",
        )

        return redirect(
            url_for(
                "pet_profile",
                pet_id=pet.id,
            )
        )

    return render_template(
        "add_pet.html",
        now=date.today(),
    )


# ==========================================================
# Edit Pet
# ==========================================================


@app.route("/edit_pet/<int:pet_id>", methods=["GET", "POST"])
@login_required
def edit_pet(pet_id):

    pet = Pet.query.filter_by(
        id=pet_id,
        user_id=current_user.id,
    ).first_or_404()

    if request.method == "POST":

        name = request.form.get("name", "").strip()

        breed = request.form.get("breed", "").strip()

        gender = request.form.get("gender", "").strip()

        birth_date = request.form.get("birth_date", "").strip()

        weight = request.form.get("weight", "").strip()

        vaccination_status = request.form.get(
            "vaccination_status",
            "",
        ).strip()

        # ------------------------------------------
        # Validation
        # ------------------------------------------

        if not name:

            flash(
                "Pet name is required.",
                "danger",
            )

            return redirect(
                url_for(
                    "edit_pet",
                    pet_id=pet.id,
                )
            )

        if not breed:

            flash(
                "Breed is required.",
                "danger",
            )

            return redirect(
                url_for(
                    "edit_pet",
                    pet_id=pet.id,
                )
            )

        if gender not in (
            "Male",
            "Female",
        ):

            flash(
                "Invalid gender selected.",
                "danger",
            )

            return redirect(
                url_for(
                    "edit_pet",
                    pet_id=pet.id,
                )
            )

        parsed_birth_date = None

        if birth_date:

            try:

                parsed_birth_date = date.fromisoformat(birth_date)

                if parsed_birth_date > date.today():

                    flash(
                        "Birth date cannot be in the future.",
                        "danger",
                    )

                    return redirect(
                        url_for(
                            "edit_pet",
                            pet_id=pet.id,
                        )
                    )

            except ValueError:

                flash(
                    "Invalid birth date.",
                    "danger",
                )

                return redirect(
                    url_for(
                        "edit_pet",
                        pet_id=pet.id,
                    )
                )

        parsed_weight = None

        if weight:

            try:

                parsed_weight = float(weight)

                if parsed_weight <= 0:

                    flash(
                        "Weight must be greater than zero.",
                        "danger",
                    )

                    return redirect(
                        url_for(
                            "edit_pet",
                            pet_id=pet.id,
                        )
                    )

            except ValueError:

                flash(
                    "Invalid weight.",
                    "danger",
                )

                return redirect(
                    url_for(
                        "edit_pet",
                        pet_id=pet.id,
                    )
                )

        # ------------------------------------------
        # Upload New Photo
        # ------------------------------------------

        photo = request.files.get("photo")

        if photo and photo.filename:

            if not allowed_file(photo.filename):

                flash(
                    "Only JPG, JPEG, PNG, GIF and WEBP images are allowed.",
                    "danger",
                )

                return redirect(
                    url_for(
                        "edit_pet",
                        pet_id=pet.id,
                    )
                )

            new_filename = save_pet_photo(photo)

            if new_filename is None:

                flash(
                    "Unable to save uploaded image.",
                    "danger",
                )

                return redirect(
                    url_for(
                        "edit_pet",
                        pet_id=pet.id,
                    )
                )

            delete_pet_photo(pet.photo)

            pet.photo = new_filename

        # ------------------------------------------
        # Update Database
        # ------------------------------------------

        pet.name = name
        pet.breed = breed
        pet.gender = gender
        pet.birth_date = parsed_birth_date
        pet.weight = parsed_weight
        pet.vaccination_status = vaccination_status

        try:

            db.session.commit()

        except Exception:

            db.session.rollback()

            flash(
                "Unable to update pet. Please try again.",
                "danger",
            )

            return redirect(
                url_for(
                    "edit_pet",
                    pet_id=pet.id,
                )
            )

        flash(
            "Pet updated successfully!",
            "success",
        )

        return redirect(
            url_for(
                "pet_profile",
                pet_id=pet.id,
            )
        )

    return render_template(
        "edit_pet.html",
        pet=pet,
        now=date.today(),
    )


# ==========================================================
# Delete Pet
# ==========================================================


@app.route("/delete_pet/<int:pet_id>", methods=["POST"])
@login_required
def delete_pet(pet_id):

    pet = Pet.query.filter_by(
        id=pet_id,
        user_id=current_user.id,
    ).first_or_404()

    # ------------------------------------------
    # Delete image from disk
    # ------------------------------------------

    if pet.photo:
        delete_pet_photo(pet.photo)

    # ------------------------------------------
    # Delete database record
    # ------------------------------------------

    try:

        db.session.delete(pet)
        db.session.commit()

    except Exception:

        db.session.rollback()

        flash(
            "Unable to delete pet.",
            "danger",
        )

        return redirect(
            url_for(
                "pet_profile",
                pet_id=pet.id,
            )
        )

    flash(
        "Pet deleted successfully!",
        "success",
    )

    return redirect(url_for("home"))


# ==========================================================
# END OF FILE
# ==========================================================
