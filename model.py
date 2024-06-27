import datetime
from flask import Flask, render_template, request
import mysql.connector

mydb = mysql.connector.connect(
    port="8889",
    host="localhost",
    user="root",
    password="root",
    database="dailynotes"
)

# -----------------------------------------------------------------------------------------------
# |                                                                                             |
# ------------------------------------ ADD ------------------------------------------------------
# |                                                                                             |
# -----------------------------------------------------------------------------------------------

def addUser(pseudo, password, lastname, firstname):
    mycursor = mydb.cursor()
    query = "INSERT INTO `USER`(`user_pseudo`, `user_password`, `user_lastname`, `user_firstname`) VALUES (%s, %s, %s, %s)"
    values = (pseudo, password, lastname, firstname)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()

def addNotes(pseudo, comment_plus, comment_minus, mood, drinks, sleep):
    mycursor = mydb.cursor()
    user_id = getInfoUser(pseudo)
    query = "INSERT INTO `DAY`(`day_comment_plus`, `day_comment_minus`, `day_mood`, `day_drinks`, `day_sleep`, `day_date`, `user_id`) VALUES (%s, %s, %s, %s, %s, NOW(), %s)"
    values = (comment_plus, comment_minus, mood, drinks, sleep, user_id)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()

def addActivities(activities, pseudo):
    user_id = getInfoUser(pseudo)
    day_id = getDayId(user_id)
    for activity in activities :
        activity_cursor = mydb.cursor()
        activity_cursor.execute("SELECT activity_id FROM ACTIVITY WHERE activity_name = %s", (activity,))
        activity_id_result = activity_cursor.fetchone()
        if activity_id_result is None:
            activity_cursor.close()
            continue
        activity_id = activity_id_result[0]
        
        query = "INSERT INTO `ACTIVITY_DAY`(`day_id`, `activity_id`) VALUES (%s, %s)"
        values = (day_id, activity_id)
        activity_cursor.execute(query, values)
        mydb.commit()
        activity_cursor.close()



# -----------------------------------------------------------------------------------------------
# |                                                                                             |
# ------------------------------------ GET ------------------------------------------------------
# |                                                                                             |
# -----------------------------------------------------------------------------------------------


def getUser(pseudo, password):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM USER WHERE user_pseudo = %s AND user_password = %s", (pseudo, password))
    result = mycursor.fetchall()
    mycursor.close()
    if result:
        return render_template('dailynotes.html', pseudo=pseudo)
    else :
        return render_template('connexion.html', erreur="identifiant ou mot de passe incorrect")

def getInfoUser(pseudo):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT user_id FROM USER WHERE user_pseudo = %s", (pseudo,))
    user_id_result = mycursor.fetchone()
    mycursor.close()
    if user_id_result is None:
        return None
    return user_id_result[0]

def getDayId(user_id):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT MAX(day_id) FROM DAY WHERE user_id = %s", (user_id,))
    day_id_result = mycursor.fetchone()
    mycursor.close()
    return day_id_result[0]



# -----------------------------------------------------------------------------------------------
# |                                                                                             |
# ------------------------------------ MOOD / JOUR ----------------------------------------------
# |                                                                                             |
# -----------------------------------------------------------------------------------------------


# Votre humeur moyenne est de : 3.6667 /5
def getAvgMood(pseudo):
    mycursor = mydb.cursor()
    query = "SELECT AVG(day_mood) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s"
    values = (pseudo,)
    mycursor.execute(query, values)
    result = mycursor.fetchall()
    mycursor.close()
    if result and result[0][0] is not None:
        return result[0][0]
    else :
        return None

# Vous avez ete le plus heureux (humeur de : 5.0 /5) le(s) jour(s) 2024-06-25
def getMaxMood(pseudo) :
    mycursor = mydb.cursor()
    query = "SELECT MAX(day_mood) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s"
    values = (pseudo,)
    mycursor.execute(query, values)
    result = mycursor.fetchall()
    mycursor.close()
    if result and result[0][0] is not None:
        return result[0][0]
    return None

def getDayMoodMax(pseudo):
    mycursor = mydb.cursor()
    query = "SELECT day_date FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s GROUP BY day_date HAVING MAX(day_mood) = (SELECT MAX(day_mood) FROM DAY WHERE user_id = (SELECT user_id FROM USER WHERE user_pseudo = %s) GROUP BY day_date ORDER BY MAX(day_mood) DESC LIMIT 1)"
    values = (pseudo, pseudo)
    mycursor.execute(query, values)
    result = mycursor.fetchall()
    mycursor.close()
    if result and result[0][0] is not None:
        return result[0][0]
    return None

# Vous avez ete le moins heureux (humeur de : 1.0 /5) le jour 2024-06-24
def getMinMood(pseudo) :
    mycursor = mydb.cursor()
    query = "SELECT MIN(day_mood) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s"
    values = (pseudo,)
    mycursor.execute(query, values)
    result = mycursor.fetchall()
    mycursor.close()
    if result and result[0][0] is not None:
        return result[0][0]
    return None

def getDayMoodMin(pseudo):
    mycursor = mydb.cursor()
    query = "SELECT day_date FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s GROUP BY day_date HAVING MIN(day_mood) = (SELECT MIN(day_mood) FROM DAY WHERE user_id = (SELECT user_id FROM USER WHERE user_pseudo = %s) GROUP BY day_date ORDER BY MIN(day_mood) LIMIT 1)"
    values = (pseudo, pseudo)
    mycursor.execute(query, values)
    result = mycursor.fetchall()
    mycursor.close()
    if result and result[0][0] is not None:
        return result[0][0]
    return None


# -----------------------------------------------------------------------------------------------
# |                                                                                             |
# ------------------------------------ SLEEP / JOUR ----------------------------------------------
# |                                                                                             |
# -----------------------------------------------------------------------------------------------

# Votre duree moyenne de sommeil est de : 8.3333h
def getAvgSleep(pseudo):
    mycursor = mydb.cursor()
    query = "SELECT AVG(day_sleep) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s"
    values = (pseudo,)
    mycursor.execute(query, values)
    result = mycursor.fetchall()
    mycursor.close()
    if result and result[0][0] is not None:
        return result[0][0]
    else :
        return None

# Vous avez dormi le plus (sommeil de : 12.0h) le jour 2024-06-26
def getMaxSleep(pseudo) :
    mycursor = mydb.cursor()
    query = "SELECT MAX(day_sleep) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s"
    values = (pseudo,)
    mycursor.execute(query, values)
    result = mycursor.fetchall()
    mycursor.close()
    if result and result[0][0] is not None:
        return result[0][0]
    return None

def getDaySleepMax(pseudo):
    mycursor = mydb.cursor()
    query = "SELECT day_date FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s GROUP BY day_date HAVING MAX(day_sleep) = (SELECT MAX(day_sleep) FROM DAY WHERE user_id = (SELECT user_id FROM USER WHERE user_pseudo = %s) GROUP BY day_date ORDER BY MAX(day_sleep) DESC LIMIT 1)"
    values = (pseudo, pseudo)
    mycursor.execute(query, values)
    result = mycursor.fetchall()
    mycursor.close()
    if result and result[0][0] is not None:
        return result[0][0]
    return None

# Vous avez dormi le moins (sommeil de : 6.0h) le jour2024-06-24
def getMinSleep(pseudo) :
    mycursor = mydb.cursor()
    query = "SELECT MIN(day_sleep) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s"
    values = (pseudo,)
    mycursor.execute(query, values)
    result = mycursor.fetchall()
    mycursor.close()
    if result and result[0][0] is not None:
        return result[0][0]
    return None

def getDaySleepMin(pseudo):
    mycursor = mydb.cursor()
    query = "SELECT day_date FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s GROUP BY day_date HAVING MIN(day_sleep) = (SELECT MIN(day_sleep) FROM DAY WHERE user_id = (SELECT user_id FROM USER WHERE user_pseudo = %s) GROUP BY day_date ORDER BY MIN(day_sleep) LIMIT 1)"
    values = (pseudo, pseudo)
    mycursor.execute(query, values)
    result = mycursor.fetchall()
    mycursor.close()
    if result and result[0][0] is not None:
        return result[0][0]
    return None


# -----------------------------------------------------------------------------------------------
# |                                                                                             |
# ------------------------------------ WATER / JOUR ---------------------------------------------
# |                                                                                             |
# -----------------------------------------------------------------------------------------------

# Votre hydratation moyenne est de : 4.0 verre(s) d'eau
def getAvgWater(pseudo):
    mycursor = mydb.cursor()
    query = "SELECT AVG(day_drinks) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s"
    values = (pseudo,)
    mycursor.execute(query, values)
    result = mycursor.fetchall()
    mycursor.close()
    if result and result[0][0] is not None:
        return result[0][0]
    else :
        return None
    
# Vous avez bu le plus (hydratation de : 6.0 verre(s) d'eau) le jour 2024-06-26
def getMaxWater(pseudo) :
    mycursor = mydb.cursor()
    query = "SELECT MAX(day_drinks) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s"
    values = (pseudo,)
    mycursor.execute(query, values)
    result = mycursor.fetchall()
    mycursor.close()
    if result and result[0][0] is not None:
        return result[0][0]
    return None

def getDayWaterMax(pseudo):
    mycursor = mydb.cursor()
    query = "SELECT day_date FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s GROUP BY day_date HAVING MAX(day_drinks) = (SELECT MAX(day_drinks) FROM DAY WHERE user_id = (SELECT user_id FROM USER WHERE user_pseudo = %s) GROUP BY day_date ORDER BY MAX(day_drinks) DESC LIMIT 1)"
    values = (pseudo, pseudo)
    mycursor.execute(query, values)
    result = mycursor.fetchall()
    mycursor.close()
    if result and result[0][0] is not None:
        return result[0][0]
    return None

# Vous avez bu le moins (hydratation de : 2.0 verre(s) d'eau) le jour 2024-06-25
def getMinWater(pseudo) :
    mycursor = mydb.cursor()
    query = "SELECT MIN(day_drinks) FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s"
    values = (pseudo,)
    mycursor.execute(query, values)
    result = mycursor.fetchall()
    mycursor.close()
    if result and result[0][0] is not None:
        return result[0][0]
    return None

def getDayWaterMin(pseudo):
    mycursor = mydb.cursor()
    query = "SELECT day_date FROM DAY INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s GROUP BY day_date HAVING MIN(day_drinks) = (SELECT MIN(day_drinks) FROM DAY WHERE user_id = (SELECT user_id FROM USER WHERE user_pseudo = %s) GROUP BY day_date ORDER BY MIN(day_drinks) LIMIT 1)"
    values = (pseudo, pseudo)
    mycursor.execute(query, values)
    result = mycursor.fetchall()
    mycursor.close()
    if result and result[0][0] is not None:
        return result[0][0]
    return None

# -----------------------------------------------------------------------------------------------
# |                                                                                             |
# ------------------------------------ ACTIVITIES / JOUR ----------------------------------------
# |                                                                                             |
# -----------------------------------------------------------------------------------------------

# Votre activite preferee est : golf
def getFavActivity(pseudo):
    mycursor = mydb.cursor()
    query = "SELECT activity_name FROM ACTIVITY INNER JOIN ACTIVITY_DAY ON ACTIVITY.activity_id = ACTIVITY_DAY.activity_id INNER JOIN DAY ON ACTIVITY_DAY.day_id = DAY.day_id INNER JOIN USER ON DAY.user_id = USER.user_id WHERE USER.user_pseudo = %s GROUP BY activity_name ORDER BY COUNT(*) DESC LIMIT 1"
    values = (pseudo)
    mycursor.execute(query, values)
    result = mycursor.fetchall()
    mycursor.close()
    if result and result[0] is not None:
        return result[0]
    return None