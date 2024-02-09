import json
import sys
sys.path.insert(1, '../')
from bookmaker import Bookmaker
import requests
import datetime

PROXY_ADDRESS = 'http://localhost:8000/'
PROXY_HEADER = {"X-Requested-With": "XMLHttpRequest"}

class Mozzart(Bookmaker):
    def __init__(self):
        super().__init__('Mozzart')

    def proxy_url(url):
        return PROXY_ADDRESS + url

    def getMatchIDs():
        payload = {
            "date": "all",
            "sportIds": [1],
            "competitionIds": [],
            "sort": "bycompetition",
            "specials": False,
            "subgames": [],
            "size": 1000,
            "mostPlayed": False,
            "type": "betting",
            "numberOfGames": 115,
            "activeCompleteOffer": False,
            "lang": "sr",
            "offset": 0
        }
        result = requests.post(url=Mozzart.proxy_url('https://www.mozzartbet.com/betOffer2'), headers=PROXY_HEADER, json=payload).json()
        data = [{match['id']: {"date": match['startTime']}} for match in result['matches']]
        print(data)
        dict = {}
        for match in [match for match in result['matches'] if len(match['participants']) > 1]:
            dict[match['id']] = {
                "startTime": match['startTime']
                
            }
        return dict
    
    def fillMatchData(id):
        pass

    def getAllMatchOdds():
        # print(Mozzart.getMatchIDs())
        IDs = Mozzart.getMatchIDs()

        pass
        # Implement getAllMatchOdds method for Mozzart
    def getMatchOdds(link):
        pass
        # Implement getMatchOdds method for Mozzart
    
if __name__ == '__main__':
    Mozzart.getMatchIDs()
