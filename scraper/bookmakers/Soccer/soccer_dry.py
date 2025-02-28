from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
from bs4 import BeautifulSoup
import json
import copy
import re

CHROME_DRIVER_LAPTOP = 'C:/dev/Enterprise/NenadTips/scraper/chromedriver.exe'
CHROME_DRIVER_PC = 'F:/dev/NenadTips/scraper/chromedriver.exe'

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service= Service(executable_path=CHROME_DRIVER_LAPTOP), options=options)
driver.get("https://www.soccerbet.rs/sr/sportsko-kladjenje/fudbal/S")
time.sleep(5)
driver.execute_script('document.querySelector("body > app-root > ng-component > ion-app > div > ds-main-layout > ds-main-layout-desktop > ion-row > ion-row > div.DESK-content--center > ion-router-outlet > ds-offer > ion-content > ds-offer-landing > ds-offer-landing-desk > ds-offer-type-filter > ion-row > ion-button.offer-type-filter--btn.offer-type-filter--btn-calendar.ion-color.ion-color-clear.ios.button.button-solid.ion-activatable.ion-focusable.hydrated").shadowRoot.querySelector("button").click()')
time.sleep(1)
driver.execute_script('document.querySelector("body > app-root > ng-component > ion-app > div > ds-main-layout > ds-main-layout-desktop > div > ion-row > ds-time-offer-filter > ion-row > ion-button:nth-child(4)").shadowRoot.querySelector("button").click()')
time.sleep(1)


# Load the mapping JSON file
with open("soccer_football_mapping.json", "r", encoding="utf-8") as mapping_file:
    mapping_data = json.load(mapping_file)

# Scroll to the bottom of the page
def scroll_to_bottom(driver):
    prev_children_count = -1
    same_count_times = 0
    
    while same_count_times < 8:
        children_count = driver.execute_script('return document.querySelector("body > app-root > ng-component > ion-app > div > ds-main-layout > ds-main-layout-desktop > ion-row > ion-row > div.DESK-content--center > ion-router-outlet > ds-offer > ion-content > ds-offer-landing > ds-offer-landing-desk > div:nth-child(4) > ds-matches-by-time-container").children.length')
        print(children_count)
        if children_count == prev_children_count:
            same_count_times += 1
        else:
            same_count_times = 0
        prev_children_count = children_count
        driver.execute_script('document.querySelector("body > app-root > ng-component > ion-app > div > ds-main-layout > ds-main-layout-desktop > ion-row > ion-row > div.DESK-content--center > ion-router-outlet > ds-offer > ion-content").scrollByPoint(1000, 1000)')
        time.sleep(1)

        if (prev_children_count > 20):
            return

scroll_to_bottom(driver)

# count the number of bet elements
count = driver.execute_script('return document.querySelectorAll("ds-prematch-top").length')
print(count)

def string_to_date(date_string):
    parts = date_string.strip().split()
    current_year = datetime.now().year
    date = f"{parts[0]} {parts[2]}{current_year}"
    date_format = "%H:%M %d.%m.%Y"
    date_object = datetime.strptime(date, date_format)
    
    # Adjust year if the date is more than 3 days ahead
    today = datetime.now()
    if abs((date_object - today).days) > 3:
        date_object = date_object.replace(year=current_year + 1)
    
    return date_object

def get_odds_from_html(html_content, map):
    soup = BeautifulSoup(html_content, "html.parser")

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

    def get_odd_from_instruction(instruction):
        print(instruction)
        cat = instruction[0]
        subcat = instruction[1]
        return odds_data.get(cat, {}).get(subcat, None)
    

    
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
                            map["odds"][cat][subcat][odd][subodd] = get_odd_from_instruction(map["odds"][cat][subcat][odd][subodd])

                elif x is None:
                    continue
                else:
                    map["odds"][cat][subcat][odd] = get_odd_from_instruction(map["odds"][cat][subcat][odd])
    
    # with open("odds.json", "w") as file:
    #     file.write(json.dumps(odds_data, indent=4))
    return map

# iterate through the bet elements
for i in range(count):
    #get the time text from the bet element
    time_html = driver.execute_script(f'return document.querySelector("ds-prematch-top:nth-child({i+2}) .es-match-kickoff").textContent')

    #get the teams text from the bet element
    teams_text = driver.execute_script(f'return document.querySelector("ds-prematch-top:nth-child({i+2}) .es-match-teams").innerText').split("\n")

    #get the competition name from the bet element
    competition_text = driver.execute_script(f'return document.querySelector("ds-prematch-top:nth-child({i+2}) .prematch-top-desk--league-info").textContent')

    #click on the bet element
    command = f'document.querySelector("ds-prematch-top:nth-child({i+2}) > ds-prematch-top-desk > ion-item-sliding > ion-item > ion-grid > ion-row > ion-row.prematch-top-desk--left-content.ios.hydrated").click()'
# print(command)
    driver.execute_script(command)

    #wait for the odds to load
    time.sleep(1)

    #scroll to the bottom of the page
    for i in range(5):
        driver.execute_script('document.querySelector("#pmSpecialContainer > div > ds-match-special-bet > div").scrollBy(10000, 10000)')
        time.sleep(0.2)

    #get the odds html from the bet element
    odds_html = driver.execute_script('return document.querySelector("ds-match-special-bet > div > div").innerHTML')
    map = copy.deepcopy(mapping_data)
    odds = get_odds_from_html(odds_html, map)

    #get the match url and read the html
    match_url = driver.current_url
    date = string_to_date(time_html)
    home = teams_text[0]
    away = teams_text[1]
    print(date, home, away, competition_text, match_url, sep=" | ")

    map["teams"]["home"] = home
    map["teams"]["away"] = away
    map["competition"] = competition_text.strip()
    map["time"] = date.isoformat()
    map["match_url"] = match_url

    with open(f"rezultati/{home}_{away}.json", "w") as file:
        file.write(json.dumps(map, indent=4))

    # input()

input()
driver.close()