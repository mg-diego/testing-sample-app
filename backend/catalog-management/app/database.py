from bson import ObjectId
from pymongo import MongoClient


class CatalogManagementDatabase:

    def __init__(self):
        self.client = MongoClient("mongodb://mongo:27017/")
        self.db = self.client["testing-sample-app"]
        self.catalog_collection = self.db["catalog"]


    def create_item(self, catalog_item):
        self.catalog_collection.insert_one(catalog_item.dict())
        return True
    
    def delete_item(self, item_id):
        result = self.catalog_collection.delete_one({"_id": ObjectId(item_id)})
        return result.deleted_count > 0

    def update_item(self, catalog_item):
        result = self.catalog_collection.update_one(
            {"_id": catalog_item.id},
            {"$set": catalog_item.dict()}
        )
        return result.modified_count > 0

    def get_items(self, filter):
        items = list(self.catalog_collection.find({"name": {"$regex": filter, "$options": "i"}}))
        for item in items:
            item["_id"] = str(item["_id"])
        return items
