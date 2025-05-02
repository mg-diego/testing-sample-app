from typing import Optional
from pydantic import BaseModel, Field

class CatalogItem(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str
    description: str
