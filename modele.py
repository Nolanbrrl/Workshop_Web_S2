import mysql.connector




mydb = mysql.connector.connect(
    port = 8889,
    host = "localhost",
    user="root",
    password="root"
    database = "",
    )

mycursor = mydb.cursor()



def get_users():
    users = mycursor.execute('''select * from USER''')
    return users.fetchall()