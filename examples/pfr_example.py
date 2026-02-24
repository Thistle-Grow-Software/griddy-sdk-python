import json

from griddy.core.utils.serializers import DateTimeEncoder
from griddy.pfr.parsers.player_profile import PlayerProfileParser

with open("data/pfr_examples/BradTo00_QB.htm", "r") as infile:
    html = infile.read()


parser = PlayerProfileParser()
player_data = parser.parse(html=html)

with open("tom_brady.json", "w") as outfile:
    json.dump(player_data, outfile, indent=4, cls=DateTimeEncoder)
