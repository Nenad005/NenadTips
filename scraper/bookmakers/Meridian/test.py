import json

# Load the JSON file
with open("response.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Dictionary to store extracted data
games = {}

# Extract gameTemplateIds and selectionIds
for league in data:
    for event in league["events"]:
        for position in event["positions"]:
            for group in position["groups"]:
                game_template_id = None
                game_name = group.get("name", "Unknown")
                
                for selection in group["selections"]:
                    game_template_id = selection["gameTemplateId"]
                    selection_id = selection["selectionId"]
                    selection_name = selection["name"]
                    
                    if game_template_id not in games:
                        games[game_template_id] = {
                            "game_name": game_name,
                            "selections": {}
                        }
                    
                    games[game_template_id]["selections"][selection_id] = selection_name

# Save extracted data to a JSON file
output_path = "extracted_games.json"
with open(output_path, "w", encoding="utf-8") as outfile:
    json.dump(games, outfile, indent=4, ensure_ascii=False)

print(f"Extracted data saved to {output_path}")