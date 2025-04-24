from fastapi import FastAPI
from .models import CatalogItem

app = FastAPI()

@app.post("/catalog/")
def create_catalog_item(item: CatalogItem):
    return {"message": "PENDING"}

@app.get("/catalog/")
def list_catalog_items():
    return {"name": "PENDING", "price": "6"}