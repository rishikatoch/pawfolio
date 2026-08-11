from flask import jsonify, request
from flask_login import current_user, login_required

from app import app
from app.services.ai_service import ask_ai
from app.services.pet_context import build_pet_context


@app.route("/api/ai/chat", methods=["POST"])
@login_required
def ai_chat():
    data = request.get_json(silent=True) or {}

    question = data.get("message", "").strip()

    if not question:
        return jsonify({"error": "Message is required."}), 400

    if len(question) > 2000:
        return jsonify({"error": "Message is too long."}), 400

    try:
        pet_context = build_pet_context(current_user.id)

        prompt = f"""
PAWFOLIO RECORDS
================
{pet_context}

USER QUESTION
=============
{question}

Answer the user's question using the Pawfolio records above.

If the question asks for a health summary, organize the response around
important current and upcoming care.

If the question asks about a specific record, use the exact record provided.

If the requested information is not present, say that it is not available.
"""

        answer = ask_ai(prompt)

        return jsonify({"answer": answer})

    except Exception:
        app.logger.exception("Pawfolio AI request failed")

        return jsonify({"error": "Pawfolio AI is temporarily unavailable."}), 500
