from flask import Flask, render_template, session, redirect
import os 
from questions import questions_responses
from resultats import personnalites

app = Flask("Quiz")
app.secret_key = os.urandom(24)

@app.route('/')
def index() :
    session["numero_question"] = 0
    session["score"] = {"Hermès":0, "Athéna":0, "Apollon":0, "Dionysos":0}
    return render_template("index.html")

@app.route('/questions')
def questions():
    global questions
    numero_question = session["numero_question"]

    if numero_question >= len(questions_responses) :
        print(session["score"])
        return redirect('/resultats')

    nouvelle_question = questions_responses[numero_question].copy()
    enonce = nouvelle_question["Question"]

    nouvelle_question.pop("Question")
    reponses = list(nouvelle_question.values())

    session["score_reponse"] = list(nouvelle_question.keys())

    return render_template("questions.html", 
    numero_question=numero_question, enonce=enonce, reponses=reponses)


@app.route('/reponse/<cle>')
def reponse(cle):
    session["numero_question"] += 1
    cle = int(cle)
    score_reponse = session["score_reponse"][cle]
    session["score"][score_reponse] += 1
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
    return render_template("resultats.html", resultat=resultat, personnalite=personnalite)

app.run(host="0.0.0.0", port=4200)