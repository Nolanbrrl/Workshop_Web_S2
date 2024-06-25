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
        def get_single_value(query, user_id):
            mycursor.execute(query, (user_id,))
            result = mycursor.fetchone()
            if result and result[0] is not None:
                return float(result[0])
            return None

        mood_avg = get_single_value("SELECT AVG(day_mood) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s", user_id)
        mood_max = get_single_value("SELECT MAX(day_mood) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s", user_id)
        mood_min = get_single_value("SELECT MIN(day_mood) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s", user_id)

        sleep_avg = get_single_value("SELECT AVG(day_sleep) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s", user_id)
        sleep_max = get_single_value("SELECT MAX(day_sleep) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s", user_id)
        sleep_min = get_single_value("SELECT MIN(day_sleep) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s", user_id)

        drinks_avg = get_single_value("SELECT AVG(day_drinks) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s", user_id)
        drinks_max = get_single_value("SELECT MAX(day_drinks) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s", user_id)
        drinks_min = get_single_value("SELECT MIN(day_drinks) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s", user_id)


        mood_avg_month = get_single_value("SELECT AVG(day_mood) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s AND DAY.date >= CURDATE() - INTERVAL 31 DAY", user_id)
        mood_max_month = get_single_value("SELECT MAX(day_mood) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s AND DAY.date >= CURDATE() - INTERVAL 31 DAY", user_id)
        mood_min_month = get_single_value("SELECT MIN(day_mood) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s AND DAY.date >= CURDATE() - INTERVAL 31 DAY", user_id)

        sleep_avg_month = get_single_value("SELECT AVG(day_sleep) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s AND DAY.date >= CURDATE() - INTERVAL 31 DAY", user_id)
        sleep_max_month = get_single_value("SELECT MAX(day_sleep) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s AND DAY.date >= CURDATE() - INTERVAL 31 DAY", user_id)
        sleep_min_month = get_single_value("SELECT MIN(day_sleep) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s AND DAY.date >= CURDATE() - INTERVAL 31 DAY", user_id)

        drinks_avg_month = get_single_value("SELECT AVG(day_drinks) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s AND DAY.date >= CURDATE() - INTERVAL 31 DAY", user_id)
        drinks_max_month = get_single_value("SELECT MAX(day_drinks) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s AND DAY.date >= CURDATE() - INTERVAL 31 DAY", user_id)
        drinks_min_month = get_single_value("SELECT MIN(day_drinks) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s AND DAY.date >= CURDATE() - INTERVAL 31 DAY", user_id)



        mood_avg_week = get_single_value("SELECT AVG(day_mood) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s AND DAY.date >= CURDATE() - INTERVAL 7 DAY", user_id)
        mood_max_week = get_single_value("SELECT MAX(day_mood) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s AND DAY.date >= CURDATE() - INTERVAL 7 DAY", user_id)
        mood_min_week = get_single_value("SELECT MIN(day_mood) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s AND DAY.date >= CURDATE() - INTERVAL 7 DAY", user_id)

        sleep_avg_week = get_single_value("SELECT AVG(day_sleep) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s AND DAY.date >= CURDATE() - INTERVAL 7 DAY", user_id)
        sleep_max_week = get_single_value("SELECT MAX(day_sleep) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s AND DAY.date >= CURDATE() - INTERVAL 7 DAY", user_id)
        sleep_min_week = get_single_value("SELECT MIN(day_sleep) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s AND DAY.date >= CURDATE() - INTERVAL 7 DAY", user_id)

        drinks_avg_week = get_single_value("SELECT AVG(day_drinks) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s AND DAY.date >= CURDATE() - INTERVAL 7 DAY", user_id)
        drinks_max_week = get_single_value("SELECT MAX(day_drinks) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s AND DAY.date >= CURDATE() - INTERVAL 7 DAY", user_id)
        drinks_min_week = get_single_value("SELECT MIN(day_drinks) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_id = %s AND DAY.date >= CURDATE() - INTERVAL 7 DAY", user_id)
        return render_template('dailynotes.html', mood_avg=mood_avg, mood_max=mood_max, mood_min=mood_min, sleep_avg=sleep_avg, sleep_max=sleep_max, sleep_min=sleep_min, drinks_avg=drinks_avg, drinks_max=drinks_max, drinks_min=drinks_min,
                               mood_avg_month=mood_avg_month, mood_max_month=mood_max_month, mood_min_month=mood_min_month, sleep_avg_month=sleep_avg_month, sleep_max_month=sleep_max_month, sleep_min_month=sleep_min_month, drinks_avg_month=drinks_avg_month, drinks_max_month=drinks_max_month, drinks_min_month=drinks_min_month,
                               mood_avg_week=mood_avg_week , mood_max_week=mood_max_week, mood_min_week=mood_min_week, sleep_avg_week=sleep_avg_week, sleep_max_week=sleep_max_week, sleep_min_week=sleep_min_week, drinks_avg_week=drinks_avg_week, drinks_max_week=drinks_max_week, drinks_min_week=drinks_min_week
                               )