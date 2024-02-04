import sys
sys.path.insert(1, '../')
from bookmaker import Bookmaker

class SoccerBet(Bookmaker):
    def __init__(self):
        super().__init__('SoccerBet')

    def getAllMatchOdds(self):
        pass
        # Implement getAllMatchOdds method for SoccerBet
    def getMatchOdds(self, link):
        pass
        # Implement getMatchOdds method for SoccerBet
