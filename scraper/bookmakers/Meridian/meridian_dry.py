import json
import sys
sys.path.insert(1, '../')
from bookmaker import Bookmaker
import copy
from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re

class MeridianBet(Bookmaker):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.mapping_data = None

    def get_all_match_odds(self):
        self.start_driver()
        self.start_db_session()

        self.load_mapping()
        self.load_page()
        self.scroll_to_bottom()
        self.get_odds_data_scrolled()

        self.close_db_session()
        self.close_driver()

    def get_collection_name(self):
        return "Meridian"

    def start_driver(self):
        CHROME_DRIVER_LAPTOP = 'C:/dev/Enterprise/NenadTips/scraper/chromedriver.exe'
        CHROME_DRIVER_PC = 'F:/dev/NenadTips/scraper/chromedriver.exe'
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service= Service(executable_path=CHROME_DRIVER_LAPTOP), options=options)

    def load_mapping(self):
        with open("meridian_football_mapping.json", "r", encoding="utf-8") as mapping_file:
            self.mapping_data = json.load(mapping_file)

    def load_page(self):
        self.driver.get("https://meridianbet.rs/sr/kladjenje/fudbal")
        time.sleep(2)
        self.driver.execute_script('document.querySelector("body > app-root > main > main-app > div.l-main-content > sport-page > div > div.c-highlighted-section.c-highlighted-section--default > event-filters > div > div > div:nth-child(2) > div > div:nth-child(4)").click()')
        time.sleep(1)

    def close_driver(self):
        self.driver.quit()

    def scroll_to_bottom(self):
        prev_children_count = -1
        same_count_times = 0
        self.driver.execute_script('document.querySelector("body > app-root > main > main-app > div.l-main-content > sport-page > div").scrollBy(0, 10000)')
        
        while same_count_times < 4:
            children_count = self.driver.execute_script('return document.querySelectorAll("standard-event").length')
            print(children_count)
            if children_count == prev_children_count:
                same_count_times += 1
            else:
                same_count_times = 0
            prev_children_count = children_count
            time.sleep(1)
    
    def get_odds_from_html(self, html_content, map):
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
            # print(instruction)
            cat = instruction[0]
            subcat = instruction[1]
            return odds_data.get(cat, {}).get(subcat, None)
        
        for cat in map["odds"].keys():
            for subcat in map["odds"][cat].keys():
                # print(map["odds"][cat][subcat])
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
        return map
    
    def string_to_date(self, date_string):
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

    def get_odds_data_scrolled(self):
        count = self.driver.execute_script('return document.querySelectorAll("standard-event").length')
        print(f"Nasa : {count}")
        # input()

        def wait_for_odds(loaded, timeout=500, interval=50):
            start_time = time.time() * 1000
            while (time.time() * 1000) - start_time < timeout:
                if self.driver.execute_script('return document.querySelectorAll("event-game").length') > loaded: return
                time.sleep(interval/1000)
            return 

        for i in range(count):
            # * get the time and date string from the element
            time_string = self.driver.execute_script(f'return document.querySelectorAll("standard-event")[{i}].querySelector(".c-event__period-time").textContent')
            date_string = self.driver.execute_script(f'return document.querySelectorAll("standard-event")[{i}].querySelector(".c-event__period-min").textContent')
            # input(f"{time_string} {date_string}")

            # * get the team names from the element
            home = self.driver.execute_script(f'return document.querySelectorAll("standard-event")[{i}].querySelector(".c-event__rivals--home").textContent').strip()
            away = self.driver.execute_script(f'return document.querySelectorAll("standard-event")[{i}].querySelector(".c-event__rivals--away").textContent').strip()
            # input(f"{home} {away}")


            # * click on the bet element
            command = f'return document.querySelectorAll("standard-event")[{i}].querySelector(".c-event__info").click()'
            self.driver.execute_script(command)


            # * wait for the odds to load
            while self.driver.execute_script('return document.querySelector(".c-single-event-scoreboard__title")') != None:
                time.sleep(0.1)

            # input()

            # time.sleep(0.1)
            # * get the competition name from the bet element
            # competiton = self.driver.execute_script('return document.querySelector(".c-single-event-scoreboard__title").textContent').strip()

            competition = ""
            print(f"{home} {away} {date_string} {time_string} {competition}")

            # * start loading all odds and wait for them to load
            loaded = self.driver.execute_script('return document.querySelectorAll("event-game").length')
            self.driver.execute_script('document.querySelectorAll(".c-basic-slider-item--without-margin")[document.querySelectorAll(".c-basic-slider-item--without-margin").length -1].click()')
            wait_for_odds(loaded, 600, 50)

            # TODO get the odds html from the bet element
            odds_element = self.driver.execute_script('return document.querySelector("ds-match-special-bet > div > div")')
            if odds_element is None:
                continue
            else:
                odds_html = self.driver.execute_script('return document.querySelector("ds-match-special-bet > div > div").innerHTML')
            map = copy.deepcopy(self.mapping_data)
            # odds = self.get_odds_from_html(html_content=odds_html, map=map)
            # ! above not done

            #get the match url and read the html
            match_url = self.driver.execute_script('return document.querySelector("a.c-single-event-scoreboard__cta-btn").href')
            date = self.string_to_date(time_string, date_string)
            print(date, home, away, competition, match_url, sep=" | ")

            map["teams"]["home"] = home
            map["teams"]["away"] = away
            map["competition"] = competition
            map["time"] = date.isoformat()
            map["match_url"] = match_url

            self.upsert_match(match_data=map)

if __name__ == "__main__":
    bet = MeridianBet()
    bet.get_all_match_odds()