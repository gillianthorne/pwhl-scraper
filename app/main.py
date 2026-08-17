from app.scrape_data import get_players
import app.write_data as wd

def players():
    try:
        player_list = get_players()
        wd.write_players(player_list)
    except Exception as e:
        print("Couldn't write players")
        print(e)

def game():
    try:
        