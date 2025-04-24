from pymongo import MongoClient

client = MongoClient("mongodb://mongo:27017/")
db = client["catalog_db"]
collection = db["items"]

def create_item(item):
    collection.insert_one(item.dict())

def get_items():
    return list(collection.find())
