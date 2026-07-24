from datetime import date, datetime, timedelta

from flask import render_template
from flask_login import current_user, login_required

from app import app
from app.models import Deworming, Pet, Vaccination

# ==========================================
# Home
# ==========================================


@app.route("/")
@login_required
def home():

    pets = Pet.query.filter_by(user_id=current_user.id).order_by(Pet.name.asc()).all()

    total_pets = len(pets)

    total_vaccinations = (
        Vaccination.query.join(Pet).filter(Pet.user_id == current_user.id).count()
    )

    total_dewormings = (
        Deworming.query.join(Pet).filter(Pet.user_id == current_user.id).count()
    )

    today = date.today()
    next_week = today + timedelta(days=7)

    # ==========================================
    # Counts
    # ==========================================

    due_vaccinations = (
        Vaccination.query.join(Pet)
        .filter(
            Pet.user_id == current_user.id,
            Vaccination.next_due >= today,
            Vaccination.next_due <= next_week,
        )
        .count()
    )

    due_dewormings = (
        Deworming.query.join(Pet)
        .filter(
            Pet.user_id == current_user.id,
            Deworming.next_due >= today,
            Deworming.next_due <= next_week,
        )
        .count()
    )

    due_soon = due_vaccinations + due_dewormings

    overdue_vaccinations = (
        Vaccination.query.join(Pet)
        .filter(
            Pet.user_id == current_user.id,
            Vaccination.next_due < today,
        )
        .count()
    )

    overdue_dewormings = (
        Deworming.query.join(Pet)
        .filter(
            Pet.user_id == current_user.id,
            Deworming.next_due < today,
        )
        .count()
    )

    overdue_count = overdue_vaccinations + overdue_dewormings

    # ==========================================
    # Upcoming Reminders
    # ==========================================

    upcoming_reminders = []

    upcoming_vaccinations = (
        Vaccination.query.join(Pet)
        .filter(
            Pet.user_id == current_user.id,
            Vaccination.next_due >= today,
            Vaccination.next_due <= next_week,
        )
        .all()
    )

    for vaccination in upcoming_vaccinations:
        upcoming_reminders.append(
            {
                "pet_name": vaccination.pet.name,
                "type": "Vaccination",
                "title": vaccination.vaccine_name,
                "date": vaccination.next_due,
            }
        )

    upcoming_dewormings = (
        Deworming.query.join(Pet)
        .filter(
            Pet.user_id == current_user.id,
            Deworming.next_due >= today,
            Deworming.next_due <= next_week,
        )
        .all()
    )

    for deworming in upcoming_dewormings:
        upcoming_reminders.append(
            {
                "pet_name": deworming.pet.name,
                "type": "Deworming",
                "title": deworming.medicine_name,
                "date": deworming.next_due,
            }
        )

    upcoming_reminders.sort(key=lambda reminder: reminder["date"])

    # ==========================================
    # Overdue Reminders
    # ==========================================

    overdue_reminders = []

    overdue_vaccination_records = (
        Vaccination.query.join(Pet)
        .filter(
            Pet.user_id == current_user.id,
            Vaccination.next_due < today,
        )
        .all()
    )

    for vaccination in overdue_vaccination_records:
        overdue_reminders.append(
            {
                "pet_name": vaccination.pet.name,
                "type": "Vaccination",
                "title": vaccination.vaccine_name,
                "date": vaccination.next_due,
            }
        )

    overdue_deworming_records = (
        Deworming.query.join(Pet)
        .filter(
            Pet.user_id == current_user.id,
            Deworming.next_due < today,
        )
        .all()
    )

    for deworming in overdue_deworming_records:
        overdue_reminders.append(
            {
                "pet_name": deworming.pet.name,
                "type": "Deworming",
                "title": deworming.medicine_name,
                "date": deworming.next_due,
            }
        )

    overdue_reminders.sort(key=lambda reminder: reminder["date"])

    # ==========================================
    # Upcoming Birthdays
    # ==========================================

    upcoming_birthdays = []

    for pet in pets:

        if pet.birth_date:

            upcoming_birthdays.append(
                {
                    "pet": pet,
                    "next_birthday": pet.next_birthday,
                    "days_left": pet.days_until_birthday,
                    "birthday_today": pet.birthday_today,
                }
            )

    upcoming_birthdays.sort(key=lambda birthday: birthday["days_left"])

    # ==========================================
    # Recent Activity
    # ==========================================

    recent_activity = []

    recent_vaccinations = (
        Vaccination.query.join(Pet)
        .filter(Pet.user_id == current_user.id)
        .order_by(Vaccination.date_given.desc())
        .limit(5)
        .all()
    )

    for vaccination in recent_vaccinations:

        recent_activity.append(
            {
                "date": vaccination.date_given,
                "icon": "💉",
                "message": (
                    f"{vaccination.pet.name} received {vaccination.vaccine_name}"
                ),
            }
        )

    recent_dewormings = (
        Deworming.query.join(Pet)
        .filter(Pet.user_id == current_user.id)
        .order_by(Deworming.date_given.desc())
        .limit(5)
        .all()
    )

    for deworming in recent_dewormings:

        recent_activity.append(
            {
                "date": deworming.date_given,
                "icon": "🪱",
                "message": (f"{deworming.pet.name} received {deworming.medicine_name}"),
            }
        )

    recent_activity.sort(
        key=lambda activity: activity["date"],
        reverse=True,
    )

    recent_activity = recent_activity[:8]

    return render_template(
        "index.html",
        pets=pets,
        total_pets=total_pets,
        total_vaccinations=total_vaccinations,
        total_dewormings=total_dewormings,
        due_soon=due_soon,
        overdue_count=overdue_count,
        upcoming_reminders=upcoming_reminders,
        overdue_reminders=overdue_reminders,
        upcoming_birthdays=upcoming_birthdays,
        recent_activity=recent_activity,
        now=datetime.now(),
    )


# ==========================================
# Health Check
# ==========================================


@app.route("/health")
def health():
    return {
        "status": "healthy",
        "service": "pawfolio",
    }, 200
