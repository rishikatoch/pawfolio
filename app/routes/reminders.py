from datetime import date

from flask import render_template
from flask_login import current_user, login_required

from app import app
from app.models import Deworming, Vaccination, VetVisit


def build_reminder(
    pet,
    reminder_type,
    title,
    due_date,
):
    return {
        "pet": pet,
        "type": reminder_type,
        "title": title,
        "date": due_date,
        "days_left": (due_date - date.today()).days,
    }


@app.route("/reminders")
@login_required
def reminders():

    reminders = []

    # ==========================================
    # Vaccinations
    # ==========================================

    vaccinations = (
        Vaccination.query.join(Vaccination.pet)
        .filter(
            Vaccination.pet.has(
                user_id=current_user.id,
            ),
            Vaccination.completed.is_(False),
        )
        .all()
    )

    for vaccination in vaccinations:

        if vaccination.next_due is None:
            continue

        reminders.append(
            build_reminder(
                pet=vaccination.pet.name,
                reminder_type="Vaccination",
                title=vaccination.vaccine_name,
                due_date=vaccination.next_due,
            )
        )

    # ==========================================
    # Deworming
    # ==========================================

    dewormings = (
        Deworming.query.join(Deworming.pet)
        .filter(
            Deworming.pet.has(
                user_id=current_user.id,
            )
        )
        .all()
    )

    for deworming in dewormings:

        if deworming.next_due is None:
            continue

        reminders.append(
            build_reminder(
                pet=deworming.pet.name,
                reminder_type="Deworming",
                title=deworming.medicine_name,
                due_date=deworming.next_due,
            )
        )

    # ==========================================
    # Vet Visits
    # ==========================================

    visits = (
        VetVisit.query.join(VetVisit.pet)
        .filter(
            VetVisit.pet.has(
                user_id=current_user.id,
            ),
            VetVisit.follow_up_date.isnot(None),
        )
        .all()
    )

    for visit in visits:

        reminders.append(
            build_reminder(
                pet=visit.pet.name,
                reminder_type="Vet Follow-up",
                title=visit.reason,
                due_date=visit.follow_up_date,
            )
        )

    reminders.sort(key=lambda reminder: reminder["date"])

    due_today = [reminder for reminder in reminders if reminder["days_left"] == 0]

    upcoming = [reminder for reminder in reminders if reminder["days_left"] > 0]

    overdue = [reminder for reminder in reminders if reminder["days_left"] < 0]

    return render_template(
        "reminders/index.html",
        reminders=reminders,
        due_today=due_today,
        upcoming=upcoming,
        overdue=overdue,
        total_reminders=len(reminders),
    )
