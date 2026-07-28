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
