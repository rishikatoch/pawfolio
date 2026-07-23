from datetime import date, datetime

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
from app.models import Pet, Vaccination


# ==========================================================
# Add Vaccination
# ==========================================================


@app.route("/pet/<int:pet_id>/vaccination/add", methods=["GET", "POST"])
@login_required
def add_vaccination(pet_id):

    pet = Pet.query.filter_by(
        id=pet_id,
        user_id=current_user.id,
    ).first_or_404()

    if request.method == "POST":

        vaccine_name = request.form.get(
            "vaccine_name",
            "",
        ).strip()

        date_given = request.form.get(
            "date_given",
            "",
        ).strip()

        next_due = request.form.get(
            "next_due",
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

        if not vaccine_name:

            return render_template(
                "add_vaccination.html",
                pet=pet,
                today=date.today(),
                error="Vaccine name is required.",
            )

        if not date_given:

            return render_template(
                "add_vaccination.html",
                pet=pet,
                today=date.today(),
                error="Date given is required.",
            )

        if not next_due:

            return render_template(
                "add_vaccination.html",
                pet=pet,
                today=date.today(),
                error="Next due date is required.",
            )

        vaccination = Vaccination(
            pet_id=pet.id,
            vaccine_name=vaccine_name,
            date_given=date_given,
            next_due=next_due,
            veterinarian=veterinarian,
            notes=notes,
        )

        try:

            db.session.add(vaccination)
            db.session.commit()

        except Exception:

            db.session.rollback()

            return render_template(
                "add_vaccination.html",
                pet=pet,
                today=date.today(),
                error="Unable to save vaccination.",
            )

        flash(
            "Vaccination added successfully!",
            "success",
        )

        return redirect(
            url_for(
                "pet_profile",
                pet_id=pet.id,
            )
        )

    return render_template(
        "add_vaccination.html",
        pet=pet,
        today=date.today(),
    )


# ==========================================================
# Edit Vaccination
# ==========================================================


@app.route(
    "/vaccination/<int:vaccination_id>/edit",
    methods=["GET", "POST"],
)
@login_required
def edit_vaccination(vaccination_id):

    vaccination = Vaccination.query.get_or_404(
        vaccination_id
    )

    pet = Pet.query.filter_by(
        id=vaccination.pet_id,
        user_id=current_user.id,
    ).first_or_404()

    if request.method == "POST":
        vaccine_name = request.form.get(
            "vaccine_name",
            "",
        ).strip()

        date_given = request.form.get(
            "date_given",
            "",
        ).strip()

        next_due = request.form.get(
            "next_due",
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

        if not vaccine_name:

            return render_template(
                "edit_vaccination.html",
                pet=pet,
                vaccination=vaccination,
                today=date.today(),
                error="Vaccine name is required.",
            )

        if not date_given:

            return render_template(
                "edit_vaccination.html",
                pet=pet,
                vaccination=vaccination,
                today=date.today(),
                error="Date given is required.",
            )

        if not next_due:

            return render_template(
                "edit_vaccination.html",
                pet=pet,
                vaccination=vaccination,
                today=date.today(),
                error="Next due date is required.",
            )

        # ------------------------------------------
        # Update Record
        # ------------------------------------------

        vaccination.vaccine_name = vaccine_name
        vaccination.date_given = date_given
        vaccination.next_due = next_due
        vaccination.veterinarian = veterinarian
        vaccination.notes = notes

        try:

            db.session.commit()

        except Exception:

            db.session.rollback()

            return render_template(
                "edit_vaccination.html",
                pet=pet,
                vaccination=vaccination,
                today=date.today(),
                error="Unable to update vaccination.",
            )

        flash(
            "Vaccination updated successfully!",
            "success",
        )

        return redirect(
            url_for(
                "pet_profile",
                pet_id=pet.id,
            )
        )

    return render_template(
        "edit_vaccination.html",
        pet=pet,
        vaccination=vaccination,
        today=date.today(),
    )


# ==========================================================
# Delete Vaccination
# ==========================================================


@app.route(
    "/vaccination/<int:vaccination_id>/delete",
    methods=["POST"],
)
@login_required
def delete_vaccination(vaccination_id):

    vaccination = Vaccination.query.get_or_404(
        vaccination_id
    )

    pet = Pet.query.filter_by(
        id=vaccination.pet_id,
        user_id=current_user.id,
    ).first_or_404()

    try:

        db.session.delete(vaccination)
        db.session.commit()

    except Exception:

        db.session.rollback()

        flash(
            "Unable to delete vaccination.",
            "danger",
        )

        return redirect(
            url_for(
                "pet_profile",
                pet_id=pet.id,
            )
        )

    flash(
        "Vaccination deleted successfully!",
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
# ==========================================================