import os
from pymongo import MongoClient

def connect_mongo():
    mongo_uri = os.getenv("MONGO_URI")
    client = MongoClient(mongo_uri)
    return client.get_default_database()

def get_all_clients():
    db = connect_mongo()
    clients = list(db.clients.find({}, {"_id": 0}))
    return clients


def get_top_holders_from_mongo(stock_name):
    db = connect_mongo()
    
    pipeline = [
        {"$unwind": "$holdings"},  
        {"$match": {"holdings.stock": {"$regex": stock_name, "$options": "i"}}},  
        {"$project": {"name": 1, "value": "$holdings.value"}},  
        {"$sort": {"value": -1}},  
        {"$limit": 10}
    ]

    results = list(db.clients.aggregate(pipeline))

    return {
        "labels": [r["name"] for r in results],
        "data": [r["value"] for r in results]
    }
