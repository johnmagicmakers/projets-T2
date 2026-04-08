from flask import Flask, render_template, session, redirect, request
from pendu import Pendu

import os
import random

# On crée l'application
app = Flask("MonApplication")
app.secret_key = os.urandom(32)

def generer_mot():
  with open("static/français.txt") as f:
    mots = f.read().striplines()
  mot = random.choice(mots)
  return mot 

#Route de base : Page d'accueil
@app.route("/")
def index():
  mot = "test"
  vies = 6
  if "score" not in session:
    session["score"]= 0
    session["record"]= 0
  session["etat_jeu"] = Pendu.initialiser(mot,vies)
  print (session["etat_jeu"])
  return redirect("/jeu")
@app.route("/jeu")
def jeu():
  if session["etat_jeu"]["victoire"]:
    session["score"] += session["etat_jeu"]["vies"] * random.choice([0, 1, 2])
  elif session["etat_jeu"]["defaite"]:
    if session["score"] > session["record"]:
      session["record"] = session["score"]
    session["score"] = 0
  return render_template('index.html', etat_jeu=session["etat_jeu"], score=session["score"], record=session["record"])

@app.route("/deviner", methods=["POST"])
def deviner():
  if session ["etat_jeu"]["victoire"] or session["etat_jeu"]["defaite"]:
    return redirect("/jeu")
  input = request.form["essai"]
  session["etat_jeu"] = Pendu.deviner(session["etat_jeu"], input)
  return redirect("/jeu")

# On lance l'application
app.run("0.0.0.0","3904", debug=True)