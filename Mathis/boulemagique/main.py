from flask import Flask, render_template, request
import random

def get_response():
    pool = ["non",
            "non.",
            "non !",
            "nan",
            "nope",
            "pas du tout",
            "jamais",
            "impossible",
            "hors de question",
            "je ne peux pas",
            "je peux pas",
            "ce n'est pas possible",
            "pas possible",
            "refusé",
            "négatif"
            "oui",
            "oui.",
            "oui !",
            "ouais",
            "yeah",
            "yep",
            "ok",
            "okay",
            "d'accord",
            "dac",
            "bien sûr",
            "bien sur",
            "bien entendu",
            "certainement",
            "absolument",
            "évidemment",
            "grave",
            "carrément",
            "sans aucun doute",
            "je confirme",
            "c'est bon",
            "ça marche",
            "aucun problème"
            "peut-être",
            "peut etre",
            "ça dépend",
            "ca depend",
            "je ne sais pas",
            "jsp",
            "pas sûr",
            "pas sur",
            "à voir"
    ]
    return random.choice(pool)

    
app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def index():
    response = None
    if request.method == "POST":
        response = get_response()
    return render_template("magie.html", response=response)
app.run(host='0.0.0.0', port=81)