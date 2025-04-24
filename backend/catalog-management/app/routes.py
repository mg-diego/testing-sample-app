from fastapi import APIRouter, HTTPException
from .models import CatalogItem, create_item, get_items
from pymongo import MongoClient

router = APIRouter()

@router.post("/catalog/")
def create_catalog_item(item: CatalogItem):
    return create_item(item)

@router.get("/catalog/")
def list_catalog_items():
    return get_items()
