import sys
sys.path.insert(1, '../')
from bookmaker import Bookmaker

class OktagonBet(Bookmaker):
    def __init__(self):
        super().__init__('OktagonBet')

    def getAllMatchOdds(self):
        pass
        # Implement getAllMatchOdds method for OktagonBet
    def getMatchOdds(self, link):
        pass
        # Implement getMatchOdds method for OktagonBet
