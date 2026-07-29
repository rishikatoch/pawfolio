from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired

from wtforms import (
    BooleanField,
    DateField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
    TimeField,
)

from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional,
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

from wtforms import IntegerField


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


# ==================================================
# Medication
# ==================================================


class MedicationForm(FlaskForm):

    medicine_name = StringField(
        "Medicine Name",
        validators=[
            DataRequired(),
            Length(max=150),
        ],
    )

    dosage = StringField(
        "Dosage",
        validators=[
            Optional(),
            Length(max=100),
        ],
    )

    frequency = SelectField(
        "Frequency",
        choices=[
            ("Once Daily", "Once Daily"),
            ("Twice Daily", "Twice Daily"),
            ("Three Times Daily", "Three Times Daily"),
            ("Every Alternate Day", "Every Alternate Day"),
            ("Weekly", "Weekly"),
            ("Monthly", "Monthly"),
            ("As Needed", "As Needed"),
        ],
        validators=[DataRequired()],
    )

    start_date = DateField(
        "Start Date",
        validators=[DataRequired()],
    )

    end_date = DateField(
        "End Date",
        validators=[Optional()],
    )

    prescribed_by = StringField(
        "Prescribed By",
        validators=[
            Optional(),
            Length(max=150),
        ],
    )

    reason = StringField(
        "Reason",
        validators=[
            Optional(),
            Length(max=255),
        ],
    )

    instructions = TextAreaField(
        "Instructions",
        validators=[Optional()],
    )

    notes = TextAreaField(
        "Notes",
        validators=[Optional()],
    )

    submit = SubmitField("Save Medication")


# ==================================================
# Document Upload
# ==================================================


class DocumentUploadForm(FlaskForm):

    title = StringField(
        "Document Title",
        validators=[
            DataRequired(),
            Length(max=150),
        ],
    )

    document_type = SelectField(
        "Document Type",
        choices=[
            ("Prescription", "Prescription"),
            ("Vaccination Certificate", "Vaccination Certificate"),
            ("Lab Report", "Lab Report"),
            ("Medical Bill", "Medical Bill"),
            ("X-Ray", "X-Ray"),
            ("Pet Photo", "Pet Photo"),
            ("Other", "Other"),
        ],
        validators=[
            DataRequired(),
        ],
    )

    file = FileField(
        "Upload File",
        validators=[
            FileRequired(),
            FileAllowed(
                [
                    "pdf",
                    "jpg",
                    "jpeg",
                    "png",
                ],
                "Only PDF, JPG, JPEG and PNG files are allowed.",
            ),
        ],
    )

    notes = TextAreaField(
        "Notes",
        validators=[
            Optional(),
        ],
    )

    submit = SubmitField("Upload Document")
