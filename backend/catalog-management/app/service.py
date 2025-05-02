from .database import CatalogManagementDatabase
from .models import CatalogItem

catalog_management_database = CatalogManagementDatabase()

def create_catalog_service(catalog: CatalogItem):
    if catalog.name == "":
        return "Name can't be empty."
    if catalog.description == "":
        return "Description can't be empty."
    
    return catalog_management_database.create_item(catalog)

def get_catalog_list_service(filter: str):
    return catalog_management_database.get_items(filter)

def delete_catalog_service(catalog_id: str):
    return catalog_management_database.delete_item(catalog_id)

def update_catalog_service(catalog: CatalogItem):
    return catalog_management_database.update_item(catalog)
    