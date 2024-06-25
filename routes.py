from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
    port="8889",
    host="localhost",
    user="elea",
    password="root",
    database="dailynotes"
)

mycursor = mydb.cursor()

@app.route('/')
def connexion():
    return render_template('connexion.html')

@app.route('/dailynotes', methods=['POST'])
def accueil_user():
    if request.method == 'POST':
        pseudo = request.form['user_pseudo']
        password = request.form['user_password']
        mycursor.execute("SELECT * FROM USER WHERE user_pseudo = %s AND user_password = %s", (pseudo, password))
        result = mycursor.fetchall()
        if result:
            return render_template('accueil.html', pseudo=pseudo)
        else :
            return render_template('connexion.html', erreur="identifiant ou mot de passe incorrect")
    else :
        return render_template('connexion.html', erreur="identifiant ou mot de passe incorrect") 
      

