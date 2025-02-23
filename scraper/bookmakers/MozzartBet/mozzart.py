# from bookmaker import Bookmaker
import requests
import json

PROXY_ADDRESS = 'http://localhost:8000/'
PROXY_HEADER = {
    "X-Requested-With": "XMLHttpRequest",
    "medium": "WEB"
}

class MozzartBet:
    def __init__(self):
        super().__init__()
        self.session = None

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

    def save_content(self, content, filename):
        with open(filename, "w") as file:
            json.dump(content, file, indent=4)

    def make_request(self):
        url = f"{PROXY_ADDRESS}https://www.mozzartbet.com/betting/matches"
        data = {
            "date": "three_days",
            "sort": "bycompetition",
            "currentPage": 0,
            "pageSize": 100,
            "sportId": 1,
            "competitionIds": [],
            "subgameIds": self.get_subgame_ids(),
            "search": "",
            "matchTypeId": 0
        }
        response = self.session.post(url, data=data, headers=PROXY_HEADER)

        self.save_content(response.json(), "mozzart.json")
        print(response.status_code)

    def close_session(self):
        if self.session:
            self.session.close()

if __name__ == "__main__":
    mozzart = MozzartBet()
    mozzart.start_session()
    mozzart.make_request()
    mozzart.close_session()