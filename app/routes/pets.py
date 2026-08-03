import os
import uuid
import logging
from datetime import date

from flask import (
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from flask_login import (
    current_user,
    login_required,
)

from werkzeug.utils import secure_filename

from app import app, db
from app.forms import WeightRecordForm
from app.models import (
    Pet,
    WeightRecord,
)

logger = logging.getLogger(__name__)


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
    Saves uploaded image using UUID filename.

    Returns:
        filename on success
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

    os.makedirs(
        upload_folder,
        exist_ok=True,
    )

    try:
        photo.save(
            os.path.join(
                upload_folder,
                filename,
            )
        )

        return filename

    except Exception:
        logger.exception("Failed to save pet photo")
        return None


def delete_pet_photo(filename):
    """
    Safely delete pet photo.
    """

    if not filename:
        return

    path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        filename,
    )

    try:
        os.remove(path)
    except FileNotFoundError:
        logger.debug("Pet photo '%s' was already removed.", filename)
    except Exception:
        logger.exception("Failed to delete pet photo")


# ==========================================================
# Weight Helpers
# ==========================================================


def create_initial_weight_record(
    pet,
    weight,
    measurement_date=None,
):
    """
    Create the first WeightRecord for a pet.

    Pet no longer stores a weight column.
    WeightRecord is the single source of truth.
    """

    if weight is None:
        return

    db.session.add(
        WeightRecord(
            pet_id=pet.id,
            weight=weight,
            measurement_date=(measurement_date or date.today()),
            notes="Initial weight",
        )
    )


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

    vaccinations = pet.vaccinations
    dewormings = pet.dewormings

    weight_history = (
        WeightRecord.query.filter_by(
            pet_id=pet.id,
        )
        .order_by(
            WeightRecord.measurement_date.desc(),
            WeightRecord.id.desc(),
        )
        .all()
    )

    latest_weight = weight_history[0] if weight_history else None

    previous_weight = weight_history[1] if len(weight_history) > 1 else None

    weight_change = latest_weight.weight_change if latest_weight else None

    today = date.today()

    upcoming_items = []
    overdue_count = 0

    # ------------------------------------------------------
    # Vaccinations
    # ------------------------------------------------------

    for vaccination in vaccinations:

        if not vaccination.next_due:
            continue

        if vaccination.next_due < today:
            overdue_count += 1

        else:
            upcoming_items.append(
                {
                    "title": vaccination.vaccine_name,
                    "date": vaccination.next_due,
                    "type": "Vaccination",
                }
            )

    # ------------------------------------------------------
    # Dewormings
    # ------------------------------------------------------

    for deworming in dewormings:

        if not deworming.next_due:
            continue

        if deworming.next_due < today:
            overdue_count += 1

        else:
            upcoming_items.append(
                {
                    "title": deworming.medicine_name,
                    "date": deworming.next_due,
                    "type": "Deworming",
                }
            )

    next_due = None

    if upcoming_items:
        next_due = min(
            upcoming_items,
            key=lambda item: item["date"],
        )

    return render_template(
        "pet_profile.html",
        pet=pet,
        vaccinations=vaccinations,
        dewormings=dewormings,
        weight_history=weight_history,
        latest_weight=latest_weight,
        previous_weight=previous_weight,
        weight_change=weight_change,
        today=today,
        next_due=next_due,
        overdue_count=overdue_count,
    )


# ==========================================================
# Add Pet
# ==========================================================


@app.route("/add_pet", methods=["GET", "POST"])
@login_required
def add_pet():

    if request.method == "POST":

        name = request.form.get(
            "name",
            "",
        ).strip()

        breed = request.form.get(
            "breed",
            "",
        ).strip()

        gender = request.form.get(
            "gender",
            "",
        ).strip()

        birth_date = request.form.get(
            "birth_date",
            "",
        ).strip()

        weight = request.form.get(
            "weight",
            "",
        ).strip()

        vaccination_status = request.form.get(
            "vaccination_status",
            "",
        ).strip()

        # --------------------------------------------------
        # Validation
        # --------------------------------------------------

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

        if gender not in (
            "Male",
            "Female",
        ):
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
                        error=("Birth date cannot " "be in the future."),
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
                        error=("Weight must be " "greater than zero."),
                        now=date.today(),
                    )

            except ValueError:

                return render_template(
                    "add_pet.html",
                    error="Invalid weight.",
                    now=date.today(),
                )

        # --------------------------------------------------
        # Image Upload
        # --------------------------------------------------

        photo = request.files.get("photo")

        filename = None

        if photo and photo.filename:

            if not allowed_file(photo.filename):
                return render_template(
                    "add_pet.html",
                    error=(
                        "Only JPG, JPEG, PNG, " "GIF and WEBP images " "are allowed."
                    ),
                    now=date.today(),
                )

            filename = save_pet_photo(photo)

            if filename is None:
                return render_template(
                    "add_pet.html",
                    error=("Unable to save " "uploaded image."),
                    now=date.today(),
                )

        # --------------------------------------------------
        # Create Pet
        # --------------------------------------------------

        pet = Pet(
            user_id=current_user.id,
            name=name,
            breed=breed,
            gender=gender,
            birth_date=parsed_birth_date,
            vaccination_status=vaccination_status,
            photo=filename,
        )

        try:

            db.session.add(pet)
            db.session.flush()

            create_initial_weight_record(
                pet,
                parsed_weight,
            )

            db.session.commit()

        except Exception:

            db.session.rollback()

            if filename:
                delete_pet_photo(filename)

            return render_template(
                "add_pet.html",
                error=("Unable to save pet. " "Please try again."),
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


@app.route("/pet/<int:pet_id>/weights")
@login_required
def weight_history(pet_id):

    pet = Pet.query.filter_by(
        id=pet_id,
        user_id=current_user.id,
    ).first_or_404()

    weight_history = (
        WeightRecord.query.filter_by(
            pet_id=pet.id,
        )
        .order_by(
            WeightRecord.measurement_date.desc(),
            WeightRecord.id.desc(),
        )
        .all()
    )

    return render_template(
        "weight_history.html",
        pet=pet,
        weight_history=weight_history,
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

        name = request.form.get(
            "name",
            "",
        ).strip()

        breed = request.form.get(
            "breed",
            "",
        ).strip()

        gender = request.form.get(
            "gender",
            "",
        ).strip()

        birth_date = request.form.get(
            "birth_date",
            "",
        ).strip()

        vaccination_status = request.form.get(
            "vaccination_status",
            "",
        ).strip()

        # --------------------------------------------------
        # Validation
        # --------------------------------------------------

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

        # --------------------------------------------------
        # Upload New Photo
        # --------------------------------------------------

        photo = request.files.get("photo")

        if photo and photo.filename:

            if not allowed_file(photo.filename):
                flash(
                    ("Only JPG, JPEG, PNG, " "GIF and WEBP images " "are allowed."),
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

        # --------------------------------------------------
        # Save Changes
        # --------------------------------------------------

        pet.name = name
        pet.breed = breed
        pet.gender = gender
        pet.birth_date = parsed_birth_date
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


@app.route(
    "/pet/<int:pet_id>/weight/add",
    methods=["GET", "POST"],
)
@login_required
def add_weight(pet_id):

    pet = Pet.query.filter_by(
        id=pet_id,
        user_id=current_user.id,
    ).first_or_404()

    form = WeightRecordForm()

    if form.validate_on_submit():

        record = WeightRecord(
            pet_id=pet.id,
            weight=form.weight.data,
            measurement_date=form.measurement_date.data,
            notes=form.notes.data,
        )

        try:

            db.session.add(record)
            db.session.commit()

            flash(
                "Weight record added successfully.",
                "success",
            )

            return redirect(
                url_for(
                    "pet_profile",
                    pet_id=pet.id,
                )
            )

        except Exception:

            db.session.rollback()

            flash(
                "Unable to save weight record.",
                "danger",
            )

    return render_template(
        "add_weight.html",
        pet=pet,
        form=form,
    )


@app.route(
    "/weight/<int:weight_id>/edit",
    methods=["GET", "POST"],
)
@login_required
def edit_weight(weight_id):

    record = (
        WeightRecord.query.join(Pet)
        .filter(
            WeightRecord.id == weight_id,
            Pet.user_id == current_user.id,
        )
        .first_or_404()
    )

    form = WeightRecordForm(obj=record)

    if form.validate_on_submit():

        record.weight = form.weight.data
        record.measurement_date = form.measurement_date.data
        record.notes = form.notes.data

        try:

            db.session.commit()

            flash(
                "Weight record updated.",
                "success",
            )

            return redirect(
                url_for(
                    "weight_history",
                    pet_id=record.pet_id,
                )
            )

        except Exception:

            db.session.rollback()

            flash(
                "Unable to update weight.",
                "danger",
            )

    return render_template(
        "edit_weight.html",
        form=form,
        pet=record.pet,
        record=record,
    )


@app.route(
    "/weight/<int:weight_id>/delete",
    methods=["POST"],
)
@login_required
def delete_weight(weight_id):

    record = (
        WeightRecord.query.join(Pet)
        .filter(
            WeightRecord.id == weight_id,
            Pet.user_id == current_user.id,
        )
        .first_or_404()
    )

    pet = record.pet

    try:

        db.session.delete(record)
        db.session.commit()

        flash(
            "Weight record deleted.",
            "success",
        )

    except Exception:

        db.session.rollback()

        flash(
            "Unable to delete weight record.",
            "danger",
        )

    return redirect(
        url_for(
            "weight_history",
            pet_id=pet.id,
        )
    )


# ==========================================================
# Delete Pet
# ==========================================================


@app.route(
    "/pet/<int:pet_id>/delete",
    methods=["POST"],
)
@login_required
def delete_pet(pet_id):

    pet = Pet.query.filter_by(
        id=pet_id,
        user_id=current_user.id,
    ).first_or_404()

    try:

        # Delete pet image if it exists
        if pet.photo:
            delete_pet_photo(pet.photo)

        db.session.delete(pet)
        db.session.commit()

        flash(
            "Pet deleted successfully.",
            "success",
        )

    except Exception:

        db.session.rollback()

        flash(
            "Unable to delete pet.",
            "danger",
        )

    return redirect(url_for("home"))
