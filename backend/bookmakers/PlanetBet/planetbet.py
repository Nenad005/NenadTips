import sys
sys.path.insert(1, '../')
from bookmaker import Bookmaker

class PlanetBet(Bookmaker):
    def __init__(self):
        super().__init__('PlanetBet')

    def getAllMatchOdds(self):
        pass
        # Implement getAllMatchOdds method for PlanetBet
    def getMatchOdds(self, link):
        pass
        # Implement getMatchOdds method for PlanetBet
