from flask_wtf import FlaskForm

from wtforms import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
)

from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
)

# ==================================================
# Register
# ==================================================


class RegisterForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=20),
        ],
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6),
        ],
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Passwords must match.",
            ),
        ],
    )

    submit = SubmitField("Create Account")


# ==================================================
# Login
# ==================================================


class LoginForm(FlaskForm):

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
        ],
    )

    remember_me = BooleanField("Remember me")

    submit = SubmitField("Login")


# ==================================================
# Forgot Password
# ==================================================


class ForgotPasswordForm(FlaskForm):

    email = StringField(
        "Email Address",
        validators=[
            DataRequired(),
            Email(),
        ],
    )

    submit = SubmitField("Send Reset Link")


# ==================================================
# Reset Password
# ==================================================


class ResetPasswordForm(FlaskForm):

    password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            Length(min=6),
        ],
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Passwords must match.",
            ),
        ],
    )

    submit = SubmitField("Reset Password")


# ==================================================
# Notification Settings
# ==================================================

from wtforms import (
    BooleanField,
    IntegerField,
    SelectField,
    TimeField,
)


class NotificationSettingsForm(FlaskForm):

    email_notifications = BooleanField("Enable Email Notifications")

    reminder_days = SelectField(
        "Remind Me",
        choices=[
            (1, "1 Day Before"),
            (3, "3 Days Before"),
            (7, "7 Days Before"),
            (14, "14 Days Before"),
        ],
        coerce=int,
    )

    notification_time = TimeField(
        "Notification Time",
        validators=[
            DataRequired(),
        ],
    )

    timezone = SelectField(
        "Timezone",
        choices=[
            ("Asia/Kolkata", "Asia/Kolkata (IST)"),
        ],
    )

    submit = SubmitField("Save Preferences")
