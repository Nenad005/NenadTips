import json
import requests

r = requests.post('http://localhost:8000/https://www.mozzartbet.com/matchBetting', json={"id": 7855653}, headers={"X-Requested-With": "XMLHttpRequest"})
jsonData = r.json()

# print(jsonData)
kodds = jsonData['kodds']
result_dict = {}

for element in kodds:
    # print(element)
    game = kodds[element]['subGame']['gameName']
    subGame = kodds[element]['subGame']['subGameName']
    # print(game, subGame)
    if not game in result_dict:
        result_dict[game] = {}
    result_dict[game][subGame] = element

with open("mozzart_football_mapping.json", "w", encoding="utf-8") as json_file:
    json.dump(result_dict, json_file, indent=4, ensure_ascii=False)