import app.db as db
import mysql.connector

mydb = db.get_connection()
cursor = db.get_cursor(mydb)

def write_players(players_list):
    # blank sql insert statement
    sql = "INSERT IGNORE INTO players (id, name, shoots, catches, birthdate, hometown) VALUES (%s, %s, %s, %s, %s, %s)"

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

def write_games(games_list):
    sql = """INSERT INTO games (id, date, home_team_id, visiting_team_id, season, venue, attendance, start_time, end_time, duration, home_goals, visiting_goals, win_type)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    AS new_data
    ON DUPLICATE KEY UPDATE
        attendance = new_data.attendance,
        start_time = new_data.start_time,
        end_time = new_data.end_time,
        duration = new_data.duration,
        home_goals = new_data.home_goals,
        visiting_goals = new_data.visiting_goals,
        win_type = new_data.win_type
    """

    records = []
    for game in games_list:
        records.append((
            game["game_id"],
            game["date"],
            game["home_team"],
            game["visiting_team"],
            game["season"],
            game["venue"],
            game["attendance"],
            game["start_time"],
            game["end_time"],
            game["duration"],
            game["home_goals"],
            game["visiting_goals"],
            game["win_type"]
        ))

        print(game["home_team"], game["visiting_team"])
    try:
        cursor.executemany(sql, records)
        mydb.commit()
        print(f"{cursor.rowcount} records inserted into GAMES successfully.")
    except mysql.connector.Error as err:
        print(game)
        print(f"Error: {err}")
        mydb.rollback()

def write_goalie_changes(goalie_change_list):
    sql = """INSERT INTO goalie_changes (player_id, game_id, period, time, entering) 
    VALUES (%s, %s, %s, %s, %s) 
    AS new_data
    ON DUPLICATE KEY UPDATE 
        entering = new_data.entering"""

    records = []
    for goalie_change in goalie_change_list:
        records.append((
            goalie_change["player_id"],
            goalie_change["game_id"],
            goalie_change["period"],
            goalie_change["time"],
            goalie_change["entering"]
        ))

    try:
        cursor.executemany(sql, records)
        mydb.commit()
        print(f"{cursor.rowcount} records inserted into GOALIE_CHANGES successfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()

def write_faceoffs(faceoff_list):
    sql = """INSERT INTO faceoffs (home_player_id, visiting_player_id, game_id, period, time, x_location, y_location, home_win) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    AS new_data
    ON DUPLICATE KEY UPDATE
        home_player_id = new_data.home_player_id,
        visiting_player_id = new_data.visiting_player_id,
        x_location = new_data.x_location,
        y_location = new_data.y_location,
        home_win = new_data.home_win
    """

    records = []
    for faceoff in faceoff_list:
        records.append((
            faceoff["home_player_id"],
            faceoff["visiting_player_id"],
            faceoff["game_id"],
            faceoff["period"],
            faceoff["time"],
            faceoff["x_location"],
            faceoff["y_location"],
            faceoff["home_win"]
        ))

    try:
        cursor.executemany(sql, records)
        mydb.commit()
        print(f"{cursor.rowcount} records inserted into FACEOFFS successfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()

def write_shots(shot_list):
    sql = """INSERT INTO shots (shooter_id, goalie_id, game_id, period, time, is_goal, x_location, y_location, type, quality) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    AS new_data
    ON DUPLICATE KEY UPDATE
        shooter_id = new_data.shooter_id,
        goalie_id = new_data.goalie_id,
        is_goal = new_data.is_goal,
        x_location = new_data.x_location,
        y_location = new_data.y_location,
        type = new_data.type,
        quality = new_data.quality"""

    records = []
    for shot in shot_list:
        records.append((
            shot["shooter_id"],
            shot["goalie_id"],
            shot["game_id"],
            shot["period"],
            shot["time"],
            shot["is_goal"],
            shot["x_location"],
            shot["y_location"],
            shot["type"],
            shot["quality"]
        ))

    try:
        cursor.executemany(sql, records)
        mydb.commit()
        print(f"{cursor.rowcount} records inserted into SHOTS successfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()

def write_goals(goal_list):
    sql = """INSERT INTO goals (id, scorer_id, game_id, period, time, is_powerplay, is_shorthanded, is_emptynet, is_insurancegoal, is_gamewinninggoal, x_location, y_location, is_penaltyshot) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        AS new_data
        ON DUPLICATE KEY UPDATE
            scorer_id = new_data.scorer_id,
            period = new_data.period,
            time = new_data.time,
            is_powerplay = new_data.is_powerplay,
            is_shorthanded = new_data.is_shorthanded,
            is_insurancegoal = new_data.is_insurancegoal,
            is_gamewinninggoal = new_data.is_gamewinninggoal,
            x_location = new_data.x_location,
            y_location = new_data.y_location,
            is_penaltyshot = new_data.is_penaltyshot

    """

    records = []
    for goal in goal_list:
        records.append((
            goal["goal_id"],
            goal["scorer_id"],
            goal["game_id"],
            goal["period"],
            goal["time"],
            goal["is_powerplay"],
            goal["is_shorthanded"],
            goal["is_emptynet"],
            goal["is_insurancegoal"],
            goal["is_gamewinninggoal"],
            goal["x_location"],
            goal["y_location"],
            goal["is_penaltyshot"]
        ))

    try:
        cursor.executemany(sql, records)
        mydb.commit()
        print(f"{cursor.rowcount} records inserted into GOALS successfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()

def write_assists(assists_list):
    sql = """INSERT INTO assists (goal_id, player_id, primary_secondary) 
    VALUES (%s, %s, %s)
    as new_data
    ON DUPLICATE KEY UPDATE
        player_id = new_data.player_id
    """

    records = []
    for assist in assists_list:
        records.append((
            assist["goal_id"],
            assist["player_id"],
            assist["primary_secondary"]
        ))

    try:
        cursor.executemany(sql, records)
        mydb.commit()
        print(f"{cursor.rowcount} records inserted into ASSISTS successfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()   

def write_plusminus(plusminus_list):
    sql = "INSERT IGNORE INTO plus_minus (goal_id, player_id, is_plus) VALUES (%s, %s, %s)"

    records = []
    for plusminus in plusminus_list:
        records.append((
            plusminus["goal_id"],
            plusminus["player_id"],
            plusminus["is_plus"]
        )) 

    try:
        cursor.executemany(sql, records)
        mydb.commit()
        print(f"{cursor.rowcount} records inserted into PLUS_MINUS successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()
    
def write_penalty(penalty_list):
    sql = """INSERT INTO penalties (penalty_id, taken_by_id, served_by_id, team_id, game_id, description, period, time, length, is_powerplay, is_bench)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    AS new_data
    ON DUPLICATE KEY UPDATE
        taken_by_id = new_data.taken_by_id,
        served_by_id = new_data.served_by_id,
        team_id = new_data.team_id,
        description = new_data.description,
        period = new_data.period,
        time = new_data.time,
        length = new_data.length,
        is_powerplay = new_data.is_powerplay,
        is_bench = new_data.is_bench"""

    records = []
    for penalty in penalty_list:
        records.append((
            penalty["penalty_id"],
            penalty["taken_by_id"],
            penalty["served_by_id"],
            penalty["team_id"],
            penalty["game_id"],
            penalty["description"],
            penalty["period"],
            penalty["time"],
            penalty["length"],
            penalty["is_powerplay"],
            penalty["is_bench"]
        ))

    try:
        cursor.executemany(sql, records)
        mydb.commit()
        print(f"{cursor.rowcount} records inserted into PENALTIES successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()

def write_hits(hit_list):
    sql = """INSERT INTO hits (player_id, game_id, period, time, x_location, y_location, on_player_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    AS new_data
    ON DUPLICATE KEY UPDATE
        x_location = new_data.x_location,
        y_location = new_data.y_location,
        on_player_id = new_data.on_player_id"""

    records = []
    for hit in hit_list:
        records.append((
            hit["player_id"],
            hit["game_id"],
            hit["period"],
            hit["time"],
            hit["x_location"],
            hit["y_location"],
            hit["on_player_id"]
        ))

    try:
        cursor.executemany(sql, records)
        mydb.commit()
        print(f"{cursor.rowcount} records inserted into HITS successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()

def write_blocked_shots(blocked_shot_list):
    sql = """INSERT INTO blocked_shots (shooter_id, blocker_id, goalie_id, game_id, period, time, x_location, y_location, quality, type)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    AS new_data
    ON DUPLICATE KEY UPDATE
        shooter_id = new_data.shooter_id,
        blocker_id = new_data.blocker_id,
        goalie_id = new_data.goalie_id,
        x_location = new_data.x_location,
        y_location = new_data.y_location,
        quality = new_data.quality,
        type = new_data.type"""

    records = []
    for blocked_shot in blocked_shot_list:
        records.append((
            blocked_shot["shooter_id"],
            blocked_shot["blocker_id"],
            blocked_shot["goalie_id"],
            blocked_shot["game_id"],
            blocked_shot["period"],
            blocked_shot["time"],
            blocked_shot["x_location"],
            blocked_shot["y_location"],
            blocked_shot["quality"],
            blocked_shot["type"]
        ))

    try:
        cursor.executemany(sql, records)
        mydb.commit()
        print(f"{cursor.rowcount} records inserted into BLOCKED_SHOTS successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()

def write_shootouts(shootout_list):
    sql = """INSERT INTO shootouts (shooter_id, goalie_id, game_id, is_goal, is_gamewinninggoal, shootout_attempt)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    AS new_data
    ON DUPLICATE KEY UPDATE
        goalie_id = new_data.goalie_id,
        is_goal = new_data.is_goal,
        is_gamewinninggoal = new_data.is_gamewinninggoal"""

    records = []
    for shootout in shootout_list:
        records.append((
            shootout["shooter_id"],
            shootout["goalie_id"],
            shootout["game_id"],
            shootout["is_goal"],
            shootout["is_gwg"],
            shootout["shootout_attempt"]
        ))

    try:
        cursor.executemany(sql, records)
        mydb.commit()
        print(f"{cursor.rowcount} records inserted into SHOOTOUTS successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()

def write_penalty_shots(penalty_shot_list):
    sql = """INSERT INTO penalty_shots (shooter_id, goalie_id, game_id, period, time, is_goal)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    AS new_data
    ON DUPLICATE KEY UPDATE
        goalie_id = new_data.goalie_id,
        is_goal = new_data.is_goal
        """

    records = []
    for penalty_shot in penalty_shot_list:
        records.append((
            penalty_shot["shooter_id"],
            penalty_shot["goalie_id"],
            penalty_shot["game_id"],
            penalty_shot["period"],
            penalty_shot["time"],
            penalty_shot["is_goal"]
        ))

    try:
        cursor.executemany(sql, records)
        mydb.commit()
        print(f"{cursor.rowcount} rows inserted into PENALTY_SHOTS successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()