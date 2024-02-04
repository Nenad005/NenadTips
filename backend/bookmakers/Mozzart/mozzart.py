import sys
sys.path.insert(1, "../")
from bookmaker import Bookmaker
from flask import Flask, jsonify
import asyncio
import aiohttp
PROXY_ADDRESS = 'http://localhost:8000/'

class Mozzart(Bookmaker):
    def __init__(self):
        super().__init__('Mozzart')

    def getAllMatchOdds(self):
        pass
        # Implement getAllMatchOdds method for Mozzart
    def getMatchOdds(self, link):
        pass
        # Implement getMatchOdds method for Mozzart
    

    def proxy_url(self, url):
        return PROXY_ADDRESS + url

    async def fetch(self, session, url, payload=None):
        async with session.post(self.proxy_url(url), json=payload, headers={"X-Requested-With": "XMLHttpRequest"}) as response:
            return await response.json()
    
    async def process_match(self, session, match):
        match_id = match['id']
        odds_url = 'https://www.mozzartbet.com/matchBetting'
        match_odds = await self.fetch(session, odds_url, payload={'id': match_id})
        match_odds = match_odds['kodds']
        sub_game_odds = {
            'pairs': [
                {"1": None, "x": None, "2": None},
                {"1x": None, "2": None},
                {"12": None, "x": None},
                {"1": None, "x2": None},
                {"0-1": None, "2+": None},
                {"0-2": None, "3+": None},
                {"0-3": None, "4+": None},
                {"0-4": None, "5+": None},
                {"fh1": None, "fhx": None, "fh2": None},
                {"fh1x": None, "fh2": None},
                {"fh12": None, "fhx": None},
                {"fh1": None, "fhx2": None},
                {"fh0-1": None, "fh2+": None},
                {"sh1": None, "shx": None, "sh2": None},
                {"sh0-1": None, "sh2+": None},
            ]
        }

        sub_game_odds['pairs'][0]['1'] =      match_odds['1001001001']['value'] if match_odds.get('1001001001') != None else None
        sub_game_odds['pairs'][0]['x'] =      match_odds['1001001002']['value'] if match_odds.get('1001001002') != None else None
        sub_game_odds['pairs'][0]['2'] =      match_odds['1001001003']['value'] if match_odds.get('1001001003') != None else None

        sub_game_odds['pairs'][1]["1x"] =     match_odds['1001002001']['value'] if match_odds.get('1001002001') != None else None
        sub_game_odds['pairs'][1]["2"] =      match_odds['1001001003']['value'] if match_odds.get('1001001003') != None else None
            
        sub_game_odds['pairs'][2]["12"] =     match_odds['1001002002']['value'] if match_odds.get('1001002002') != None else None
        sub_game_odds['pairs'][2]["x"] =      match_odds['1001001002']['value'] if match_odds.get('1001001002') != None else None
            
        sub_game_odds['pairs'][3]["1"] =      match_odds['1001001001']['value'] if match_odds.get('1001001001') != None else None
        sub_game_odds['pairs'][3]["x2"] =     match_odds['1001002003']['value'] if match_odds.get('1001002003') != None else None
            
        sub_game_odds['pairs'][4]["0-1"] =    match_odds['1001003001']['value'] if match_odds.get('1001003001') != None else None
        sub_game_odds['pairs'][4]["2+"] =     match_odds['1001003012']['value'] if match_odds.get('1001003012') != None else None
            
        sub_game_odds['pairs'][5]["0-2"] =    match_odds['1001003002']['value'] if match_odds.get('1001003002') != None else None
        sub_game_odds['pairs'][5]["3+"] =     match_odds['1001003004']['value'] if match_odds.get('1001003004') != None else None
            
        sub_game_odds['pairs'][6]["0-3"] =    match_odds['1001003013']['value'] if match_odds.get('1001003013') != None else None
        sub_game_odds['pairs'][6]["4+"] =     match_odds['1001003005']['value'] if match_odds.get('1001003005') != None else None
            
        sub_game_odds['pairs'][7]["0-4"] =    match_odds['1001003026']['value'] if match_odds.get('1001003026') != None else None
        sub_game_odds['pairs'][7]["5+"] =     match_odds['1001003007']['value'] if match_odds.get('1001003007') != None else None
            
        sub_game_odds['pairs'][8]["fh1"] =    match_odds['1001004001']['value'] if match_odds.get('1001004001') != None else None
        sub_game_odds['pairs'][8]["fhx"] =    match_odds['1001004002']['value'] if match_odds.get('1001004002') != None else None
        sub_game_odds['pairs'][8]["fh2"] =    match_odds['1001004003']['value'] if match_odds.get('1001004003') != None else None
            
        sub_game_odds['pairs'][9]["fh1x"] =   match_odds['1001297001']['value'] if match_odds.get('1001297001') != None else None
        sub_game_odds['pairs'][9]["fh2"] =    match_odds['1001004003']['value'] if match_odds.get('1001004003') != None else None
            
        sub_game_odds['pairs'][10]["fh12"] =  match_odds['1001297002']['value'] if match_odds.get('1001297002') != None else None
        sub_game_odds['pairs'][10]["fhx"] =   match_odds['1001004002']['value'] if match_odds.get('1001004002') != None else None
            
        sub_game_odds['pairs'][11]["fh1"] =   match_odds['1001004001']['value'] if match_odds.get('1001004001') != None else None
        sub_game_odds['pairs'][11]["fhx2"] =  match_odds['1001297003']['value'] if match_odds.get('1001297003') != None else None
        
        sub_game_odds['pairs'][12]["fh0-1"] = match_odds['1001008005']['value'] if match_odds.get('1001008005') != None else None
        sub_game_odds['pairs'][12]["fh2+"] =  match_odds['1001008002']['value'] if match_odds.get('1001008002') != None else None
        
        sub_game_odds['pairs'][13]["sh1"] =   match_odds['1001019001']['value'] if match_odds.get('1001019001') != None else None
        sub_game_odds['pairs'][13]["shx"] =   match_odds['1001019002']['value'] if match_odds.get('1001019002') != None else None
        sub_game_odds['pairs'][13]["sh2"] =   match_odds['1001019003']['value'] if match_odds.get('1001019003') != None else None
        
        sub_game_odds['pairs'][14]["sh0-1"] = match_odds['1001009005']['value'] if match_odds.get('1001009005') != None else None
        sub_game_odds['pairs'][14]["sh2+"] =  match_odds['1001009002']['value'] if match_odds.get('1001009002') != None else None

        # Add the remaining subgame odds...

        match['subGameOdds'] = sub_game_odds
        return match
    
    async def fetch_matches(self):
        offers_url = 'https://www.mozzartbet.com/betOffer2'
        payload = {
            "date": "three_days",
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

        async with aiohttp.ClientSession() as session:
            response = await self.fetch(session, offers_url, payload)
            data = [match for match in response['matches'] if len(match['participants']) > 1]
            data = [{
                'id': match['id'],
                'home': match['participants'][0],
                'away': match['participants'][1]
            } for match in data]
            tasks = [self.process_match(session, match) for match in data]
            return await asyncio.gather(*tasks)
        

async def main():
    test = Mozzart()
    print(jsonify((await test.fetch_matches())))

if __name__ == "__main__":
    main()
    input()