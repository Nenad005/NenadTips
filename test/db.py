import json
from pymongo import MongoClient

with open("Bologna_Milan.json", "r", encoding="utf-8") as mapping_file:
    odds = json.load(mapping_file)
    def save_to_mongodb(data, collection_name):
        client = MongoClient('mongodb://localhost:27017/')
        db = client['NenadTips']
        collection = db[collection_name]
        collection.insert_one(data)
        client.close()

    save_to_mongodb(odds, 'odds_collection')
