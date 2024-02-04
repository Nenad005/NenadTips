import sys
sys.path.insert(1, '../')
from bookmaker import Bookmaker

class BalkanBet(Bookmaker):
    def __init__(self):
        super().__init__('BalkanBet')

    def getAllMatchOdds(self):
        pass
        # Implement getAllMatchOdds method for BalkanBet
    def getMatchOdds(self, link):
        pass
        # Implement getMatchOdds method for BalkanBet
