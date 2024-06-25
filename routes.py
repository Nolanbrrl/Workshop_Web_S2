from flask import Flask, render_template, request
import modele.py

app = Flask(__name__)



@app.route('/')
def connexion():
        return render_template('connexion.html')

@app.route('/<user_id>', methods=['GET'])
def accueil_user(user_id):
    if request.method == 'GET':
        # if user_id == 'id' and user_password == 'mdp':
        return render_template('accueil.html', id_user_vue = user_id)
    

@app.route('/<user_id>/mon_espace', methods=['GET'])
def page_user(user_id):
    if request.method == 'GET':
        return render_template('mon_espace.html', id_user_vue = user_id)

