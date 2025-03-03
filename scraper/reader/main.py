from pymongo import MongoClient
import json
from itertools import combinations
from TeamMatcher import TeamMatcher

from pymongo import MongoClient
from bson.objectid import ObjectId

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
        grouped[timestamp] = []

    for bookmaker in COLLECTIONS.keys():
        for document in COLLECTIONS[bookmaker]:
            grouped[document['time']].append({
                "id": f'{document['_id']}',
                "home": document["teams"]["home"],
                "away": document["teams"]["away"],
                "bookmaker": bookmaker
            })

    return grouped

def compare_odds(json1, json2):
    """Recursively compares "odds" properties and returns the higher values."""
    if isinstance(json1, dict) and isinstance(json2, dict):
        result = {}
        for key in set(json1.keys()).union(json2.keys()):
            if key in json1 and key in json2:
                result[key] = compare_odds(json1[key], json2[key])
            elif key in json1:
                result[key] = json1[key]
            else:
                result[key] = json2[key]
        return result
    elif isinstance(json1, list) and isinstance(json2, list):
        return [compare_odds(v1, v2) for v1, v2 in zip(json1, json2)]
    elif isinstance(json1, (int, float)) and isinstance(json2, (int, float)):
        return max(json1, json2)
    return json1 if json1 else json2

def get_odd_from_instruction(highest_odds, instructions):
    odds = highest_odds
    for instruction in instructions:
        odds = odds[instruction]
        if odds == None:
            return None
    return odds

if __name__ == "__main__":
    get_all_documents()
    print(len(COLLECTIONS['Mozzart']))
    print(len(COLLECTIONS['Soccer']))
    grouped = group_by_timestamps()
    matcher = TeamMatcher()

    client = MongoClient("mongodb://localhost:27017/")
    db = client["NenadTips"]
    db_collections = {
        "Mozzart": db["Mozzart"],
        "Soccer": db["Soccer"],
    }
    matches = db["Matches"],

    results = []
    for timestamp, matches in grouped.items():
    # Generate all possible pairs of matches
        for match1, match2 in combinations(matches, 2):
            # Check if both home and away teams match exactly
            if matcher.match(match1['home'], match1["away"], match2["home"], match2["away"]) and match1["bookmaker"] != match2["bookmaker"]:
                print(match1, match2, sep="\n")

                match1_data = db_collections[match1["bookmaker"]].find_one({"_id": ObjectId(match1["id"])})
                match2_data = db_collections[match2["bookmaker"]].find_one({"_id": ObjectId(match2["id"])})
                match1_data["_id"] = f"{match1_data["_id"]}"
                match2_data["_id"] = f"{match2_data["_id"]}"

                highest_odds = compare_odds(match1_data.get("odds", {}), match2_data.get("odds", {}))

                with open("arbitrage_mappings.json", "r") as f:
                    mappings = json.load(f)

                print(json.dumps(highest_odds, indent=4))

                for mapping in mappings:
                    odds = []
                    for instructions in mapping:
                        odd = get_odd_from_instruction(highest_odds, instructions)
                        odds.append(odd)
                    
                    if None in odds:
                        continue

                    arb = sum(1/x for x in odds)
                    print(mapping, arb)
                    if arb < 1:
                        for i in range(10):
                            print("NASAO")
                        print(odds)

                # print(json.dumps(match1_data, indent=4), json.dumps(match2_data, indent=4), sep="\n")
                # print("-----------------------------------------")
                # print("-----------------------------------------")
                input()


    # print(grouped)
    # print(json.dumps(grouped, indent=4))
    with open("grouped.json", 'w', encoding="utf8") as f:
        f.write(json.dumps(grouped, indent=4, ensure_ascii=False))