from pydantic import BaseModel

class CatalogItem(BaseModel):
    name: str
    description: str
    price: float
