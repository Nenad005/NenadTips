import sys
sys.path.insert(1, '../')
from bookmaker import Bookmaker

class MerkurXTIP(Bookmaker):
    def __init__(self):
        super().__init__('MerkurXTIP')

    def getAllMatchOdds(self):
        pass
        # Implement getAllMatchOdds method for MerkurXTIP
    def getMatchOdds(self, link):
        pass
        # Implement getMatchOdds method for MerkurXTIP
