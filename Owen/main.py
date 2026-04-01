from flask import Flask, render_template

app = Flask("BouleMagique")

@app.route('/')
def index():
    return render_template("index.html")

app.run("0.0.0.0", 3904, debug=True)
