from flask import Flask, render_template, request
from model import *

app = Flask(__name__)

@app.route('/')
def connexion():
    return render_template('connexion.html')



@app.route('/dailynotes', methods=['POST', 'GET'])
def accueil_user():
    if request.method == 'POST':
        pseudo = request.form['user_pseudo']
        password = request.form['user_password']
        return getUser(pseudo, password)
    else :
        return render_template('connexion.html', erreur="erreur serveur") 



@app.route('/<pseudo>/dailynotes/jour', methods=['POST', 'GET'])
def dailynotes(pseudo):
    if request.method == 'POST':
        comment_plus = request.form['comment_plus']
        comment_minus = request.form['comment_minus']
        mood = request.form['mood']
        drinks = request.form['drinks']
        sleep = request.form['sleep']
        activities = request.form.getlist('sport[]')
        addNotes(pseudo, comment_plus, comment_minus, mood, drinks, sleep)
        addActivities(activities, pseudo)

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
        # fav_activity = getFavActivity(pseudo)

        return render_template('jour.html', 
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
                                # fav_activity = fav_activity
                               )
    
    elif request.method == 'GET':

        # mood
        avg_mood = getAvgMood(pseudo)
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
        # fav_activity = getFavActivity(pseudo)

        return render_template('jour.html', 
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
                                # fav_activity = fav_activity
                               )

@app.route('/<pseudo>/dailynotes/semaine', methods=['POST', 'GET'])
def semaine(pseudo):
    return render_template('semaine.html', pseudo=pseudo)



@app.route('/<pseudo>/dailynotes/mois', methods=['POST', 'GET'])
def mois(pseudo):
    return render_template('mois.html', pseudo=pseudo)
    


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
    