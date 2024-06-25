import mysql.connector




mydb = mysql.connector.connect(
    host = "localhost",
    user="root",
    password="root"
    )


mycursor = mydb.cursor()



def get_users():
    mycursor.execute('''select * from USER''')
    users = mycursor.fetchall()
    return users