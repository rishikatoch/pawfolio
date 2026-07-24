from datetime import date

from flask import (
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required

from app import app, db
from app.models import Pet, VetVisit

# ==========================================================
# Add Vet Visit
# ==========================================================


@app.route("/add_vet_visit/<int:pet_id>", methods=["GET", "POST"])
@login_required
def add_vet_visit(pet_id):

    pet = Pet.query.filter_by(
        id=pet_id,
        user_id=current_user.id,
    ).first_or_404()

    if request.method == "POST":

        visit_date = request.form.get(
            "visit_date",
            "",
        ).strip()

        clinic_name = request.form.get(
            "clinic_name",
            "",
        ).strip()

        veterinarian = request.form.get(
            "veterinarian",
            "",
        ).strip()

        reason = request.form.get(
            "reason",
            "",
        ).strip()

        diagnosis = request.form.get(
            "diagnosis",
            "",
        ).strip()

        treatment = request.form.get(
            "treatment",
            "",
        ).strip()

        prescription = request.form.get(
            "prescription",
            "",
        ).strip()

        follow_up_date = request.form.get(
            "follow_up_date",
            "",
        ).strip()

        notes = request.form.get(
            "notes",
            "",
        ).strip()

        # ==================================================
        # Validation
        # ==================================================

        if not visit_date:
            flash(
                "Visit date is required.",
                "danger",
            )
            return redirect(
                url_for(
                    "add_vet_visit",
                    pet_id=pet.id,
                )
            )

        try:
            parsed_visit_date = date.fromisoformat(visit_date)

        except ValueError:
            flash(
                "Invalid visit date.",
                "danger",
            )
            return redirect(
                url_for(
                    "add_vet_visit",
                    pet_id=pet.id,
                )
            )

        if parsed_visit_date > date.today():
            flash(
                "Visit date cannot be in the future.",
                "danger",
            )
            return redirect(
                url_for(
                    "add_vet_visit",
                    pet_id=pet.id,
                )
            )

        if not clinic_name:
            flash(
                "Clinic name is required.",
                "danger",
            )
            return redirect(
                url_for(
                    "add_vet_visit",
                    pet_id=pet.id,
                )
            )

        if not veterinarian:
            flash(
                "Veterinarian name is required.",
                "danger",
            )
            return redirect(
                url_for(
                    "add_vet_visit",
                    pet_id=pet.id,
                )
            )

        if not reason:
            flash(
                "Reason for visit is required.",
                "danger",
            )
            return redirect(
                url_for(
                    "add_vet_visit",
                    pet_id=pet.id,
                )
            )

        parsed_follow_up = None

        if follow_up_date:

            try:
                parsed_follow_up = date.fromisoformat(follow_up_date)

            except ValueError:
                flash(
                    "Invalid follow-up date.",
                    "danger",
                )
                return redirect(
                    url_for(
                        "add_vet_visit",
                        pet_id=pet.id,
                    )
                )

        visit = VetVisit(
            pet_id=pet.id,
            visit_date=parsed_visit_date,
            clinic_name=clinic_name,
            veterinarian=veterinarian,
            reason=reason,
            diagnosis=diagnosis,
            treatment=treatment,
            prescription=prescription,
            follow_up_date=parsed_follow_up,
            notes=notes,
        )

        try:

            db.session.add(visit)

            db.session.commit()

            flash(
                "Vet visit added successfully!",
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
                "Unable to save vet visit.",
                "danger",
            )

            return redirect(
                url_for(
                    "add_vet_visit",
                    pet_id=pet.id,
                )
            )

    return render_template(
        "vet/add_vet_visit.html",
        pet=pet,
        today=date.today(),
    )


# ==========================================================
# Edit Vet Visit
# ==========================================================


@app.route("/edit_vet_visit/<int:visit_id>", methods=["GET", "POST"])
@login_required
def edit_vet_visit(visit_id):

    visit = (
        VetVisit.query.join(Pet)
        .filter(
            VetVisit.id == visit_id,
            Pet.user_id == current_user.id,
        )
        .first_or_404()
    )

    if request.method == "POST":

        visit_date = request.form.get(
            "visit_date",
            "",
        ).strip()

        clinic_name = request.form.get(
            "clinic_name",
            "",
        ).strip()

        veterinarian = request.form.get(
            "veterinarian",
            "",
        ).strip()

        reason = request.form.get(
            "reason",
            "",
        ).strip()

        diagnosis = request.form.get(
            "diagnosis",
            "",
        ).strip()

        treatment = request.form.get(
            "treatment",
            "",
        ).strip()

        prescription = request.form.get(
            "prescription",
            "",
        ).strip()

        follow_up_date = request.form.get(
            "follow_up_date",
            "",
        ).strip()

        notes = request.form.get(
            "notes",
            "",
        ).strip()

        # ==================================================
        # Validation
        # ==================================================

        if not visit_date:
            flash(
                "Visit date is required.",
                "danger",
            )
            return redirect(
                url_for(
                    "edit_vet_visit",
                    visit_id=visit.id,
                )
            )

        try:
            parsed_visit_date = date.fromisoformat(visit_date)

        except ValueError:
            flash(
                "Invalid visit date.",
                "danger",
            )
            return redirect(
                url_for(
                    "edit_vet_visit",
                    visit_id=visit.id,
                )
            )

        if parsed_visit_date > date.today():
            flash(
                "Visit date cannot be in the future.",
                "danger",
            )
            return redirect(
                url_for(
                    "edit_vet_visit",
                    visit_id=visit.id,
                )
            )

        if not clinic_name:
            flash(
                "Clinic name is required.",
                "danger",
            )
            return redirect(
                url_for(
                    "edit_vet_visit",
                    visit_id=visit.id,
                )
            )

        if not veterinarian:
            flash(
                "Veterinarian name is required.",
                "danger",
            )
            return redirect(
                url_for(
                    "edit_vet_visit",
                    visit_id=visit.id,
                )
            )

        if not reason:
            flash(
                "Reason for visit is required.",
                "danger",
            )
            return redirect(
                url_for(
                    "edit_vet_visit",
                    visit_id=visit.id,
                )
            )

        parsed_follow_up = None

        if follow_up_date:

            try:
                parsed_follow_up = date.fromisoformat(follow_up_date)

            except ValueError:
                flash(
                    "Invalid follow-up date.",
                    "danger",
                )
                return redirect(
                    url_for(
                        "edit_vet_visit",
                        visit_id=visit.id,
                    )
                )

        visit.visit_date = parsed_visit_date
        visit.clinic_name = clinic_name
        visit.veterinarian = veterinarian
        visit.reason = reason
        visit.diagnosis = diagnosis
        visit.treatment = treatment
        visit.prescription = prescription
        visit.follow_up_date = parsed_follow_up
        visit.notes = notes

        try:

            db.session.commit()

            flash(
                "Vet visit updated successfully!",
                "success",
            )

            return redirect(
                url_for(
                    "pet_profile",
                    pet_id=visit.pet.id,
                )
            )

        except Exception:

            db.session.rollback()

            flash(
                "Unable to update vet visit.",
                "danger",
            )

            return redirect(
                url_for(
                    "edit_vet_visit",
                    visit_id=visit.id,
                )
            )

    return render_template(
        "vet/edit_vet_visit.html",
        visit=visit,
        pet=visit.pet,
        today=date.today(),
    )


# ==========================================================
# Delete Vet Visit
# ==========================================================


@app.route("/delete_vet_visit/<int:visit_id>", methods=["POST"])
@login_required
def delete_vet_visit(visit_id):

    visit = (
        VetVisit.query.join(Pet)
        .filter(
            VetVisit.id == visit_id,
            Pet.user_id == current_user.id,
        )
        .first_or_404()
    )

    pet_id = visit.pet.id

    try:

        db.session.delete(visit)

        db.session.commit()

        flash(
            "Vet visit deleted successfully!",
            "success",
        )

    except Exception:

        db.session.rollback()

        flash(
            "Unable to delete vet visit.",
            "danger",
        )

    return redirect(
        url_for(
            "pet_profile",
            pet_id=pet_id,
        )
    )


# ==========================================================
# View Vet Visit
# ==========================================================


@app.route("/vet_visit/<int:visit_id>")
@login_required
def view_vet_visit(visit_id):

    visit = (
        VetVisit.query.join(Pet)
        .filter(
            VetVisit.id == visit_id,
            Pet.user_id == current_user.id,
        )
        .first_or_404()
    )

    return render_template(
        "vet/view_vet_visit.html",
        visit=visit,
        pet=visit.pet,
    )


# ==========================================================
# Pet Vet Visit History
# ==========================================================


@app.route("/pet/<int:pet_id>/vet_visits")
@login_required
def pet_vet_visits(pet_id):

    pet = Pet.query.filter_by(
        id=pet_id,
        user_id=current_user.id,
    ).first_or_404()

    visits = (
        VetVisit.query.filter_by(
            pet_id=pet.id,
        )
        .order_by(VetVisit.visit_date.desc())
        .all()
    )

    return render_template(
        "vet/vet_visit_history.html",
        pet=pet,
        visits=visits,
    )


# ==========================================================
# END OF FILE
# ==========================================================
