from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def connexion():
    return render_template('connexion.html')

@app.route('/<id_user>', methods=['POST'])
def accueil_user(id_user):
    if request.method == 'POST':
        return render_template('accueil.html', id_user_vue = id_user)
    

