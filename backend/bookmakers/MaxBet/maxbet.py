import sys
sys.path.insert(1, '../')
from bookmaker import Bookmaker

class MaxBet(Bookmaker):
    def __init__(self):
        super().__init__('MaxBet')

    def getAllMatchOdds(self):
        pass
        # Implement getAllMatchOdds method for MaxBet
    def getMatchOdds(self, link):
        pass
        # Implement getMatchOdds method for MaxBet
