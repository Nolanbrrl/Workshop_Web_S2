from flask import Flask, render_template, request, jsonify, session, redirect
from flask_session import Session
from model import *

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
def connexion():
    if not session.get("name"):
        return render_template('connexion.html', erreur="erreur serveur") 
    return render_template('connexion.html')

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

@app.route('/dailynotes', methods=['POST', 'GET'])
def accueil_user():
    if request.method == 'POST':
        session["name"] = request.form['user_pseudo']
        password = request.form['user_password']
        return getUser(session["name"], password)
    else :
        return render_template('connexion.html', erreur="erreur serveur") 



@app.route('/<pseudo>/dailynotes/start', methods=['POST', 'GET'])
def dailynotes(pseudo):
    # mood
    avg_mood = int(getAvgMood(pseudo))
    max_mood = getMaxMood(pseudo)
    day_max_mood = getDayMoodMax(pseudo)
    min_mood = getMinMood(pseudo)
    day_min_mood = getDayMoodMin(pseudo)

    # sleep
    avg_sleep = int(getAvgSleep(pseudo))
    max_sleep = getMaxSleep(pseudo)
    day_max_sleep = getDaySleepMax(pseudo)
    min_sleep = getMinSleep(pseudo)
    day_min_sleep = getDaySleepMin(pseudo)

    # water
    avg_water = int(getAvgWater(pseudo))
    max_water = getMaxWater(pseudo)
    day_max_water = getDayWaterMax(pseudo)
    min_water = getMinWater(pseudo)
    day_min_water = getDayWaterMin(pseudo)

    # activities
    fav_activity = getFavActivity(pseudo)

    return render_template('start.html', 
                            # mood
                            pseudo=pseudo, 
                            avg_mood=avg_mood,
                            max_mood=max_mood,
                            day_max_mood=day_max_mood,
                            min_mood=min_mood,
                            day_min_mood=day_min_mood,

                            # sleep
                            avg_sleep=avg_sleep,
                            max_sleep=max_sleep,
                            day_max_sleep=day_max_sleep,
                            min_sleep=min_sleep,
                            day_min_sleep=day_min_sleep,

                            # water
                            avg_water=avg_water,
                            max_water=max_water,
                            day_max_water=day_max_water,
                            min_water=min_water,
                            day_min_water=day_min_water,

                            # activities
                            fav_activity = fav_activity
                            )
    
@app.route('/<pseudo>/dailynotes/jour', methods=['POST', 'GET'])
def jour(pseudo):
    if request.method == 'POST':
        comment_plus = request.form['comment_plus']
        comment_minus = request.form['comment_minus']
        mood = request.form['mood']
        drinks = request.form['drinks']
        sleep = request.form['sleep']
        activities = request.form.getlist('sport[]')
        addNotes(pseudo, comment_plus, comment_minus, mood, drinks, sleep)
        addActivities(activities, pseudo)

        current_day_infos = getCurrentDayInfo(pseudo)
        current_day_activities = getCurrentActivity(pseudo)

        return render_template('jour.html', 
                                pseudo=pseudo, 
                                current_day_infos=current_day_infos,
                                current_day_activities=current_day_activities,
                               )
    
    elif request.method == 'GET':

        current_day_infos = getCurrentDayInfo(pseudo)
        current_day_activities = getCurrentActivity(pseudo)

        return render_template('jour.html', 
                                pseudo=pseudo, 
                                current_day_infos=current_day_infos,
                                current_day_activities=current_day_activities,
                               )

@app.route('/<pseudo>/dailynotes/semaine', methods=['POST', 'GET'])
def semaine(pseudo):
    # mood
    avg_mood = getAvgMoodWeek(pseudo)
    max_mood = getMaxMoodWeek(pseudo)
    min_mood = getMinMoodWeek(pseudo)

    # sleep
    avg_sleep = int(getAvgSleepWeek(pseudo))
    max_sleep = getMaxSleepWeek(pseudo)
    min_sleep = getMinSleepWeek(pseudo)

    # water
    avg_water = int(getAvgWaterWeek(pseudo))
    max_water = getMaxWaterWeek(pseudo)
    min_water = getMinWaterWeek(pseudo)

    # activities
    fav_activity = getFavActivityWeek(pseudo)

    return render_template('semaine.html', 
                            # mood
                            pseudo=pseudo, 
                            avg_mood=avg_mood,
                            max_mood=max_mood,
                            min_mood=min_mood,
                                
                            # sleep
                            avg_sleep=avg_sleep,
                            max_sleep=max_sleep,
                            min_sleep=min_sleep,

                            # water
                            avg_water=avg_water,
                            max_water=max_water,
                            min_water=min_water,

                            # activities
                            fav_activity = fav_activity
                            )


@app.route('/<pseudo>/dailynotes/mois', methods=['POST', 'GET'])
def mois(pseudo):
    # mood
    avg_mood = getAvgMoodMonth(pseudo)
    max_mood = getMaxMoodMonth(pseudo)
    min_mood = getMinMoodMonth(pseudo)

    # sleep
    avg_sleep = int(getAvgSleepMonth(pseudo))
    max_sleep = getMaxSleepMonth(pseudo)
    min_sleep = getMinSleepMonth(pseudo)

    # water
    avg_water = int(getAvgWaterMonth(pseudo))
    max_water = getMaxWaterMonth(pseudo)
    min_water = getMinWaterMonth(pseudo)

    # activities
    fav_activity = getFavActivityMonth(pseudo)

    return render_template('mois.html', 
                            # mood
                            pseudo=pseudo, 
                            avg_mood=avg_mood,
                            max_mood=max_mood,
                            min_mood=min_mood,
                                
                            # sleep
                            avg_sleep=avg_sleep,
                            max_sleep=max_sleep,
                            min_sleep=min_sleep,

                            # water
                            avg_water=avg_water,
                            max_water=max_water,
                            min_water=min_water,

                            # activities
                            fav_activity = fav_activity
                            )    


@app.route('/inscription')
def inscription():
    return render_template('inscription.html')



@app.route('/inscription_user', methods=['POST'])
def inscription_user():
    if request.method == 'POST':
        pseudo = request.form['user_pseudo']
        password = request.form['user_password']
        lastname = request.form['user_lastname']
        firstname = request.form['user_firstname']
        addUser(pseudo, password, lastname, firstname)
        return render_template('dailynotes.html', pseudo=pseudo)

    else :
        return render_template('inscription.html', erreur="erreur serveur")


@app.route('/<pseudo>/dailynotes/nepascliquer', methods=['GET'])
def affichage_json(pseudo):
    return render_template('nepascliquer.html', pseudo=pseudo)

@app.route('/api/dailynotes', methods=['GET'])
def api_dailynotes():
    data = {
        'user_id': 2,
        'pseudo': "Sylvain",
        'mot_de_passe': "Tartiflette",
        'day_id': 6,
        'day_mood': 5,
        'day_comment_plus': "Mon pigeon est beau.",
        'day_comment_minus': "Au lieu de trouver des feutres, j'ai trouvé des dolipranes.",
        'day_drinks': 4,
        'day_sleep': 10,
        'day_date': "2024-06-27",
        "day_activity": "soutenances (c'est du sport)"
    }
    return jsonify(data)