from flask import Flask, render_template, session, redirect, request
from pendu import Pendu

import os
import random

# On crée l'application
app = Flask("MonApplication")
app.secret_key = os.urandom(32)

def generer_mot():
  with open("static/francais.txt") as f:
    mots = f.read().splitlines()
  mot = random.choice(mots)
  return mot


#Route de base : Page d'accueil
@app.route("/")
def index():
  mot = generer_mot()
  vies = 7
  session["etat_jeu"] = Pendu.initialiser(mot, vies)
  return redirect("/LePendu")

@app.route("/LePendu")
def jeu():
  return render_template('index.html', etat_jeu=session["etat_jeu"])

@app.route("/deviner", methods=["POST"])
def deviner():
  if session["etat_jeu"]["victoire"] or session["etat_jeu"]["defaite"]:
    return redirect("/LePendu")
  input = request.form["essai"]
  session["etat_jeu"] = Pendu.deviner(session["etat_jeu"], input)
  print("debug", session)
  return redirect("/LePendu")
  
# On lance l'application
app.run("0.0.0.0","3904", debug=True)