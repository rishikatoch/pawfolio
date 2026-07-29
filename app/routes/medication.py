from flask import (
    flash,
    redirect,
    render_template,
    url_for,
)

from flask_login import (
    current_user,
    login_required,
)

from app import app, db
from app.forms import MedicationForm
from app.models import (
    Medication,
    Pet,
)

# ==========================================================
# Medication List
# ==========================================================


@app.route("/pet/<int:pet_id>/medications")
@login_required
def medication_list(pet_id):

    pet = Pet.query.filter_by(
        id=pet_id,
        user_id=current_user.id,
    ).first_or_404()

    medications = (
        Medication.query.filter_by(
            pet_id=pet.id,
        )
        .order_by(
            Medication.start_date.desc(),
        )
        .all()
    )

    return render_template(
        "medications/index.html",
        pet=pet,
        medications=medications,
    )


# ==========================================================
# Add Medication
# ==========================================================


@app.route(
    "/pet/<int:pet_id>/medications/add",
    methods=["GET", "POST"],
)
@login_required
def add_medication(pet_id):

    pet = Pet.query.filter_by(
        id=pet_id,
        user_id=current_user.id,
    ).first_or_404()

    form = MedicationForm()

    if form.validate_on_submit():

        medication = Medication(
            pet_id=pet.id,
            medicine_name=form.medicine_name.data,
            dosage=form.dosage.data,
            frequency=form.frequency.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            prescribed_by=form.prescribed_by.data,
            reason=form.reason.data,
            instructions=form.instructions.data,
            notes=form.notes.data,
        )

        db.session.add(medication)
        db.session.commit()

        flash(
            "Medication added successfully!",
            "success",
        )

        return redirect(
            url_for(
                "medication_list",
                pet_id=pet.id,
            )
        )

    return render_template(
        "medications/form.html",
        form=form,
        pet=pet,
        title="Add Medication",
    )


# ==========================================================
# Edit Medication
# ==========================================================


@app.route(
    "/medication/<int:medication_id>/edit",
    methods=["GET", "POST"],
)
@login_required
def edit_medication(medication_id):

    medication = (
        Medication.query.join(Pet)
        .filter(
            Medication.id == medication_id,
            Pet.user_id == current_user.id,
        )
        .first_or_404()
    )

    form = MedicationForm(obj=medication)

    if form.validate_on_submit():

        form.populate_obj(medication)

        db.session.commit()

        flash(
            "Medication updated successfully!",
            "success",
        )

        return redirect(
            url_for(
                "medication_list",
                pet_id=medication.pet_id,
            )
        )

    return render_template(
        "medications/form.html",
        form=form,
        pet=medication.pet,
        title="Edit Medication",
    )


# ==========================================================
# Delete Medication
# ==========================================================


@app.route(
    "/medication/<int:medication_id>/delete",
    methods=["POST"],
)
@login_required
def delete_medication(medication_id):

    medication = (
        Medication.query.join(Pet)
        .filter(
            Medication.id == medication_id,
            Pet.user_id == current_user.id,
        )
        .first_or_404()
    )

    pet_id = medication.pet_id

    db.session.delete(medication)
    db.session.commit()

    flash(
        "Medication deleted successfully!",
        "success",
    )

    return redirect(
        url_for(
            "medication_list",
            pet_id=pet_id,
        )
    )


# ==========================================================
# END OF FILE
# ==========================================================
