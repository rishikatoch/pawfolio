from flask import abort, render_template
from flask_login import current_user, login_required

from app import app
from app.models import Pet


@app.route("/pets/<int:pet_id>/timeline")
@login_required
def pet_timeline(pet_id):

    pet = Pet.query.filter_by(
        id=pet_id,
        user_id=current_user.id,
    ).first()

    if pet is None:
        abort(404)

    events = []

    # ==================================================
    # Vaccinations
    # ==================================================

    for vaccination in pet.vaccinations:

        events.append(
            {
                "date": vaccination.date_given,
                "category": "Vaccination",
                "icon": "bi-shield-plus",
                "color": "success",
                "title": vaccination.vaccine_name,
                "description": vaccination.notes,
                "next_due": vaccination.next_due,
            }
        )

    # ==================================================
    # Deworming
    # ==================================================

    for deworming in pet.dewormings:

        events.append(
            {
                "date": deworming.date_given,
                "category": "Deworming",
                "icon": "bi-capsule-pill",
                "color": "primary",
                "title": deworming.medicine_name,
                "description": deworming.notes,
                "next_due": deworming.next_due,
            }
        )

    # ==================================================
    # Vet Visits
    # ==================================================

    for visit in pet.vet_visits:

        events.append(
            {
                "date": visit.visit_date,
                "category": "Vet Visit",
                "icon": "bi-hospital",
                "color": "danger",
                "title": visit.reason,
                "description": visit.diagnosis,
                "clinic": visit.clinic_name,
                "veterinarian": visit.veterinarian,
                "prescription": visit.prescription,
                "follow_up": visit.follow_up_date,
            }
        )

    # ==================================================
    # Sort newest first
    # ==================================================

    events.sort(
        key=lambda event: event["date"],
        reverse=True,
    )

    return render_template(
        "timeline/index.html",
        pet=pet,
        events=events,
    )
