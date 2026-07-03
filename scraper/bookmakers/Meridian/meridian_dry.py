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
        self.driver = webdriver.Chrome(service= Service(executable_path=CHROME_DRIVER_LAPTOP), options=options)

    def load_mapping(self):
        with open("meridian_football_mapping.json", "r", encoding="utf-8") as mapping_file:
            self.mapping_data = json.load(mapping_file)

    def load_page(self):
        self.driver.get("https://meridianbet.rs/sr/kladjenje/fudbal")
        self.driver.execute_script('document.querySelector("body > app-root > main > main-app > div.l-main-content > sport-page > div > div.c-highlighted-section.c-highlighted-section--default > event-filters > div > div > div:nth-child(2) > div > div:nth-child(5)").click()')
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
        
        # with open("example.json", "w", encoding="utf-8") as f:
        #     json.dump(odds_data, f, indent=4)
        
        # input()
        
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

    def get_odds_data_scrolled(self):
        count = self.driver.execute_script('return document.querySelectorAll("standard-event").length')
        print(f"Nasao : {count}")
        matches = {}

        for i in range(count):
            print(f"Scraping match {i+1} of {count}")
            try:
                # * click on the bet element
                command = f'return document.querySelectorAll("standard-event")[{i}].querySelector(".c-event__info").click()'
                self.driver.execute_script(command)

                time.sleep(0.2)

            except Exception as e:
                print(e)
                continue
        time.sleep(10)
        print("Scrapped all matches, saving . . .")

        requests_map = {}
        for request in self.driver.requests:
            requests_map[request.url] = request

        match_urls = [request.url for request in self.driver.requests if "https://online.meridianbet.com/betshop/api/v2/events/" in request.url and "markets?gameGroupId=all" not in request.url]
        print(*match_urls, sep="\n")
        print(f"\n\n{len(match_urls)}\n\n")

        for url in match_urls:
            request = requests_map[url]
            if not hasattr(request.response, "body"):
                continue
            body = decode(request.response.body, request.response.headers.get("Content-Encoding", "identity"))
            json_data = json.loads(body.decode("utf-8"))
            map = copy.deepcopy(self.mapping_data)


            map["teams"]["home"] = json_data["payload"]["header"]["rivals"][0]
            map["teams"]["away"] = json_data["payload"]["header"]["rivals"][1]
            map["competition"] = json_data["payload"]["header"]["league"]["name"]
            map["time"] = datetime.fromtimestamp(json_data["payload"]["header"]["startTime"] / 1000).isoformat()

            sport = json_data["payload"]["header"]["sport"]["name"].lower()
            region = json_data["payload"]["header"]["region"]["name"].lower()
            liga = json_data["payload"]["header"]["league"]["name"].lower().replace(" ", "-")
            rivals = json_data["payload"]["header"]["rivalsSlug"]
            id = json_data["payload"]["header"]["eventId"]
            map["match_url"] = f"https://meridianbet.rs/sr/kladjenje/{sport}/{region}/{liga}/{rivals}/{id}"

            request_url = f"https://online.meridianbet.com/betshop/api/v2/events/{id}/markets?gameGroupId=all"

            print(f"Scraping {map['teams']['home']} vs {map['teams']['away']} at {map['time']}")
            print(map["match_url"] + "\n")
            matches[request_url] = map
        # input()

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

if __name__ == "__main__":
    bet = MeridianBet()
    bet.get_all_match_odds()