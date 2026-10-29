import requests
import json
import datetime
import math
import app.config as config
import app.utils as utils
import app.read_db as rd

def return_json(url):
    # since this is literally just json, no need for beautifulsoup. just requests.get and go
    response = requests.get(url)
    # okay it isn't parsed as json: it's stored in round brackets. this strips it of them.
    data = response.text[1:-1]
    # and make it a dict for us to use!
    # using try/catch because some game data returns an empty page which errors out
    try:
        data = json.loads(data)
    except Exception as err:
        print(err)
        print(url)
    return data


def get_players():
    # set up empty lists for us to put our data in temporarily
    players = []

    # we're counting through each team, with +1 because python goes up to but not including the second number
    for i in range(1, config.MAX_TEAM_ID + 1):
        # this is the ugly ugly url that we're getting data from
        url = f"https://lscluster.hockeytech.com/feed/index.php?feed=statviewfeed&view=roster&team_id={i}&season_id={config.SEASON}&key=446521baf8c38984&client_code=pwhl&site_id=0&league_id=1&lang=en"
        
        roster = return_json(url)

        # the path to the actual data is janky, but this is it
        for section in roster["roster"][0]["sections"]:
            # if the section we're looking at is actually a hockey player (IDK why it would be)
            if section["title"] in ["Forwards", "Defenders", "Goalies"]:
                players += [player["row"] for player in section["data"]]

    return players

def get_games():
    # set up empty dict for us to put our data in
    games = {}

    try:
        url = f"https://lscluster.hockeytech.com/feed/index.php?feed=statviewfeed&view=schedule&team=-1&season={config.SEASON}&month=-1&location=homeaway&key=694cfeed58c932ee&client_code=pwhl&site_id=2&league_id=1&division_id=-1&lang=en"

        game_list = return_json(url)

        # we'll need venue data later
        venues = rd.get_venues()

        # if you look at what was returned, we want the data specifically in [sections][0][data]
        for game in game_list[0]["sections"][0]["data"]:
            # format the date properly
            # date_str = game["row"]["date_with_day"]

            # formate the game status properly
            win_type = game["row"]["game_status"].split()[-1]

            # if win_type = "Final" turn it into "REG" for regulation
            if win_type == "Final":
                win_type = "REG"
            
            date_str = game["row"]["date_with_day"]

            games[game["row"]["game_id"]] = {
                "game_id": game["row"]["game_id"],
                "date": utils.parse_date(date_str),
                "home_team": game["prop"]["home_team_city"]["teamLink"],
                "visiting_team": game["prop"]["visiting_team_city"]["teamLink"],
                "season": config.SEASON,
                "venue": 0,
                "attendance": 0,
                "start_time": None,
                "end_time": None,
                "duration": None,
                "home_goals": game["row"]["home_goal_count"],
                "visiting_goals": game["row"]["visiting_goal_count"],
                "win_type": win_type
            }
    except TypeError as err:
        print(f"Error: {err}")
        print("This typically is a game not found error, which is expected if the game_id is not valid. This is normal behavior for the scraper.")
    except Exception as err:
        print(f"Error: {err}")
        print("This is an unexpected error. Please check the URL and the data returned.")
        print("URL: ", url)
        print("Game list: ", game_list)

    # we're using another page now for the rest of the data
    for i in range(config.MIN_GAME, config.MAX_GAME + 1):
        # initialize a blank dict, i like this more than creating a large one at the end
        
        try:
            url = f"https://lscluster.hockeytech.com/feed/index.php?feed=statviewfeed&view=gameSummary&game_id={i}&key=694cfeed58c932ee&site_id=2&client_code=pwhl&lang=en&league_id="        
            game = return_json(url)["details"]

            game_id = str(game["id"]).strip()

            # check if start_time is am or pm
            if game["startTime"][-6:-4] == "PM":
                start_time = utils.parse_game_time(game["startTime"][:-7], "pm")
            else:
                start_time = utils.parse_game_time(game["startTime"][:-7], "am")


            # check if end_time is am or pm
            if game["endTime"][-6:-4] == "PM":
                end_time = utils.parse_game_time(game["endTime"][:-7], "pm")
            else:
                end_time = utils.parse_game_time(game["endTime"][:-7], "am")

            try:
                games[game_id]["game_id"] = game["id"]
                # games[game_id]["venue"] = venues[game["venue"].split("|")[0].strip()]
                games[game_id]["attendance"] = game["attendance"]
                games[game_id]["start_time"] = start_time
                games[game_id]["end_time"] = end_time
                games[game_id]["duration"] = utils.parse_duration(game["duration"])

            # sometimes the pwhl skips games or orders them weirdly, this should account for that
            except KeyError as err:
                print(f"Error: Game {err} does not exist. (KeyError)")
            except Exception as err:
                print(f"Error: {err}")
                print("This is an unexpected error. Please check the URL and the data returned.")
                print("URL: ", url)
                print("Game data: ", game)
        # sometimes it'll try to get a game and mistake the error code for a game, this should account for that
        except TypeError as err:
            print(f"Error: Game {err} does not exist. (TypeError)")
        except Exception as err:
            print(f"Error: {err}")
            print("This is an unexpected error. Please check the URL and the data returned.")
            print("URL: ", url)
            print("Game data: ", game)
    return games

def get_game_events():
    # a nice structured dict to return all game data
    # then in write_data i can separate each event
    events = {
        "goalie_changes": [],
        "faceoffs": [],
        "shots": [],
        "goals": [],
        "assists": [],
        "plus_minus": [],
        "penalties": [],
        "hits": [],
        "blocked_shots": [],
        "shootouts": [],
        "penalty_shots": []
    }

    for i in range(config.MIN_GAME, config.MAX_GAME):
        try:
            url = f"https://lscluster.hockeytech.com/feed/index.php?feed=statviewfeed&view=gameCenterPlayByPlay&game_id={i}&key=694cfeed58c932ee&client_code=pwhl&lang=en&league_id="
            game = return_json(url)
        except Exception as e:
            print(f"Error occurred while fetching game {i}: {e}")
            continue

        # init shootout_counter at 1 so when the first shot is taken, it will be 1 and not 0 - purely personal preference bc i know programming languages start at 0 so i could follow that standard
        # just makes it more readable if i ever get around to sharing my data
        shootout_counter = 1

        for event in game:
            # general structure for this is:
                # 1. figure out what the event type is
                # 2. get the details for the event
                # 3. do any additional logic, such as goalie_change
                # 4. write it to a structured dict with each field in the database table
                # 5. repeat until all events are parsed

            if event["event"] == "goalie_change":
                goalie_change = event["details"]
                # json labels are slightly different depending on if a goalie is entering or exiting so i have to get those two first
                if goalie_change["goalieGoingOut"]:
                    out = True
                    player_id = goalie_change["goalieGoingOut"]["id"]
                else:
                    out = False
                    player_id = goalie_change["goalieComingIn"]["id"]

            
                events["goalie_changes"].append({
                    "game_id": i,
                    "player_id": player_id,
                    "period": goalie_change["period"]["id"],
                    "time": utils.format_time(goalie_change["time"]),
                    "entering": out
                })

            if event["event"] == "faceoff":
                faceoff = event["details"]
                events["faceoffs"].append({
                    "game_id": i,
                    "home_player_id": faceoff["homePlayer"]["id"],
                    "visiting_player_id": faceoff["visitingPlayerId"]["id"],
                    "period": faceoff["period"]["id"],
                    "time": utils.format_time(faceoff["time"]),
                    "x_location": faceoff["xLocation"],
                    "y_location": faceoff["yLocation"],
                    "home_win": faceoff["homeWin"]
                })

            if event["event"] == "shot":
                shot = event["details"]
                events["shots"].append({
                    "game_id": i,
                    "shooter_id": shot["shooter"]["id"],
                    "goalie_id": shot["goalie"]["id"],
                    "period": shot["period"]["id"],
                    "time": utils.format_time(shot["time"]),
                    "is_goal": shot["isGoal"],
                    "x_location": shot["xLocation"],
                    "y_location": shot["yLocation"],
                    "type": shot["shotType"],
                    "quality": shot["shotQuality"]
                })

            if event["event"] == "goal":
                goal = event["details"]
                properties = goal["properties"]
                events["goals"].append({
                    "game_id": i,
                    "scorer_id": goal["scorer"]["id"],
                    "goal_id": goal["game_goal_id"],
                    "period": goal["period"]["id"],
                    "time": utils.format_time(goal["time"]),
                    "is_powerplay": properties["isPowerplay"],
                    "is_shorthanded": properties["isEmptyNet"],
                    "is_insurancegoal": properties["isInsuranceGoal"],
                    "is_gamewinninggoal": properties["isGameWinningGoal"],
                    "is_penaltyshot": properties["isPenaltyShot"],
                    "x_location": goal["xLocation"],
                    "y_location": goal["yLocation"]
                })

                # this ties back to the powerplay thing - i wanted primary/secondary to be 1/2 for ease of reading, so therefore index+1
                for index, assist in enumerate(goal["assists"]):
                    events["assists"].append({
                        "goal_id": goal["game_goal_id"],
                        "player_id": assist["id"],
                        "primary_secondary": index + 1
                    })

                for plus in goal["plus_players"]:
                    events["plus_minus"].append({
                        "goal_id": goal["game_goal_id"],
                        "player_id": plus["id"],
                        "is_plus": True
                    })

                for minus in goal["minus_players"]:
                    events["plus_minus"].append({
                        "goal_id": goal["game_goal_id"],
                        "player_id": minus["id"],
                        "is_plus": False
                    })

            if event["event"] == "penalty":
                penalty = event["details"]
                events["penalties"].append({
                    "game_id": i,
                    "taken_by_id": penalty["takenBy"]["id"],
                    "served_by_id": penalty["servedBy"]["id"],
                    "team_id": penalty["againstTeam"]["id"],
                    "penalty_id": penalty["game_penalty_id"],
                    "description": penalty["description"],
                    "period": penalty["period"]["id"],
                    "time": utils.format_time(penalty["time"]),
                    "length": penalty["minutes"],
                    "is_powerplay": penalty["isPowerPlay"],
                    "is_bench": penalty["isBench"]
                })

            if event["event"] == "hit":
                hit = event["details"]
                # sometimes it errors out because there is no onPlayer
                try:
                    on_player = hit["onPlayer"]["id"]
                except TypeError:
                    on_player = 0

                events["hits"].append({
                    "game_id": i,
                    "player_id": hit["player"]["id"],
                    "period": hit["period"]["id"],
                    "time": utils.format_time(hit["time"]),
                    "x_location": hit["xLocation"],
                    "y_location": hit["yLocation"],
                    "on_player_id": on_player
                })

            if event["event"] == "blocked_shot":
                blocked_shot = event["details"]
                events["blocked_shots"].append({
                    "game_id": i,
                    "shooter_id": blocked_shot["shooter"]["id"],
                    "blocker_id": blocked_shot["blocker"]["id"],
                    "goalie_id": blocked_shot["goalie"]["id"],
                    "period": blocked_shot["period"]["id"],
                    "time": utils.format_time(blocked_shot["time"]),
                    "x_location": blocked_shot["xLocation"],
                    "y_location": blocked_shot["yLocation"],
                    "type": blocked_shot["type"],
                    "quality": blocked_shot["shotQuality"]
                })

            if event["event"] == "shootout":
                shootout = event["details"]
                events["shootouts"].append({
                    "game_id": i,
                    "shooter_id": shootout["shooter"]["id"],
                    "goalie_id": shootout["goalie"]["id"],
                    "is_goal": shootout["isGoal"],
                    "is_gwg": shootout["isGameWinningGoal"],
                    # math.ceil(shootout_counter/2) allows for two shooutouts to each count - one per team
                    "shootout_attempt": math.ceil(shootout_counter/2)
                })

                shootout_counter += 1

            if event["event"] == "penalty_shot":
                penalty_shot = event["details"]
                events["penalty_shots"].append({
                    "game_id": i,
                    "shooter_id": penalty_shot["shooter"]["id"],
                    "goalie_id": penalty_shot["goalie"]["id"],
                    "period": penalty_shot["period"]["id"],
                    "time": utils.format_time(penalty_shot["time"]),
                    "is_goal": penalty_shot["isGoal"]
                })