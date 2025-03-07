import json
from bs4 import BeautifulSoup
import re

# Load HTML content
with open('odds.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Nottingham Forest vs Manchester City
home = "Nottingham Forest"
away = "Manchester City"

soup = BeautifulSoup(html_content, 'html.parser')

result = {}

# Find all event-game elements
for event_game in soup.find_all('event-game'):
    # Extract group name
    def clean_text(text):
            """Remove extra spaces, newlines, and normalize text."""
            return re.sub(r"\s+", " ", text).strip()
    name_label = event_game.find(class_='c-single-event__game-name-label')
    if not name_label:
        continue
    group_name = clean_text(name_label.get_text(strip=True)).replace(home, "Domacin").replace(away, "Gost") # Extract only main category
    
    # Find game container
    game_container = event_game.find(class_='c-single-event__game')
    if not game_container:
        continue
    
    selections = {}
    # Process each game-inner section
    for game_inner in game_container.find_all(class_='c-single-event__game-inner'):
        OU = False
        limit_title = game_inner.find(class_='c-single-event-limit__title')
        if limit_title:
            title = clean_text(limit_title.get_text(strip=True))
            if title == 'O/U':
                OU = True
                limit = game_inner.find(class_='c-single-event-limit__value')
                if limit:
                    limit_value = clean_text(limit.get_text(strip=True))
        
        for selection in game_inner.find_all(class_='c-single-event__selection'):
            # Skip disabled selections if needed (remove this check to include them)
            if 'c-single-event__selection--disabled' in selection.get('class', []):
                continue
            
            name = selection.find(class_='c-selection__name')
            odd = selection.find(class_='c-selection__odd')
            
            if name and odd:
                if OU:
                    key = clean_text(name.get_text(strip=True)) + f" {limit_value}"
                    value = odd.get_text(strip=True)
                    print(key, value)
                    selections[key] = value
                else:
                    selections[clean_text(name.get_text(strip=True))] = odd.get_text(strip=True)

    # if OU:
    #     print(selections)
    
    if selections:  # Only add non-empty selections
        result[group_name] = selections

# Save to JSON
with open('odds.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print('Odds saved to odds.json')
