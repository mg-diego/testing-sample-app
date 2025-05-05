from bson import ObjectId
from pymongo import MongoClient

NOT_FOUND = "No document matched the provided ID."

class CatalogManagementDatabase:    

    def __init__(self):
        self.client = MongoClient("mongodb://mongo:27017/")
        self.db = self.client["testing-sample-app"]
        self.catalog_collection = self.db["catalog"]


    def create_item(self, catalog_item):
        try:
            result = self.catalog_collection.insert_one(catalog_item.dict())
            if result.acknowledged and result.inserted_id:
                return {"success": True, "created": True, 'id': str(result.inserted_id)}

        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}
    
    def delete_item(self, item_id):
        try:
            result = self.catalog_collection.delete_one({"_id": ObjectId(item_id)})

            if result.deleted_count == 0:
                return {"success": False, "error": NOT_FOUND}
            
            return {"success": True, "deleted": True}
        
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}

    def update_item(self, catalog_item):
        try:
            _id = ObjectId(catalog_item.id)

            update_data = catalog_item.dict(by_alias=True, exclude={"id"})  # Don't update _id
            result = self.catalog_collection.update_one(
                {"_id": _id},
                {"$set": update_data}
            )

            if result.matched_count == 0:
                return {"success": False, "error": NOT_FOUND}

            if result.modified_count == 0:
                return {"success": True, "error": ""}  # No changes were made

            return {"success": True, "updated": True}
        
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}

    def get_items(self, filter):
        try:
            items = list(self.catalog_collection.find({"name": {"$regex": filter, "$options": "i"}}))
            for item in items:
                item["_id"] = str(item["_id"])
            return {"success": True, "detail": items}
    
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}
