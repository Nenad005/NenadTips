import sys
sys.path.insert(1, '../')
from bookmaker import Bookmaker

class PinBet(Bookmaker):
    def __init__(self):
        super().__init__('PinBet')

    def getAllMatchOdds(self):
        pass
        # Implement getAllMatchOdds method for PinBet
    def getMatchOdds(self, link):
        pass
        # Implement getMatchOdds method for PinBet
