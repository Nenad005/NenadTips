from abc import ABC, abstractmethod

class Bookmaker(ABC):
    @abstractmethod
    def getAllMatchOdds(self):
        pass

    @abstractmethod
    def getMatchOdds(self, link):
        pass
