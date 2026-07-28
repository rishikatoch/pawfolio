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

from app import (
    app,
    db,
)

from app.forms import NotificationSettingsForm

# ==================================================
# Notification Settings
# ==================================================


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():

    form = NotificationSettingsForm(obj=current_user)

    if form.validate_on_submit():

        current_user.email_notifications = form.email_notifications.data
        current_user.reminder_days = form.reminder_days.data
        current_user.notification_time = form.notification_time.data
        current_user.timezone = form.timezone.data

        db.session.commit()

        flash(
            "Notification preferences updated successfully.",
            "success",
        )

        return redirect(
            url_for("settings"),
        )

    return render_template(
        "settings/notification_settings.html",
        form=form,
    )
