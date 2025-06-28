
from pymongo import MongoClient

def connect_mongo():
    client = MongoClient("mongodb://localhost:27017/")
    return client["portfolio_db"]

def get_all_clients():
    db = connect_mongo()
    clients = list(db.clients.find({}, {"_id": 0}))
    return clients


def get_top_holders_from_mongo(stock_name):
    db = connect_mongo()
    
    pipeline = [
        {"$unwind": "$holdings"},  # Deconstruct array of holdings
        {"$match": {"holdings.stock": {"$regex": stock_name, "$options": "i"}}},  # Case-insensitive match
        {"$project": {"name": 1, "value": "$holdings.value"}},  # Select name + stock value
        {"$sort": {"value": -1}},  # Descending by value
        {"$limit": 10}
    ]

    results = list(db.clients.aggregate(pipeline))

    return {
        "labels": [r["name"] for r in results],
        "data": [r["value"] for r in results]
    }
