from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

pets = []

@app.route("/")
def home():
    return render_template("index.html", pets=pets)

@app.route("/add-pet", methods=["GET", "POST"])
def add_pet():
    if request.method == "POST":
        pet = {
            "name": request.form.get("pet_name"),
            "breed": request.form.get("pet_breed"),
            "gender": request.form.get("pet_gender"),
            "age": request.form.get("pet_age"),
            "weight": request.form.get("pet_weight"),
            "vaccination_status": request.form.get("pet_vaccination_status")
        }

        pets.append(pet)

        return redirect(url_for("home"))

    return render_template("add_pet.html")

if __name__ == "__main__":
    app.run(debug=True)