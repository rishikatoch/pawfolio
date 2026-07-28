from flask import (
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)

from app import (
    app,
    db,
    google,
)

from app.email import send_password_reset_email

from app.forms import (
    ForgotPasswordForm,
    LoginForm,
    RegisterForm,
    ResetPasswordForm,
)

from app.models import User

# ==================================================
# Register
# ==================================================


@app.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = RegisterForm()

    if form.validate_on_submit():

        existing_user = User.query.filter_by(email=form.email.data.lower()).first()

        if existing_user:

            flash(
                "An account with this email already exists.",
                "danger",
            )

            return redirect(url_for("register"))

        user = User(
            username=form.username.data.strip(),
            email=form.email.data.lower(),
            auth_provider="local",
        )

        user.set_password(
            form.password.data,
        )

        db.session.add(user)
        db.session.commit()

        flash(
            "Account created successfully. Please login.",
            "success",
        )

        return redirect(url_for("login"))

    return render_template(
        "register.html",
        form=form,
    )


# ==================================================
# Login
# ==================================================


@app.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data.lower()).first()

        if not user:

            flash(
                "Invalid email or password.",
                "danger",
            )

            return render_template(
                "login.html",
                form=form,
            )

        # ------------------------------------------
        # Google Account
        # ------------------------------------------

        if user.auth_provider == "google" and user.password_hash is None:

            flash(
                "This account uses Google Sign-In. " "Please continue with Google.",
                "warning",
            )

            return redirect(url_for("login"))

        # ------------------------------------------
        # Password Check
        # ------------------------------------------

        if not user.check_password(form.password.data):

            flash(
                "Invalid email or password.",
                "danger",
            )

            return render_template(
                "login.html",
                form=form,
            )

        login_user(
            user,
            remember=form.remember_me.data,
        )

        flash(
            f"Welcome back, {user.username}!",
            "success",
        )

        next_page = request.args.get("next")

        if next_page:
            return redirect(next_page)

        return redirect(url_for("home"))

    return render_template(
        "login.html",
        form=form,
    )


# ==================================================
# Google Login
# ==================================================


@app.route("/login/google")
def google_login():

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    redirect_uri = url_for(
        "google_callback",
        _external=True,
    )

    return google.authorize_redirect(
        redirect_uri,
    )


# ==================================================
# Google Callback
# ==================================================


@app.route("/auth/google/callback")
def google_callback():

    token = google.authorize_access_token()

    user_info = token.get("userinfo")

    if not user_info:
        user_info = google.userinfo()

    google_id = user_info.get("sub")
    email = user_info.get("email")
    username = user_info.get("name") or email.split("@")[0]

    # ------------------------------------------
    # Existing Google Account
    # ------------------------------------------

    user = User.query.filter_by(
        google_id=google_id,
    ).first()

    if user:

        login_user(
            user,
            remember=True,
        )

        flash(
            f"Welcome back, {user.username}!",
            "success",
        )

        return redirect(url_for("home"))

    # ------------------------------------------
    # Existing Local Account
    # Link Google Account
    # ------------------------------------------

    user = User.query.filter_by(
        email=email.lower(),
    ).first()

    if user:

        if not user.google_id:

            user.google_id = google_id
            user.auth_provider = "google"

            db.session.commit()

        login_user(
            user,
            remember=True,
        )

        flash(
            "Your Google account has been linked successfully.",
            "success",
        )

        return redirect(url_for("home"))

    # ------------------------------------------
    # First Time Login
    # ------------------------------------------

    base_username = username.strip()

    final_username = base_username

    counter = 1

    while User.query.filter_by(username=final_username).first():

        final_username = f"{base_username}{counter}"

        counter += 1

    user = User(
        username=final_username,
        email=email.lower(),
        google_id=google_id,
        auth_provider="google",
    )

    db.session.add(user)
    db.session.commit()

    login_user(
        user,
        remember=True,
    )

    flash(
        "Welcome to Pawfolio!",
        "success",
    )

    return redirect(url_for("home"))


# ==================================================
# Forgot Password
# ==================================================


@app.route(
    "/forgot-password",
    methods=["GET", "POST"],
)
def forgot_password():

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = ForgotPasswordForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data.lower()).first()

        # ------------------------------------------
        # Google-only account
        # ------------------------------------------

        if user and user.auth_provider == "google" and user.password_hash is None:

            flash(
                "This account uses Google Sign-In. " "Password reset is not available.",
                "warning",
            )

            return redirect(url_for("login"))

        if user:
            send_password_reset_email(user)

        flash(
            "If an account exists with that email, "
            "a password reset link has been sent.",
            "info",
        )

        return redirect(url_for("login"))

    return render_template(
        "forgot_password.html",
        form=form,
    )


# ==================================================
# Reset Password
# ==================================================


@app.route(
    "/reset-password/<token>",
    methods=["GET", "POST"],
)
def reset_password(token):

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    user = User.verify_reset_password_token(token)

    if not user:

        flash(
            "This password reset link is invalid or has expired.",
            "danger",
        )

        return redirect(url_for("forgot_password"))

    if user.auth_provider == "google" and user.password_hash is None:

        flash(
            "Google accounts cannot reset passwords.",
            "warning",
        )

        return redirect(url_for("login"))

    form = ResetPasswordForm()

    if form.validate_on_submit():

        user.set_password(form.password.data)

        db.session.commit()

        flash(
            "Your password has been updated successfully.",
            "success",
        )

        return redirect(url_for("login"))

    return render_template(
        "reset_password.html",
        form=form,
    )


# ==================================================
# Logout
# ==================================================


@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "You have been logged out successfully.",
        "info",
    )

    return redirect(url_for("login"))


# ==================================================
# Optional Google Account Unlink
# (Future Feature)
# ==================================================


@app.route("/account/unlink-google")
@login_required
def unlink_google():

    if current_user.auth_provider != "google":

        flash(
            "This account is not linked to Google.",
            "warning",
        )

        return redirect(url_for("home"))

    if current_user.password_hash is None:

        flash(
            "Set a password before unlinking Google.",
            "warning",
        )

        return redirect(url_for("home"))

    current_user.google_id = None
    current_user.auth_provider = "local"

    db.session.commit()

    flash(
        "Google account unlinked successfully.",
        "success",
    )

    return redirect(url_for("home"))
