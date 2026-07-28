from flask import flash, redirect, url_for
from flask_login import login_required

from app import app
from app.services.reminder_service import send_due_reminders


@app.route("/admin/send-test-reminders")
@login_required
def send_test_reminders():
    send_due_reminders()
    flash("Reminder job executed successfully.", "success")
    return redirect(url_for("index"))
