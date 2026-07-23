from flask import render_template
from flask_login import current_user, login_required

from app import app
from app.models import Pet, Vaccination

# ==========================================
# Home
# ==========================================


@app.route("/")
@login_required
def home():
    pets = Pet.query.filter_by(user_id=current_user.id).order_by(Pet.name.asc()).all()

    total_pets = len(pets)

    total_vaccinations = (
        Vaccination.query.join(Pet).filter(Pet.user_id == current_user.id).count()
    )

    due_soon = 0

    return render_template(
        "index.html",
        pets=pets,
        total_pets=total_pets,
        total_vaccinations=total_vaccinations,
        due_soon=due_soon,
    )


# ==========================================
# Health Check
# ==========================================


@app.route("/health")
def health():
    return {
        "status": "healthy",
        "service": "pawfolio",
    }, 200
