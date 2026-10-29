import mysql.connector

import app.db as db

def get_table_max(table_name):
    conn = db.get_connection()
    cursor = db.get_cursor(conn)

    try:
        cursor.execute("SELECT MAX(id) FROM %s", table_name)
        result = cursor.fetchone()
        cursor.close()
        return result
    except Exception as err:
        print(f"Error: {err}")
        cursor.close()
        return -1

def get_row_count(table_name):
    conn = db.get_connection()
    cursor = db.get_cursor(conn)

    try:
        cursor.execute("SELECT COUNT(*) FROM %s", table_name)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as err:
        print(f"Error: {err}")
        cursor.close()
        return -1

def get_venues():
    conn = db.get_connection()
    cursor = db.get_cursor(conn)

    try:
        cursor.execute("SELECT venue_id, name FROM arenas")
        result = cursor.fetchall()
        cursor.close()
        venues = {}
        for venue in result:
            venues[venue[1]] = venue[0]
        return venues
    except Exception as err:
        print(f"Error: {err}")
        print("this is the error")
        cursor.close()
        return -1