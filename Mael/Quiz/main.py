# import flask
from flask import Flask, render_template, session, redirect
import random
import os
from question import question_réponse

#crée l'application
app = Flask("Quiz")
app.secret_key = os.urandom(24)

# retour de la page d'accueill
@app.route('/')
def index():
    #initialise les cooke et enregistre le numéro question
    session["numero_question"] = 0
    #initialise le cookie qui enregistre les réponse
    session["score"] = {"manger":0,"chocolat":0,"nutella":0}
    return render_template("index.html")
@app.route('/question')
def question():
    session["numero_question"]  += 1
    global question
    numero_question = session["numero_question"]



    #recupération nouvelle question
    nouvelle_question = question_réponse[numero_question].copy()


    #Récupération de lénoncer ou la question
    enonce = nouvelle_question["Question"]

    #récuper des réponses
    nouvelle_question.pop("Question")
    reponses = list(nouvelle_question.values())

    #récupération score
    session["score_reponse"] = list(nouvelle_question.keys())
    return render_template("question.html", numero_question=numero_question, enonce=enonce, reponses=reponses)



@app.route('/reponse/<cle>')
def reponse(cle):
    
    cle = int(cle)
    score_reponse = session["score_reponse"][cle]
    session["score"][score_reponse] += 1
    return redirect('/question')
# toujour tout en bas du fichier main.py
#execute l'application
app.run(host='0.0.0.0', debug=True)  