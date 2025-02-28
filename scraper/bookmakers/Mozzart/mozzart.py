import requests
import json
import sys
sys.path.insert(1, '../')
from bookmaker import Bookmaker
import copy
from datetime import datetime
import time

PROXY_ADDRESS = 'http://localhost:8000/'
PROXY_HEADER = {
    "X-Requested-With": "XMLHttpRequest",
    "medium": "WEB"
}

class MozzartBet(Bookmaker):
    def __init__(self):
        super().__init__()
        self.session = None

    def get_all_match_odds(self):

        self.start_session()
        self.start_db_session()
        response = self.make_request()
        current_page = 0
        response = self.make_request(page=current_page)
        while response["status_code"] == 200:
            self.save_content(response["content"])
            time.sleep(2)
            current_page += 1
            response = self.make_request(page=current_page)
        if response["status_code"] == -1:
            print("No more matches to scrape.")
        else:
            print("An error occurred while scraping matches.")

        self.close_db_session()
        self.close_session()

    def get_collection_name(self):
        return "Mozzart"

    def start_session(self):
        self.session = requests.Session()

    def get_subgame_ids(self):
        with open("mozzart_football_mapping.json", "r") as file:
            data = json.load(file)
        
        subgame_ids = []

        def collect_values(obj):
            if isinstance(obj, dict):
                for value in obj.values():
                    collect_values(value)
            elif isinstance(obj, list):
                for item in obj:
                    collect_values(item)
            elif obj is not None:
                subgame_ids.append(obj)

        collect_values(data)
        return subgame_ids

    def save_content(self, content):
        with open ("mozzart_football_mapping.json", "r") as file:
            mapping = json.load(file)

        items = content["items"]
        for item in items:
            home = item["home"]["name"]
            away = item["visitor"]["name"]
            competition = item["competition"]["name"]
            time = item["startTime"]
            time = datetime.fromtimestamp(time / 1000).isoformat()
            match_url = "https://www.mozzartbet.com/sr/kladjenje/sport/1/match/" + str(item["id"])

            # print(home, away, competition)

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

            map = copy.deepcopy(mapping)

            map["teams"]["home"] = home
            map["teams"]["away"] = away
            map["competition"] = competition
            map["time"] = time
            map["match_url"] = match_url
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
                                    try:
                                        map["odds"][cat][subcat][odd][subodd] = odds_data[x[subodd]]["value"]
                                    except KeyError:
                                        map["odds"][cat][subcat][odd][subodd] = None

                        elif x is None:
                            continue
                        else:

                            try:
                                map["odds"][cat][subcat][odd] = odds_data[x]["value"]
                            except KeyError:
                                map["odds"][cat][subcat][odd] = None

            self.upsert_match(map)

    def make_request(self, page=0):
        print(f"Requesting page {page}...")
        url = f"{PROXY_ADDRESS}https://www.mozzartbet.com/betting/matches"
        data = {
            "date": "three_days",
            "sort": "bycompetition",
            "currentPage": page,
            "pageSize": 100,
            "sportId": 1,
            "competitionIds": [],
            "subgameIds": self.get_subgame_ids(),
            "search": "",
            "matchTypeId": 0
        }
        response = self.session.post(url, data=data, headers=PROXY_HEADER)

        if (response.status_code == 200):
            if response.json()["matchCount"] == 0:
                return {
                    "status_code": -1,
                    "content": {}
                }
            else:
                return {
                    "status_code": response.status_code,
                    "content": response.json()
                }
        else:
            return {
                "status_code": response.status_code,
                "content": {}
            }
    
    def close_session(self):
        if self.session:
            self.session.close()

if __name__ == "__main__":
    mozzart = MozzartBet()
    mozzart.get_all_match_odds()