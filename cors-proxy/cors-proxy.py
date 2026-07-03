import sys
sys.path.insert(1, '../')
from bookmaker import Bookmaker

class cors-proxy(Bookmaker):
    def __init__(self):
        super().__init__('cors-proxy')

    def getAllMatchOdds(self):
        pass
        # Implement getAllMatchOdds method for cors-proxy
    def getMatchOdds(self, link):
        pass
        # Implement getMatchOdds method for cors-proxy
