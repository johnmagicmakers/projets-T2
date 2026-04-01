# import flask
from flask import Flask, render_template, request
import random

def get_response():
    pool = [
        "tu trouverra un billet pour Dubaï",
        "pas de voiyage",
        "tu ira a pékin",
        "pas de chocola pour toi",
        "tu te fais arrêter par la police de limigration ",
        "tu aurra un billet pour la Moldavie"
    ]
    return random.choice(pool)
#crée l'application
app = Flask("bouleMagique")

# retour de la page d'accueill
@app.route('/', methods=["GET", "POST"])
def index():
    response = None
    if request.method == "POST":
        response = get_response()
    return render_template("index.html", response=response)




# toujour tout en bas du fichier main.py
#execute l'application
app.run(host='0.0.0.0', debug=True)  