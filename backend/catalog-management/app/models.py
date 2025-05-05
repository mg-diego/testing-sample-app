from typing import Optional
from pydantic import BaseModel, Field

class CatalogItem(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    description: str

    class Config:
        populate_by_name = True
