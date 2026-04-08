from flask import Flask, render_template, session, redirect, request
from pendu import Pendu
import random
import time

import os


# On crée l'application
app = Flask("MonApplication")
app.secret_key = os.urandom(32)


#Route de base : Page d'accueil
@app.route("/")
def index():
  with open("francais.txt", "r") as f:
    mots_possibles = f.readlines()
  mot_a_deviner = random.choice(mots_possibles).strip()
  session["etat"] = Pendu.initialiser(mot_a_deviner, 6, time.time())
  return redirect("/jeu")

@app.route("/jeu", methods=["GET", "POST"])
def jeu():
  scores = []
  if os.path.exists("scores.txt"):
    with open("scores.txt", "r") as f:
      for line in f:
        try:
          scores.append(int(line.strip()))
        except:
          pass
  scores.sort(reverse=True)
  top_scores = scores[:10]

  def get_title(score):
    if score >= 900:
      return "Maître du Pendu"
    elif score >= 800:
      return "Expert de la Corde"
    elif score >= 700:
      return "Habitué du Gibet"
    elif score >= 600:
      return "Apprenti Bourreau"
    elif score >= 500:
      return "Survivant Chanceux"
    elif score >= 300:
      return "Débutant Courageux"
    else:
      return "Victime du Sort"

  ranked_scores = [{"score": s, "title": get_title(s)} for s in top_scores]
  return render_template("index.html", data=session["etat"], ranked_scores=ranked_scores)


@app.route("/deviner", methods=["POST"])
def deviner():
  if session["etat"]["defaite"] or session["etat"]["victoire"]:
    return redirect("/jeu")
  essai = request.form["essai"]
  session["etat"] = Pendu.deviner(session["etat"], essai)
  # Sauvegarder le score si la partie est terminée
  if session["etat"]["defaite"] or session["etat"]["victoire"]:
    score = session["etat"]["score"]
    if score > 0:
      with open("scores.txt", "a") as f:
        f.write(f"{score}\n")
  return redirect("/jeu")

@app.route("/recommencer",  methods=["POST"])
def recommencer():
  return redirect("/")

@app.route("/classement")
def classement():
  scores = []
  if os.path.exists("scores.txt"):
    with open("scores.txt", "r") as f:
      for line in f:
        try:
          scores.append(int(line.strip()))
        except:
          pass
  scores.sort(reverse=True)
  top_scores = scores[:10]  # Top 10

  # Assigner des titres
  def get_title(score):
    if score >= 900:
      return "Maître du Pendu"
    elif score >= 800:
      return "Expert de la Corde"
    elif score >= 700:
      return "Habitué du Gibet"
    elif score >= 600:
      return "Apprenti Bourreau"
    elif score >= 500:
      return "Survivant Chanceux"
    elif score >= 300:
      return "Débutant Courageux"
    else:
      return "Victime du Sort"

  ranked_scores = [{"score": s, "title": get_title(s)} for s in top_scores]

  return render_template("classement.html", ranked_scores=ranked_scores)
# On lance l'application
app.run("0.0.0.0","3900", debug=True)