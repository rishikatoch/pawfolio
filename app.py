from app import app, db
from app.models import Pet
from flask import Flask, render_template, request, redirect, url_for



if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)


