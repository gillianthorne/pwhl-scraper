from app.scrape_data import get_players
from app.write_data import write_players

def players():
    try:
        player_list = get_players()
        write_players(player_list)
    except Exception as e:
        print("Couldn't write players")
        print(e)