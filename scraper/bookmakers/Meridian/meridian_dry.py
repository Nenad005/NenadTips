import json
import sys
sys.path.insert(1, '../')
from bookmaker import Bookmaker
import copy
from datetime import datetime
import time
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from seleniumwire.utils import decode
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
        self.driver = webdriver.Chrome(service= Service(executable_path=CHROME_DRIVER_PC), options=options)

    def load_mapping(self):
        with open("meridian_football_mapping.json", "r", encoding="utf-8") as mapping_file:
            self.mapping_data = json.load(mapping_file)

    def load_page(self):
        self.driver.get("https://meridianbet.rs/sr/kladjenje/fudbal")
        self.driver.execute_script('document.querySelector("body > app-root > main > main-app > div.l-main-content > sport-page > div > div.c-highlighted-section.c-highlighted-section--default > event-filters > div > div > div:nth-child(2) > div > div:nth-child(4)").click()')
        time.sleep(3)

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
    
    def get_odds_from_json(self, json_data, map, home, away):
        odds_data = {}

        def clean_text(text):
            """Remove extra spaces, newlines, and normalize text."""
            return re.sub(r"\s+", " ", text).strip()
        
        for entry in json_data.get("payload", []):
            game_id = entry.get("gameTemplateId")
            game_name = entry.get("marketName").replace(home, "Domacin").replace(away, "Gost")
            odds_data[game_name] = {}
            markets = entry.get("markets")

            for market in markets:
                overUnder = market.get("overUnder")
                selections = market.get("selections")
                if overUnder is None:
                    for selection in selections:
                        odds_data[game_name][selection["name"]] = selection["price"]
                else:
                    for selection in selections:
                        odds_data[game_name][f"{selection["name"]} {overUnder}"] = selection["price"]

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
    
    def string_to_date(self, date_string, time_string):
        current_year = datetime.now().year
        date = f"{time_string} {date_string}.{current_year}"
        date_format = "%H:%M %d.%m.%Y"
        date_object = datetime.strptime(date, date_format)
        
        # Adjust year if the date is more than 3 days ahead
        today = datetime.now()
        if abs((date_object - today).days) > 3:
            date_object = date_object.replace(year=current_year + 1)
        
        return date_object

    def get_odds_data_scrolled(self):
        count = self.driver.execute_script('return document.querySelectorAll("standard-event").length')
        print(f"Nasao : {count}")
        matches = {}

        for i in range(count):
            print(f"Scraping match {i+1} of {count}")
            try:
                # * get the time and date string from the element
                time_string = self.driver.execute_script(f'return document.querySelectorAll("standard-event")[{i}].querySelector(".c-event__period-time").textContent')
                date_string = self.driver.execute_script(f'return document.querySelectorAll("standard-event")[{i}].querySelector(".c-event__period-min").textContent')

                # * get the team names from the element
                home = self.driver.execute_script(f'return document.querySelectorAll("standard-event")[{i}].querySelector(".c-event__rivals--home").textContent').strip()
                away = self.driver.execute_script(f'return document.querySelectorAll("standard-event")[{i}].querySelector(".c-event__rivals--away").textContent').strip()

                # * click on the bet element
                command = f'return document.querySelectorAll("standard-event")[{i}].querySelector(".c-event__info").click()'
                self.driver.execute_script(command)


                # * wait for the odds to load
                # while self.driver.execute_script('return document.querySelector(".c-single-event-scoreboard__title")') == None:
                #     time.sleep(0.1)
                # time.sleep(0.8)

                # * get the competition name from the bet element
                comp_el = WebDriverWait(self.driver, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, "c-single-event-scoreboard__title")))
                competition = comp_el.text.strip()
                # competition = self.driver.execute_script('return document.querySelector(".c-single-event-scoreboard__title").textContent').strip()
                map = copy.deepcopy(self.mapping_data)

                # * get the match url and read the html
                match_url = self.driver.execute_script('return document.querySelector("a.c-single-event-scoreboard__cta-btn").href')
                date = self.string_to_date(date_string=date_string, time_string=time_string)
                print(date, home, away, competition, match_url, sep=" | ")

                map["teams"]["home"] = home
                map["teams"]["away"] = away
                map["competition"] = competition
                map["time"] = date.isoformat()
                map["match_url"] = match_url

                event_id = match_url.split("/")[-1]
                request_url = f"https://online.meridianbet.com/betshop/api/v2/events/{event_id}/markets?gameGroupId=all"

                matches[request_url] = map

            except Exception as e:
                print(e)
                continue
        time.sleep(5)
        print("Scrapped all matches, saving . . .")


        requests_map = {}
        for request in self.driver.requests:
            requests_map[request.url] = request

        for url in matches.keys():
            if url not in requests_map.keys():
                continue
            request = requests_map[url]
            if not hasattr(request.response, "body"):
                continue
            body = decode(request.response.body, request.response.headers.get("Content-Encoding", "identity"))
            json_data = json.loads(body.decode("utf-8"))
            self.get_odds_from_json(json_data=json_data, map=matches[url], home=matches[url]["teams"]["home"], away=matches[url]["teams"]["away"])
            
            self.upsert_match(matches[url])

        # time.sleep(5)
        # pattern = r'https:\/\/online\.meridianbet\.com\/betshop\/api\/v2\/events\/[0-9]*\/markets\?gameGroupId=all'
        # for request in self.driver.requests:
        #     if re.match(pattern, request.url):
        #         if not hasattr(request.response, "body"):
        #             continue
        #         map = copy.deepcopy(self.mapping_data)
        #         body = decode(request.response.body, request.response.headers.get("Content-Encoding", "identity"))
        #         json_data = json.loads(body.decode("utf-8"))
        #         odds = self.get_odds_from_json(json_data=json_data, map=map, home=home, away=away)

if __name__ == "__main__":
    bet = MeridianBet()
    bet.get_all_match_odds()