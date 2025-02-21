import json

# Load the mozzart.json file
with open('mozzart.json', 'r') as file:
    data = json.load(file)

# Extract the dictionary from the JSON data
# Assuming the dictionary is stored under a key named 'dict_key'
items = data["items"]
print(len(items))
data = []
for item in items:
    competition = item["competition"]["name"]
    home = item["home"]["name"]
    away = item["visitor"]["name"]
    if "odds" not in item.keys():
        print(competition, home, away)
        continue
    odds = item["odds"]
    odds_data = []

    for odd in odds:
        odds_data.append({
            odd["id"]: {
                "group": odd["game"]["name"],
                "name": odd["subgame"]["name"],
                "value": odd["value"]
            }
        })

    data.append({
        "competition": competition,
        "home": home,
        "away": away,
        "odds": odds_data
    })

print(len(data))
# Save the dictionary as a new JSON file
with open('test.json', 'w') as file:
    json.dump(data, file, indent=4)