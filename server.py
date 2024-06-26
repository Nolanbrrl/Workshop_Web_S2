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
      

@app.route('/myspace/<user_pseudo>', methods=['POST'])
def results_user(user_pseudo):
    if request.method == 'POST':
        def get_single_value(query, user_pseudo):
            mycursor.execute(query, (user_pseudo,))
            result = mycursor.fetchone()
            if result and result[0] is not None:
                return float(result[0])
            return None
        
        def get_single_value2(query, user_pseudo):
            mycursor.execute(query, user_pseudo)
            result = mycursor.fetchone()
            return result[0] if result else None
                
        mood_avg = get_single_value("SELECT AVG(day_mood) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s", user_pseudo)
        mood_max = get_single_value("SELECT MAX(day_mood) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s", user_pseudo)
        mycursor.execute("SELECT day_date FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s GROUP BY day_date HAVING MAX(day_mood) = (SELECT MAX(day_mood) FROM DAY WHERE user_id = (SELECT user_id FROM USER WHERE user_pseudo = %s) GROUP BY day_date ORDER BY MAX(day_mood) DESC LIMIT 1)", (user_pseudo, user_pseudo))
        mood_max_days = mycursor.fetchall()
        mood_max_days_date = mood_max_days[0][0]
        mood_min = get_single_value("SELECT MIN(day_mood) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s", user_pseudo)
        mycursor.execute("SELECT day_date FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s GROUP BY day_date HAVING MIN(day_mood) = (SELECT MIN(day_mood) FROM DAY WHERE user_id = (SELECT user_id FROM USER WHERE user_pseudo = %s) GROUP BY day_date ORDER BY MIN(day_mood) LIMIT 1)", (user_pseudo, user_pseudo))
        mood_min_days = mycursor.fetchall()
        mood_min_days_date = mood_min_days[0][0]

        sleep_avg = get_single_value("SELECT AVG(day_sleep) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s", user_pseudo)
        sleep_max = get_single_value("SELECT MAX(day_sleep) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s", user_pseudo)
        mycursor.execute("SELECT day_date FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s GROUP BY day_date HAVING MAX(day_sleep) = (SELECT MAX(day_sleep) FROM DAY WHERE user_id = (SELECT user_id FROM USER WHERE user_pseudo = %s) GROUP BY day_date ORDER BY MAX(day_sleep) DESC LIMIT 1)", (user_pseudo, user_pseudo))
        sleep_max_days = mycursor.fetchall()
        sleep_max_days_date = sleep_max_days[0][0]
        sleep_min = get_single_value("SELECT MIN(day_sleep) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s", user_pseudo)
        mycursor.execute("SELECT day_date FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s GROUP BY day_date HAVING MIN(day_sleep) = (SELECT MIN(day_sleep) FROM DAY WHERE user_id = (SELECT user_id FROM USER WHERE user_pseudo = %s) GROUP BY day_date ORDER BY MIN(day_sleep) LIMIT 1)", (user_pseudo, user_pseudo))
        sleep_min_days = mycursor.fetchall()
        sleep_min_days_date = sleep_min_days[0][0]

        drinks_avg = get_single_value("SELECT AVG(day_drinks) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s", user_pseudo)
        drinks_max = get_single_value("SELECT MAX(day_drinks) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s", user_pseudo)
        mycursor.execute("SELECT day_date FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s GROUP BY day_date HAVING MAX(day_drinks) = (SELECT MAX(day_drinks) FROM DAY WHERE user_id = (SELECT user_id FROM USER WHERE user_pseudo = %s) GROUP BY day_date ORDER BY MAX(day_drinks) DESC LIMIT 1)", (user_pseudo, user_pseudo))
        drinks_max_days = mycursor.fetchall()
        drinks_max_days_date = drinks_max_days[0][0]
        drinks_min = get_single_value("SELECT MIN(day_drinks) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s", user_pseudo)
        mycursor.execute("SELECT day_date FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s GROUP BY day_date HAVING MIN(day_drinks) = (SELECT MIN(day_drinks) FROM DAY WHERE user_id = (SELECT user_id FROM USER WHERE user_pseudo = %s) GROUP BY day_date ORDER BY MIN(day_drinks) LIMIT 1)", (user_pseudo, user_pseudo))
        drinks_min_days = mycursor.fetchall()
        drinks_min_days_date = drinks_min_days[0][0]


        mood_avg_month = get_single_value("SELECT AVG(day_mood) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s AND DAY.day_date >= CURDATE() - INTERVAL 31 DAY", user_pseudo)
        mood_max_month = get_single_value("SELECT MAX(day_mood) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s AND DAY.day_date >= CURDATE() - INTERVAL 31 DAY", user_pseudo)
        mood_min_month = get_single_value("SELECT MIN(day_mood) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s AND DAY.day_date >= CURDATE() - INTERVAL 31 DAY", user_pseudo)

        sleep_avg_month = get_single_value("SELECT AVG(day_sleep) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s AND DAY.day_date >= CURDATE() - INTERVAL 31 DAY", user_pseudo)
        sleep_max_month = get_single_value("SELECT MAX(day_sleep) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s AND DAY.day_date >= CURDATE() - INTERVAL 31 DAY", user_pseudo)
        sleep_min_month = get_single_value("SELECT MIN(day_sleep) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s AND DAY.day_date >= CURDATE() - INTERVAL 31 DAY", user_pseudo)

        drinks_avg_month = get_single_value("SELECT AVG(day_drinks) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s AND DAY.day_date >= CURDATE() - INTERVAL 31 DAY", user_pseudo)
        drinks_max_month = get_single_value("SELECT MAX(day_drinks) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s AND DAY.day_date >= CURDATE() - INTERVAL 31 DAY", user_pseudo)
        drinks_min_month = get_single_value("SELECT MIN(day_drinks) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s AND DAY.day_date >= CURDATE() - INTERVAL 31 DAY", user_pseudo)



        mood_avg_week = get_single_value("SELECT AVG(day_mood) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s AND DAY.day_date >= CURDATE() - INTERVAL 7 DAY", user_pseudo)
        mood_max_week = get_single_value("SELECT MAX(day_mood) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s AND DAY.day_date >= CURDATE() - INTERVAL 7 DAY", user_pseudo)
        mood_min_week = get_single_value("SELECT MIN(day_mood) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s AND DAY.day_date >= CURDATE() - INTERVAL 7 DAY", user_pseudo)

        sleep_avg_week = get_single_value("SELECT AVG(day_sleep) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s AND DAY.day_date >= CURDATE() - INTERVAL 7 DAY", user_pseudo)
        sleep_max_week = get_single_value("SELECT MAX(day_sleep) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s AND DAY.day_date >= CURDATE() - INTERVAL 7 DAY", user_pseudo)
        sleep_min_week = get_single_value("SELECT MIN(day_sleep) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s AND DAY.day_date >= CURDATE() - INTERVAL 7 DAY", user_pseudo)

        drinks_avg_week = get_single_value("SELECT AVG(day_drinks) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s AND DAY.day_date >= CURDATE() - INTERVAL 7 DAY", user_pseudo)
        drinks_max_week = get_single_value("SELECT MAX(day_drinks) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s AND DAY.day_date >= CURDATE() - INTERVAL 7 DAY", user_pseudo)
        drinks_min_week = get_single_value("SELECT MIN(day_drinks) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s AND DAY.day_date >= CURDATE() - INTERVAL 7 DAY", user_pseudo)

        activity_fav = get_single_value2("SELECT activity_name FROM ACTIVITY INNER JOIN ACTIVITY_DAY ON ACTIVITY.activity_id = ACTIVITY_DAY.activity_id INNER JOIN DAY ON ACTIVITY_DAY.day_id = DAY.day_id INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s GROUP BY activity_name ORDER BY COUNT(*) DESC LIMIT 1", (user_pseudo,))
        activity_fav_week = get_single_value2("SELECT activity_name FROM ACTIVITY INNER JOIN ACTIVITY_DAY ON ACTIVITY.activity_id = ACTIVITY_DAY.activity_id INNER JOIN DAY ON ACTIVITY_DAY.day_id = DAY.day_id INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s AND DAY.day_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) GROUP BY activity_name ORDER BY COUNT(*) DESC LIMIT 1", (user_pseudo,))
        activity_fav_month = get_single_value2("SELECT activity_name FROM ACTIVITY INNER JOIN ACTIVITY_DAY ON ACTIVITY.activity_id = ACTIVITY_DAY.activity_id INNER JOIN DAY ON ACTIVITY_DAY.day_id = DAY.day_id INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s AND DAY.day_date >= DATE_SUB(CURDATE(), INTERVAL 31 DAY) GROUP BY activity_name ORDER BY COUNT(*) DESC LIMIT 1", (user_pseudo,))
       
        return render_template('dailynotes.html', mood_avg=mood_avg, mood_max=mood_max, mood_min=mood_min, sleep_avg=sleep_avg, sleep_max=sleep_max, sleep_min=sleep_min, drinks_avg=drinks_avg, drinks_max=drinks_max, drinks_min=drinks_min,
                               mood_avg_month=mood_avg_month, mood_max_month=mood_max_month, mood_min_month=mood_min_month, sleep_avg_month=sleep_avg_month, sleep_max_month=sleep_max_month, sleep_min_month=sleep_min_month, drinks_avg_month=drinks_avg_month, drinks_max_month=drinks_max_month, drinks_min_month=drinks_min_month,
                               mood_avg_week=mood_avg_week , mood_max_week=mood_max_week, mood_min_week=mood_min_week, sleep_avg_week=sleep_avg_week, sleep_max_week=sleep_max_week, sleep_min_week=sleep_min_week, drinks_avg_week=drinks_avg_week, drinks_max_week=drinks_max_week, drinks_min_week=drinks_min_week,
                               user_pseudo=user_pseudo,
                               mood_max_days_date=mood_max_days_date, mood_min_days_date=mood_min_days_date, sleep_max_days_date=sleep_max_days_date, sleep_min_days_date=sleep_min_days_date, drinks_max_days_date=drinks_max_days_date,drinks_min_days_date=drinks_min_days_date,
                               activity_fav=activity_fav, activity_fav_week=activity_fav_week, activity_fav_month=activity_fav_month
                               )
   
