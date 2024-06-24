from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def connexion():
    return render_template('connexion.html')

@app.route('/<id_user>', methods=['POST'])
def accueil_user(id_user, mot_de_passe):
    if request.method == 'POST':
        if id_user == 'id' and mot_de_passe == 'mdp':
            return render_template('accueil.html', id_user_vue = id_user)
    

@app.route('/<id_user>/mon_espace', methods=['POST'])
def page_user(id_user):
    return render_template('mon_espace.html', id_user_vue = id_user)