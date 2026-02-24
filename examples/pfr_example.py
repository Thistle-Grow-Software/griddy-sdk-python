import json
from pathlib import Path

from griddy.core.utils.serializers import DateTimeEncoder
from griddy.pfr.parsers.player_profile import PlayerProfileParser

input_html_dir = Path("data/pfr_examples/")

parser = PlayerProfileParser()
for infile in input_html_dir.glob("*.htm"):
    print(f"Working on {infile}")
    html = infile.open().read()
    player_data = parser.parse(html=html)

    with open(f"{infile.parent}/{infile.stem}.json", "w") as outfile:
        json.dump(player_data, outfile, indent=4, cls=DateTimeEncoder)
