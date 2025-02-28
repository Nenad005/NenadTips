from abc import ABC, abstractmethod
from pymongo import MongoClient

class Bookmaker(ABC):
    def __init__(self):
        self.db_client = None
        self.db = None

    def start_db_session(self):
        self.db_client = MongoClient('mongodb://localhost:27017/')
        self.db = self.db_client['NenadTips']

    def close_db_session(self):
        self.db_client.close()
        self.db = None

    def upsert_match(self, match_data):
        match_url = match_data["match_url"]
        home = match_data["teams"]["home"]
        away = match_data["teams"]["away"]
        print("Upserting match:", home, "vs", away)
        collection = self.db[self.get_collection_name()]
        
        filter_query = {"match_url": match_url}
        update_data = {"$set": match_data}
        
        result = collection.update_one(filter_query, update_data, upsert=True)
        
        if result.matched_count > 0:
            print("Document updated.")
        else:
            print("New document inserted.")

    @abstractmethod
    def get_all_match_odds():
        pass

    @abstractmethod
    def get_collection_name():
        pass