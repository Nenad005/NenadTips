# from bookmaker import Bookmaker
import requests

class MozzartBet:
    def __init__(self):
        super().__init__()
        self.session = None

    def start_session(self):
        self.session = requests.Session()
        response = self.session.get("https://www.mozzartbet.com")
        print(response.status_code)

    def make_dummy_post_request(self):
        url = "https://www.mozzartbet.com/betting/matches"
        data = {
            "date": "three_days",
            "sort": "bycompetition",
            "currentPage": 0,
            "pageSize": 100,
            "sportId": 1,
            "competitionIds": [],
            "search": "",
            "matchTypeId": 0
        }
        response = self.session.post(url, data=data)
        print(response.status_code, response.content)

    def close_session(self):
        if self.session:
            self.session.close()

if __name__ == "__main__":
    mozzart = MozzartBet()
    mozzart.start_session()
    mozzart.make_dummy_post_request()
    mozzart.close_session()