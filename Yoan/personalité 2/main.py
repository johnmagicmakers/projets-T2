from flask import Flask, render_template, request, session, redirect
import os

app = Flask("test de personalité")
app.secret_key = os.urandom(32)

questions = [
    {"texte": "En équipe, tu es plutôt ?", "options": ["Organise et structure", "Rend les choses visuelles", "Résout les problèmes complexes", "Crée des petits trucs ludiques"]},
    {"texte": "Quand tu regardes un site, tu critiques d'abord ?", "options": ["L'organisation de l'info", "L'aspect visuel et design", "Si ça fonctionne bien", "Si c'est facile à comprendre"]},
    {"texte": "Ton hobby hors du travail ?", "options": ["Ranger et organiser", "Customiser ton environnement", "Apprendre des concepts avancés", "Tester des trucs simples"]},
    {"texte": "Devant une tâche impossible, tu ?", "options": ["La décomposes en étapes", "Imagines comment la présenter", "Trouves des hacks créatifs", "Commences small et itères"]},
    {"texte": "Ton pire cauchemar ?", "options": ["Du chaos et désordre", "Une UI moche", "Des limitations techniques", "Trop de complexité"]},
    {"texte": "Tu te décris comment ?", "options": ["Méthodique et logique", "Créatif et sensible", "Curieux et expérimentateur", "Ludique et imaginatif"]},
]

symboles = ["HTML", "CSS", "Python", "C++"]

@app.route('/')
def index():
    session['symboles'] = [0, 1, 2, 3, 1, 2]  # Association question -> symbole
    session['score'] = {"HTML": 0, "CSS": 0, "Python": 0, "C++": 0}
    session['numero_question'] = 0
    return render_template('index.html')

@app.route('/question')
def question_page():
    num = session.get('numero_question', 0)
    resultat = None
    
    if num >= len(questions):
        score = session.get('score', {})
        max_symbole = max(score, key=score.get)
        resultat = f"Tu es un développeur {max_symbole} !"
        return render_template('question.html', question=None, num=num, resultat=resultat)

    question = questions[num]
    return render_template('question.html', question=question, num=num, options_indices=list(range(len(question['options']))))

# Route prenant en compte la réponse choisie
@app.route('/repondre/<numero>')  
def repondre(numero):
    # On récupère le symbole choisi
    symbole_index = session['symboles'][int(numero)]
    symbole = symboles[symbole_index]
    
    # On ajoute 1 au score pour ce symbole
    session['score'][symbole] += 1
    
    # On passe à la question suivante
    session['numero_question'] += 1
    
    # On redirige vers la question suivante
    return redirect("/question")

if __name__ == '__main__':
    app.run('0.0.0.0', port=39282, debug=True)

