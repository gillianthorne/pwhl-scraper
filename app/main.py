from app.scrape_data import get_game_events, get_games, get_players
import app.write_data as wd
from app.utils import format_exception


# same structure for all tables:
    # 1. get list of data
    # 2. write to database (as many times as needed)
    # 3. if either of those error out, don't break but instead print to console
    # (this will be run in cron with an output being emailed to me nightly, so i will be checking)
def players():
    try:
        player_list = get_players()
        wd.write_players(player_list)
    except Exception as e:
        print("Couldn't write players")
        print(e)
        print("stack trace:")
        print(format_exception(e))
        print("occurred on line {}".format(e.__traceback__.tb_lineno))

# i want to update this one to merge the two game dicts i had into one so it isn't an insert-update situation
def games():
    try:
        games_list = get_games()
        wd.write_games(games_list.values())
    except Exception as e:
        print("Couldn't write games")
        print(e)
        print("stack trace:")
        print(format_exception(e))
        print("occurred on line {}".format(e.__traceback__.tb_lineno))

def game_events():
    try:
        game_events_list = get_game_events()
        wd.write_goalie_changes(game_events_list["goalie_changes"])
        wd.write_faceoffs(game_events_list["faceoffs"])
        wd.write_shots(game_events_list["shots"])
        wd.write_goals(game_events_list["goals"])
        wd.write_assists(game_events_list["assists"])
        wd.write_plusminus(game_events_list["plus_minus"])
        wd.write_penalty(game_events_list["penalties"])
        wd.write_hits(game_events_list["hits"])
        wd.write_blocked_shots(game_events_list["blocked_shots"])
        wd.write_shootouts(game_events_list["shootouts"])
        wd.write_penalty_shots(game_events_list["penalty_shots"])
    except Exception as e:
        print("Couldn't write game events")
        print(e)
        print("stack trace:")
        print(format_exception(e))
        print("occurred on line {}".format(e.__traceback__.tb_lineno))

if __name__ == "__main__":
    players()
    games()
    game_events()