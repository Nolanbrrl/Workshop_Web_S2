from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
    # port = 8889,
    host="localhost",
    user="root",
    password="",
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
      

@app.route('/myspace/<user_id>', methods=['POST'])
def results_user(user_id):
    if request.method == 'POST':
        mycursor.execute("SELECT AVG(day_mood) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s", (user_id,))
        mood_avg = mycursor.fetchall()

        mycursor.execute("SELECT MAX(day_mood) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s", (user_id,))
        mood_max = mycursor.fetchall()

        mycursor.execute("SELECT MIN(day_mood) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s", (user_id,))
        mood_min = mycursor.fetchall()
        return render_template('dailynotes.html', mood_avg=mood_avg, mood_max=mood_max, mood_min=mood_min)
