import sys
sys.path.insert(1, '../')
from bookmaker import Bookmaker

class backend(Bookmaker):
    def __init__(self):
        super().__init__('backend')

    def getAllMatchOdds(self):
        pass
        # Implement getAllMatchOdds method for backend
    def getMatchOdds(self, link):
        pass
        # Implement getMatchOdds method for backend
