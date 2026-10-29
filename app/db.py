import mysql.connector
import config

def get_connection():
    mydb = mysql.connector.connect(
        host = config.SQL_HOST,
        port = config.SQL_PORT,
        user = config.SQL_USER,
        password = config.SQL_PASSWORD,
        database = config.SQL_DB,
    )

    return mydb

def get_cursor(db):
    return db.cursor()