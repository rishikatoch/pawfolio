from flask import current_app, render_template, url_for
from flask_mail import Message

from app import mail

# ==================================================
# Password Reset Email
# ==================================================


def send_password_reset_email(user):
    """
    Send a password reset email to the user.
    """

    token = user.get_reset_password_token()

    reset_url = url_for(
        "reset_password",
        token=token,
        _external=True,
    )

    msg = Message(
        subject="Reset Your Pawfolio Password",
        recipients=[user.email],
    )

    msg.body = render_template(
        "email/reset_password.txt",
        user=user,
        reset_url=reset_url,
    )

    msg.html = render_template(
        "email/reset_password.html",
        user=user,
        reset_url=reset_url,
    )

    mail.send(msg)
