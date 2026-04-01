from flask import Flask, render_template, request
import random


def get_response():
    pool = [
        "Oui, absolument !",
        "Non, pas du tout.",
        "C'est possible...",
        "Redemande plus tard",
        "Je ne suis pas sûr.",
        "Oui... mais ne le dis à personne",
        "Non, et n'insiste pas.",
        "Les astres hésitent... comme toi.",
        "Le destin a dit non, mais il était de mauvaise humeur.",
        "C'est compliqué",
        "Même moi je ne sais pas.",
        "Les dieux du code ont validé",
        "Erreur 404 : Réponse non trouvée"
    ]
    return random.choice(pool)

app = Flask("BouleMagique")

@app.route("/", methods=["GET", "POST"])
def index() :
    response = None
    if request.method == "POST":
        response = get_response()
    return render_template("index.html", response=response)


app.run("0.0.0.0",3904, debug=True)