from bs4 import BeautifulSoup
import json
import re

# Load the HTML file
html_file_path = "odds.html"

with open(html_file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML
soup = BeautifulSoup(html_content, "html.parser")

# Extract groups
groups = soup.find_all("ds-prematch-special-group")

odds_data = {}

def clean_text(text):
    """Remove extra spaces, newlines, and normalize text."""
    return re.sub(r"\s+", " ", text).strip()

for group in groups:
    group_name_tag = group.find("span", class_="match-special-bet-pick-group-name")
    group_name = clean_text(group_name_tag.get_text()) if group_name_tag else "Unknown Group"

    odds = {}
    odds_buttons = group.find_all("button", class_="odd-btn odd-prematch")

    for button in odds_buttons:
        odd_label_tag = button.find("span", class_="odd-btn--tip")
        odd_value_tag = button.find("span", class_="odd-btn--odd")

        if odd_label_tag and odd_value_tag:
            odd_label = clean_text(odd_label_tag.get_text())
            odd_value = clean_text(odd_value_tag.get_text())

            # Ensure the odd value is a float
            try:
                odds[odd_label] = float(odd_value)
            except ValueError:
                continue  # Ignore non-numeric odds

    if odds:
        odds_data[group_name] = odds

# Save to a JSON file
# Load the mapping JSON file
with open("soccer_football_mapping.json", "r", encoding="utf-8") as mapping_file:
    mapping_data = json.load(mapping_file)

def get_odd_from_instruction(instruction):
    print(instruction)
    cat = instruction[0]
    subcat = instruction[1]
    return odds_data.get(cat, {}).get(subcat, None)

for cat in mapping_data["odds"].keys():
        for subcat in mapping_data["odds"][cat].keys():
            print(mapping_data["odds"][cat][subcat])
            for odd in mapping_data["odds"][cat][subcat]:
                x = mapping_data["odds"][cat][subcat][odd]

                if isinstance(x, dict):
                    for subodd in x.keys():
                        if x[subodd] is None:
                            continue
                        else:
                            mapping_data["odds"][cat][subcat][odd][subodd] = get_odd_from_instruction(mapping_data["odds"][cat][subcat][odd][subodd])

                elif x is None:
                    continue
                else:
                    mapping_data["odds"][cat][subcat][odd] = get_odd_from_instruction(mapping_data["odds"][cat][subcat][odd])

# Save the extracted odds to a JSON file
json_file_path = "odds.json"
with open(json_file_path, "w", encoding="utf-8") as json_file:
    json.dump(mapping_data, json_file, indent=4)

print(f"Odds extracted and saved to {json_file_path}")
