from datetime import date

from flask import (
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

from app import app, db
from app.models import Pet, Deworming
from app.utils.deworming import calculate_deworming_schedule

# ==========================================================
# Add Deworming
# ==========================================================


@app.route("/pet/<int:pet_id>/deworming/add", methods=["GET", "POST"])
@login_required
def add_deworming(pet_id):

    pet = Pet.query.filter_by(
        id=pet_id,
        user_id=current_user.id,
    ).first_or_404()

    if request.method == "POST":

        medicine_name = request.form.get(
            "medicine_name",
            "",
        ).strip()

        date_given = request.form.get(
            "date_given",
            "",
        ).strip()

        veterinarian = request.form.get(
            "veterinarian",
            "",
        ).strip()

        notes = request.form.get(
            "notes",
            "",
        ).strip()

        # ------------------------------------------
        # Validation
        # ------------------------------------------

        if not medicine_name:

            return render_template(
                "add_deworming.html",
                pet=pet,
                today=date.today(),
                error="Medicine name is required.",
            )

        if not date_given:

            return render_template(
                "add_deworming.html",
                pet=pet,
                today=date.today(),
                error="Date given is required.",
            )

        date_given_obj = date.fromisoformat(date_given)

        schedule = calculate_deworming_schedule(
            pet.birth_date,
            date_given_obj,
        )

        deworming = Deworming(
            pet_id=pet.id,
            medicine_name=medicine_name,
            date_given=date_given_obj,
            next_due=schedule["next_due"],
            schedule_used=schedule["schedule_used"],
            age_at_deworming=schedule["age_at_deworming"],
            veterinarian=veterinarian,
            notes=notes,
        )

        try:

            db.session.add(deworming)
            db.session.commit()

        except Exception as e:

            db.session.rollback()

            return render_template(
                "add_deworming.html",
                pet=pet,
                today=date.today(),
                error=str(e),
            )

        flash(
            "Deworming record added successfully!",
            "success",
        )

        return redirect(
            url_for(
                "pet_profile",
                pet_id=pet.id,
            )
        )

    return render_template(
        "add_deworming.html",
        pet=pet,
        today=date.today(),
    )


# ==========================================================
# Edit Deworming
# ==========================================================


@app.route(
    "/deworming/<int:deworming_id>/edit",
    methods=["GET", "POST"],
)
@login_required
def edit_deworming(deworming_id):

    deworming = Deworming.query.get_or_404(deworming_id)

    pet = Pet.query.filter_by(
        id=deworming.pet_id,
        user_id=current_user.id,
    ).first_or_404()

    if request.method == "POST":

        medicine_name = request.form.get(
            "medicine_name",
            "",
        ).strip()

        date_given = request.form.get(
            "date_given",
            "",
        ).strip()

        veterinarian = request.form.get(
            "veterinarian",
            "",
        ).strip()

        notes = request.form.get(
            "notes",
            "",
        ).strip()

        if not medicine_name:

            return render_template(
                "edit_deworming.html",
                pet=pet,
                deworming=deworming,
                today=date.today(),
                error="Medicine name is required.",
            )

        if not date_given:

            return render_template(
                "edit_deworming.html",
                pet=pet,
                deworming=deworming,
                today=date.today(),
                error="Date given is required.",
            )

        date_given_obj = date.fromisoformat(date_given)

        schedule = calculate_deworming_schedule(
            pet.birth_date,
            date_given_obj,
        )

        deworming.medicine_name = medicine_name
        deworming.date_given = date_given_obj
        deworming.next_due = schedule["next_due"]
        deworming.schedule_used = schedule["schedule_used"]
        deworming.age_at_deworming = schedule["age_at_deworming"]
        deworming.veterinarian = veterinarian
        deworming.notes = notes

        try:

            db.session.commit()

        except Exception:

            db.session.rollback()

            return render_template(
                "edit_deworming.html",
                pet=pet,
                deworming=deworming,
                today=date.today(),
                error="Unable to update deworming record.",
            )

        flash(
            "Deworming record updated successfully!",
            "success",
        )

        return redirect(
            url_for(
                "pet_profile",
                pet_id=pet.id,
            )
        )

    return render_template(
        "edit_deworming.html",
        pet=pet,
        deworming=deworming,
        today=date.today(),
    )


# ==========================================================
# Delete Deworming
# ==========================================================


@app.route(
    "/deworming/<int:deworming_id>/delete",
    methods=["POST"],
)
@login_required
def delete_deworming(deworming_id):

    deworming = Deworming.query.get_or_404(deworming_id)

    pet = Pet.query.filter_by(
        id=deworming.pet_id,
        user_id=current_user.id,
    ).first_or_404()

    try:

        db.session.delete(deworming)
        db.session.commit()

    except Exception:

        db.session.rollback()

        flash(
            "Unable to delete deworming record.",
            "danger",
        )

        return redirect(
            url_for(
                "pet_profile",
                pet_id=pet.id,
            )
        )

    flash(
        "Deworming record deleted successfully!",
        "success",
    )

    return redirect(
        url_for(
            "pet_profile",
            pet_id=pet.id,
        )
    )


# ==========================================================
# END OF FILE
