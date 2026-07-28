from flask import render_template, url_for
from flask_mail import Message

from app import mail

# ==================================================
# Generic Email Sender
# ==================================================


def send_email(subject, recipients, text_body, html_body):
    """
    Send an email using Flask-Mail.
    """

    msg = Message(
        subject=subject,
        recipients=recipients,
    )

    msg.body = text_body
    msg.html = html_body

    mail.send(msg)


# ==================================================
# Password Reset Email
# ==================================================


def send_password_reset_email(user):
    """
    Send a password reset email.
    """

    token = user.get_reset_password_token()

    reset_url = url_for(
        "reset_password",
        token=token,
        _external=True,
    )

    send_email(
        subject="Reset Your Pawfolio Password",
        recipients=[user.email],
        text_body=render_template(
            "email/reset_password.txt",
            user=user,
            reset_url=reset_url,
        ),
        html_body=render_template(
            "email/reset_password.html",
            user=user,
            reset_url=reset_url,
        ),
    )


# ==================================================
# Reminder Email
# ==================================================


def send_reminder_email(user, reminders):
    """
    Send one consolidated reminder email containing
    all upcoming reminders for the user.
    """

    send_email(
        subject="Upcoming Pet Care Reminder",
        recipients=[user.email],
        text_body=render_template(
            "email/reminder.txt",
            user=user,
            reminders=reminders,
        ),
        html_body=render_template(
            "email/reminder.html",
            user=user,
            reminders=reminders,
        ),
    )
