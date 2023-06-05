import mysql.connector
import data.token as TOKEN

mydb = mysql.connector.connect(
    host=TOKEN.DBH,
    user=TOKEN.DBU,
    password=TOKEN.DBPW,
    database=TOKEN.DB
)


cursor = mydb.cursor(dictionary=True)

def createUser(id):
    sql = "INSERT INTO users (ID, BALANCE) VALUES (%s, %s)"
    val = (id, 0)
    cursor.execute(sql, val)

def userExists(id):
    cursor.execute(f"SELECT * FROM users WHERE ID = {id}")

    rows = cursor.fetchall()
    if rows:
        return True
    else:
        return False

def getUserStat(id):
    cursor.execute(f"SELECT * FROM users WHERE ID = {id}")
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            return row
    else:
        return False

def giveCoins(id, amount):
    user = getUserStat(id)

    sql = "UPDATE users SET BALANCE = %s WHERE ID = %s"
    val = (str(int(user['BALANCE']) + amount), id)
    cursor.execute(sql, val)