from pymongo import MongoClient
from datetime import datetime, timedelta
# import schedule
import time

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "NenadTips"
COLLECTIONs = ["Mozzart", "Soccer", "Meridian"]

def delete_old_documents(collection_name):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[collection_name]

    five_minutes_ago = datetime.now() + timedelta(minutes=5)
    five_minutes_ago_str = five_minutes_ago.isoformat()
    result = collection.delete_many({"time": {"$lt": five_minutes_ago_str}})
    
    print(f"Deleted {result.deleted_count} old documents.")
    client.close()

# Schedule the script to run every 5 minutes
# schedule.every(5).minutes.do(delete_old_documents)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

for colllection in COLLECTIONs:
    delete_old_documents(colllection)
