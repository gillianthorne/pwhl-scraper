from decouple import config
import mysql.connector

SQL_HOST = config("SQL_HOST")
SQL_USER = config("SQL_USER")
SQL_PASSWORD = config("SQL_PASSWORD")
SQL_DB = config("SQL_DB")

# actually connect
mydb = mysql.connector.connect(
    host=SQL_HOST,
    user=SQL_USER,
    password=SQL_PASSWORD,
    database=SQL_DB
)

cursor = mydb.cursor()

def write_players(players_list):
    # blank sql insert statement
    sql = "INSERT INTO players (id, name, shoots, catches, birthdate, hometown) VALUES (%s, %s, %s, %s, %s, %s)"

    # a list of inserts to run
    records = []

    for player in players_list:
        # if the player is a goalie vs a skater they'll have different fields to fill out
        if player["position"] == "G":
            records.append((
                player["player_id"], 
                player["name"], 
                "", 
                player["catches"],
                player["birthdate"], 
                player["hometown"]
            ))
        else:
            records.append((
                player["player_id"],
                player["name"],
                player["shoots"],
                "",
                player["birthdate"],
                player["hometown"]
            ))

    # cursor.executemany takes my records and inserts them one by one
    try:
        cursor.executemany(sql, records)
        mydb.commit()
        print(f"{cursor.rowcount} records inserted into PLAYERS successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()