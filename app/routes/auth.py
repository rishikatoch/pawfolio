from flask import flash, redirect, render_template, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)

from app import app, db
from app.forms import LoginForm, RegisterForm
from app.models import User

# ==========================================
# Register
# ==========================================


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = RegisterForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()

        if existing_user:
            flash("Email already registered.", "danger")
            return redirect(url_for("register"))

        user = User(
            username=form.username.data,
            email=form.email.data,
        )

        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully. Please login.", "success")

        return redirect(url_for("login"))

    return render_template(
        "register.html",
        form=form,
    )


# ==========================================
# Login
# ==========================================


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)

            flash("Welcome back!", "success")

            return redirect(url_for("home"))

        flash("Invalid email or password.", "danger")

    return render_template(
        "login.html",
        form=form,
    )


# ==========================================
# Logout
# ==========================================


@app.route("/logout")
@login_required
def logout():
    logout_user()

    flash("Logged out successfully.", "info")

    return redirect(url_for("login"))
