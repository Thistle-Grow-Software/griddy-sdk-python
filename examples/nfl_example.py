"""Example script for testing all NGS SDK methods."""

import json
import sys
from pprint import pprint

from griddy.nfl import GriddyNFL
from griddy.settings import NFL

_, *args = sys.argv

#
# # Lamar Jackson = 46101
if len(args) == 1:
    with open(args[0], "r") as infile:
        custom_auth_info = json.load(infile)
    nfl = GriddyNFL(nfl_auth=custom_auth_info)
else:
    nfl = GriddyNFL(
        login_email=NFL["login_email"], login_password=NFL["login_password"]
    )

# 2015 Week 01 Pittsburgh at New England
game_id = "10012015-0910-001f-0988-f51e8eea770e"
# Pittsburgh ID
pit_id = "10403900-8251-6892-d81c-4348525c2d47"
# New England ID
nwe_id = "10403200-69ab-9ea6-5af5-e240fbc08bea"
# play_list_response = nfl.pro_games.get_playlist(game_id=str(game_id))
# plays_as_json = [p.model_dump() for p in play_list_response.plays]
from pprint import pprint

team_stats = nfl.football_stats.live.get_team_statistics(game_id=game_id)
player_stats = nfl.football_stats.live.get_player_statistics(game_id=game_id)

all_stats = {"team": team_stats.model_dump(), "player": player_stats.model_dump()}

with open("live_stats_responses.json", "w") as outfile:
    json.dump(all_stats, outfile, indent=4)
