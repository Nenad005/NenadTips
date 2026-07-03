import json
from seleniumwire.utils import decode

import json
import sys

# with open("network_logs.json", "r", encoding="utf-8") as f:
#     json_data = json.loads(f.read())
#     print(json.dumps(json_data["payload"]["games"], indent=4))


with open("network_logs.json", "r", encoding="utf-8") as file:
    data = json.load(file)

domacin = "West Ham United"
gost = "Newcastle United"

odds = {}

for entry in data.get("payload", []):
    game_id = entry.get("gameTemplateId")
    game_name = entry.get("marketName").replace(domacin, "Domacin").replace(gost, "Gost")
    odds[game_name] = {}
    markets = entry.get("markets")

    for market in markets:
        overUnder = market.get("overUnder")
        selections = market.get("selections")
        if overUnder is None:
            for selection in selections:
                odds[game_name][selection["name"]] = selection["price"]
        else:
            for selection in selections:
                odds[game_name][f"{selection["name"]} {overUnder}"] = selection["price"]


# Save the extracted data to a JSON file
output_path = "extracted_game_data.json"
with open(output_path, "w", encoding="utf-8") as outfile:
    json.dump(odds, outfile, indent=4, ensure_ascii=False)

print(f"Extracted data saved to {output_path}")

