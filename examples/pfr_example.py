import json

from griddy.pfr import GriddyPFR

game_id = "201509100nwe"
pfr = GriddyPFR()
game_details = pfr.games.get_game_details(game_id=game_id)

with open("pfr_game_dtls.json", "w") as outfile:
    json.dump(game_details, outfile, indent=4)
