from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add-pet")
def add_pet():
    return render_template("add_pet.html")

if __name__ == "__main__":
    app.run(debug=True)
