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

@app.route('/')
def index():
    
    session['reponses'] = []
    session['num'] = 0
    return render_template('index.html')

@app.route('/question')
def question_page():
    num = session.get('num', 0)
    resultat = None
    
    if num >= len(questions):
        count_a = len([r for r in session['reponses'] if r == 'A'])
        count_b = len([r for r in session['reponses'] if r == 'B'])
        count_c = len([r for r in session['reponses'] if r == 'C'])
        count_d = len([r for r in session['reponses'] if r == 'D'])
        if count_a > count_b and count_a > count_c and count_a > count_d:
            resultat = "Tu es un devloppeur HTML "
        elif count_b > count_a and count_b > count_c and count_b > count_d:
            resultat = "Tu es un devloppeur CSS "
        elif count_c > count_a and count_c > count_b and count_c > count_d:
            resultat = "Tu es un devloppeur Python "
        elif count_d > count_a and count_d > count_b and count_d > count_c:
            resultat = "Tu es un devloppeur C++ "
        else:
            resultat = "Tu es un développeur unique ! "

    return render_template('question.html', question=questions[num] if num < len(questions) else None, num=num, score=num, resultat=resultat)

@app.route('/save_answer', methods=['POST'])
def save_answer():
    answer = request.form.get('answer')
    session['reponses'].append(answer)
    session['num'] += 1
    return redirect('/question')

if __name__ == '__main__':
    app.run('0.0.0.0', port=39282, debug=True)

