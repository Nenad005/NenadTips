import sys
sys.path.insert(1, '../')
from bookmaker import Bookmaker

class MeridianBet(Bookmaker):
    def __init__(self):
        super().__init__('MeridianBet')

    def getAllMatchOdds(self):
        pass
        # Implement getAllMatchOdds method for MeridianBet
    def getMatchOdds(self, link):
        pass
        # Implement getMatchOdds method for MeridianBet
