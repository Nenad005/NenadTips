from abc import ABC, abstractmethod

class Bookmaker(ABC):
    @abstractmethod
    def getAllMatchOdds():
        pass

    @abstractmethod
    def getMatchOdds(link):
        pass
