from pymongo import MongoClient

COLLECTIONS = {
    'Mozzart': [],
    'Soccer': [],
}

def get_documents_from_bookie(bookmaker):
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['NenadTips']
    collection = db[bookmaker]

    documents = collection.find().sort('time', 1)

    return documents

def get_all_documents():
    for bookmaker in COLLECTIONS.keys():
        documents = get_documents_from_bookie(bookmaker)
        for document in documents:
            COLLECTIONS[bookmaker].append(document)

def get_all_timestamps():
    timestamps = []
    for bookmaker in COLLECTIONS.keys():
        for document in COLLECTIONS[bookmaker]:
            timestamps.append(document['time'])

    timestamps = list(set(timestamps))
    timestamps.sort()
    return timestamps

def group_by_timestamps():
    timestamps = get_all_timestamps()

    grouped = {}
    for timestamp in timestamps:
        grouped[timestamp] = {
            'Mozzart': [],
            'Soccer': [],
        }

    for bookmaker in COLLECTIONS.keys():
        for document in COLLECTIONS[bookmaker]:
            grouped[document['time']][bookmaker].append(document)

    return grouped

if __name__ == "__main__":
    get_all_documents()
    print(len(COLLECTIONS['Mozzart']))
    print(len(COLLECTIONS['Soccer']))
    print(*get_all_timestamps(), sep='\n')