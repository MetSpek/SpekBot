import mysql.connector
import data.token as TOKEN
import json

mydb = mysql.connector.connect(
    host=TOKEN.DBH,
    user=TOKEN.DBU,
    password=TOKEN.DBPW,
    database=TOKEN.DB
)


cursor = mydb.cursor(dictionary=True)

async def createUser(user):
    sql = "INSERT INTO users (ID, NAME, BALANCE) VALUES (%s, %s, %s)"
    val = (user.id, user.name + '#' + str(user.discriminator), 0)
    cursor.execute(sql, val)

def userExists(id):
    cursor.execute(f"SELECT * FROM users WHERE ID = {id}")

    rows = cursor.fetchall()
    if rows:
        return True
    else:
        return False

async def getUserStat(id):
    cursor.execute(f"SELECT * FROM users WHERE ID = {id}")
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            return row
    else:
        return False

async def giveCoins(id, amount):
    user = await getUserStat(id)
    sql = "UPDATE users SET BALANCE = %s WHERE ID = %s"
    val = (str(int(user['BALANCE']) + int(amount)), id)
    cursor.execute(sql, val)


async def checkCoins(id, amount):
    user = await getUserStat(id)
    if (int(user['BALANCE']) - int(amount)) < 0:
            return False
    else:
        return True

async def removeCoins(id, amount):
    user = await getUserStat(id)

    if (int(user['BALANCE']) - int(amount)) < 0:
        return False
    else:
        sql = "UPDATE users SET BALANCE = %s WHERE ID = %s"
        val = (str(int(user['BALANCE']) - amount), id)
        cursor.execute(sql, val)
        return True


