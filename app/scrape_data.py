import requests
import json
import datetime
import math
from decouple import config
import mysql.connector

# declare global variables
SEASON = int(config("SEASON"))
MAX_TEAM_ID = int(config("MAX_TEAM_ID"))
MAX_GAME = int(config("MAX_GAME"))
MIN_GAME = int(config("MIN_GAME"))
SEASON = int(config("SEASON"))

def return_json(url):
    # since this is literally just json, no need for beautifulsoup. just requests.get and go
    response = requests.get(url)
    # okay it isn't parsed as json: it's stored in round brackets. this strips it of them.
    data = response.text[1:-1]
    # and make it a dict for us to use!
    data = json.loads(data)

    return data


def get_players():
    # set up empty lists for us to put our data in temporarily
    players = []

    # we're counting through each team, with +1 because python goes up to but not including the second number
    for i in range(1, MAX_TEAM_ID + 1):
        # this is the ugly ugly url that we're getting data from
        url = f"https://lscluster.hockeytech.com/feed/index.php?feed=statviewfeed&view=roster&team_id={i}&season_id={SEASON}&key=446521baf8c38984&client_code=pwhl&site_id=0&league_id=1&lang=en"
        
        roster = return_json(url)

        # the path to the actual data is janky, but this is it
        for section in roster["roster"][0]["sections"]:
            # if the section we're looking at is actually a hockey player (IDK why it would be)
            if section["title"] in ["Forwards", "Defenders", "Goalies"]:
                players += [player["row"] for player in section["data"]]

    return players

def get_games():
    # set up empty list for us to put our data in
    games = []

    url = f"https://lscluster.hockeytech.com/feed/index.php?feed=statviewfeed&view=schedule&team=-1&season={SEASON}&month=-1&location=homeaway&key=694cfeed58c932ee&client_code=pwhl&site_id=2&league_id=1&division_id=-1&lang=en"

    game_list = return_json(url)

    # if you look at what was returned, we want the data specifically in [sections][0][data]
    for game in game_list["sections"][0]["data"]:
        # format the date properly
        date_str = game["row"]["date_with_data"]
        datetime_str = datetime.datetime.strptime(date_str, "%a, %b %d")

        # formate the game status properly
        game_status = game["row"]["game_status"].split()

        # game statuses are "Final", "Final OT", "Final SO" etc so we want either "OT"/"SO" or "REG" if neither is there
        game_status = game_status[-1] if len(game_status) > 1 else "REG"

        game_list.append({
            "game_id": game["row"]["game_id"],
            "date": datetime_str,
            "home_team": game["prop"]["home_team_city"]["teamLink"],
            "visiting_team": game["prop"]["visiting_team_city"]["teamLink"],
            "season": SEASON,
            "venue": 0,
            "attendance": 0,
            "start_time": None,
            "end_time": None,
            "duration": None,
            "home_goals": game["row"]["home_goal_count"],
            "visiting_goals": game["row"]["visiting_goal_count"],
            "game_status": game_status
        })
