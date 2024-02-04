import sys
sys.path.insert(1, '../')
from bookmaker import Bookmaker

class frontend(Bookmaker):
    def __init__(self):
        super().__init__('frontend')

    def getAllMatchOdds(self):
        pass
        # Implement getAllMatchOdds method for frontend
    def getMatchOdds(self, link):
        pass
        # Implement getMatchOdds method for frontend
