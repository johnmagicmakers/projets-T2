from flask import Flask, render_template, session, redirect
import os
from questions import questions_reponses
from resultats import personnalites, images

#Création de la route vers main
app = Flask("Quizz")
app.secret_key = os.urandom(24)

@app.route("/")
def index():
    #initialisation du cookie mémorisant le num de la question
    session["numero_question"] = 0
    #initialisation du cookie stockant les réponses
    session["score"] = {"Mars":0, "Neptune":0, "Jupiter":0, "Lune":0}
    return render_template("index.html")

@app.route('/questions')
def questions():
    global questions_reponses

    #Affichage de la question selon le cookie
    #numero_question = session["numero_question"]

    #Récupération du numéro de la question 
    numero_question = session["numero_question"]

    #FIN DES QUESTIONS
    if numero_question >= len(questions_reponses):
        print(session)
        return redirect('/resultats')

    #récupération de la nouvelle question
    nouvelle_question = questions_reponses[numero_question].copy()

    #Récupération de l'énoncé
    enonce = nouvelle_question["Question"]

    #Récupération des réponses 
    nouvelle_question.pop("Question")
    reponses = list(nouvelle_question.values())

    #RECUPERATION DU SCORE DES REPONSES
    session["score_reponse"] = list(nouvelle_question.keys())

    return render_template("questions.html", numero_question=numero_question, enonce=enonce, reponses=reponses)

@app.route('/reponse/<cle>')
def reponse(cle):
    session["numero_question"] +=1
    cle = int(cle)
    score_reponse = session["score_reponse"][cle]
    session["score"][score_reponse] +=1
    return redirect('/questions')

@app.route('/resultats')
def resultats():
    resultats = session["score"]
    max_score = 0
    max_answer = ""
    for key, value in resultats.items():
        if value > max_score:
            max_score = value
            max_answer = key
    resultat = max_answer
    personnalite = personnalites[resultat]
    image = images[resultat]
    return render_template("resultats.html", resultat=resultat, personnalite=personnalite,
                           img="../static/")

#Toujours tout en bas de votre fichier main.py
#Executer l'application
app.run('0.0.0.0', 3904, debug=True)