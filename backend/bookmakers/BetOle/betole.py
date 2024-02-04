import sys
sys.path.insert(1, '../')
from bookmaker import Bookmaker

class BetOle(Bookmaker):
    def __init__(self):
        super().__init__('BetOle')

    def getAllMatchOdds(self):
        pass
        # Implement getAllMatchOdds method for BetOle
    def getMatchOdds(self, link):
        pass
        # Implement getMatchOdds method for BetOle
