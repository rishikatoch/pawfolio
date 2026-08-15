from datetime import date, timedelta
import logging

from app import db
from app.email import send_reminder_email
from app.models import (
    User,
    Vaccination,
    Deworming,
    VetVisit,
    ReminderLog,
)

logger = logging.getLogger(__name__)


def _collect_vaccination_reminders(user, target_date):
    reminders = []

    vaccinations = (
        Vaccination.query.join(Vaccination.pet)
        .filter(
            Vaccination.next_due == target_date,
            Vaccination.pet.has(user_id=user.id),
            Vaccination.completed.is_(False),
        )
        .all()
    )

    for vaccination in vaccinations:
        reminders.append(
            {
                "pet": vaccination.pet.name,
                "title": f"Vaccination - {vaccination.vaccine_name}",
                "date": vaccination.next_due,
                "type": "vaccination",
                "reference_id": vaccination.id,
            }
        )

    return reminders


def _collect_deworming_reminders(user, target_date):
    reminders = []

    dewormings = (
        Deworming.query.join(Deworming.pet)
        .filter(
            Deworming.next_due == target_date,
            Deworming.pet.has(user_id=user.id),
        )
        .all()
    )

    for deworming in dewormings:
        reminders.append(
            {
                "pet": deworming.pet.name,
                "title": "Deworming",
                "date": deworming.next_due,
                "type": "deworming",
                "reference_id": deworming.id,
            }
        )

    return reminders


def _collect_followup_reminders(user, target_date):
    reminders = []

    visits = (
        VetVisit.query.join(VetVisit.pet)
        .filter(
            VetVisit.follow_up_date == target_date,
            VetVisit.pet.has(user_id=user.id),
        )
        .all()
    )

    for visit in visits:
        reminders.append(
            {
                "pet": visit.pet.name,
                "title": "Vet Follow-up",
                "date": visit.follow_up_date,
                "type": "vet_visit",
                "reference_id": visit.id,
            }
        )

    return reminders


def get_user_reminders(user):
    """
    Build a consolidated reminder list for one user.
    """

    if not user.email_notifications:
        return []

    target_date = date.today() + timedelta(days=user.reminder_days)

    logger.info(
        "Target reminder date for %s: %s",
        user.email,
        target_date,
    )

    reminders = []

    reminders.extend(
        _collect_vaccination_reminders(
            user,
            target_date,
        )
    )

    reminders.extend(
        _collect_deworming_reminders(
            user,
            target_date,
        )
    )

    reminders.extend(
        _collect_followup_reminders(
            user,
            target_date,
        )
    )

    reminders.sort(key=lambda reminder: reminder["date"])

    return reminders


def reminder_already_sent(user_id, reminder):
    """
    Returns True if this reminder has already been emailed.
    """

    return (
        ReminderLog.query.filter_by(
            user_id=user_id,
            reminder_type=reminder["type"],
            reference_id=reminder["reference_id"],
            reminder_date=reminder["date"],
        ).first()
        is not None
    )


def log_sent_reminder(user_id, reminder):
    """
    Save a reminder log after an email has been sent.
    """

    db.session.add(
        ReminderLog(
            user_id=user_id,
            reminder_type=reminder["type"],
            reference_id=reminder["reference_id"],
            reminder_date=reminder["date"],
        )
    )


def send_due_reminders():
    """
    Send reminder emails for every user.
    Intended to be called by the scheduler.
    """

    logger.info("Starting reminder job")

    users = User.query.filter_by(email_notifications=True).all()

    logger.info(
        "Found %d users with email notifications enabled",
        len(users),
    )

    emails_sent = 0

    for user in users:

        logger.info(
            "Checking reminders for %s",
            user.email,
        )

        reminders = get_user_reminders(user)

        logger.info(
            "Found %d reminder(s)",
            len(reminders),
        )

        unsent_reminders = [
            reminder
            for reminder in reminders
            if not reminder_already_sent(
                user.id,
                reminder,
            )
        ]

        logger.info(
            "Found %d unsent reminder(s)",
            len(unsent_reminders),
        )

        if not unsent_reminders:
            continue

        send_reminder_email(
            user=user,
            reminders=unsent_reminders,
        )

        for reminder in unsent_reminders:
            log_sent_reminder(
                user.id,
                reminder,
            )

        db.session.commit()

        emails_sent += 1

        logger.info(
            "Reminder email sent to %s",
            user.email,
        )

    db.session.remove()

    logger.info(
        "Reminder job completed successfully. Emails sent: %d",
        emails_sent,
    )
