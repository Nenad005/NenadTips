import sys
sys.path.insert(1, '../')
from bookmaker import Bookmaker

class AdmiralBet(Bookmaker):
    def __init__(self):
        super().__init__('AdmiralBet')

    def getAllMatchOdds(self):
        pass
        # Implement getAllMatchOdds method for AdmiralBet
    def getMatchOdds(self, link):
        pass
        # Implement getMatchOdds method for AdmiralBet
