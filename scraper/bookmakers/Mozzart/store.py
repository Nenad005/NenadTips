import json
import copy
from datetime import datetime

with open ('mozzart.json', 'r') as file:
    data = json.load(file)

with open ("mozzart_football_mapping.json", "r") as file:
    mapping = json.load(file)

items = data["items"]
for item in items:
    home = item["home"]["name"]
    away = item["visitor"]["name"]
    competition = item["competition"]["name"]
    time = item["startTime"]
    time = datetime.fromtimestamp(time / 1000).isoformat()
    match_url = "https://www.mozzartbet.com/sr/kladjenje/sport/1/match/" + str(item["id"])

    print(home, away, competition)

    if "odds" not in item.keys():
        continue

    odds = item["odds"]
    odds_data = {}
    for odd in odds:
        odds_data[odd["id"]] = {
            "group": odd["game"]["name"],
            "name": odd["subgame"]["name"],
            "value": odd["value"]
        }

    # print(json.dumps(odds_data, indent=4))
    map = copy.deepcopy(mapping)

    map["teams"]["home"] = home
    map["teams"]["away"] = away
    map["competition"] = competition
    map["time"] = time
    map["match_url"] = match_url
    for cat in map["odds"].keys():
        for subcat in map["odds"][cat].keys():
            print(map["odds"][cat][subcat])
            for odd in map["odds"][cat][subcat]:
                x = map["odds"][cat][subcat][odd]

                if isinstance(x, dict):
                    for subodd in x.keys():
                        if x[subodd] is None:
                            continue
                        else:
                            map["odds"][cat][subcat][odd][subodd] = odds_data[x[subodd]]["value"]

                elif x is None:
                    continue
                else:
                    map["odds"][cat][subcat][odd] = odds_data[x]["value"]

    print(json.dumps(map, indent=4))
    # input()

    with open(f"rezultati/{home}_{away}.json", "w") as file:
        file.write(json.dumps(map, indent=4))

print(len(items))