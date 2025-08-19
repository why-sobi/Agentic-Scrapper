from pydantic import BaseModel, Field
from typing import List

class Item(BaseModel):
    name: str = Field(..., description="Name of the item")
    url: str = Field(..., description="URL of the item")
    price: str = Field(..., description="Price of the item")
    rating: str = Field(..., description="Rating of the item")
    description: str = Field(..., description="Description of the item")

class FinalResult(BaseModel):
    result: list[Item] = Field(..., description="List of items with their details")
    
if __name__ == "__main__":
    pass  # This module is not meant to be run directly
    # It is intended to be imported and used in other modules.
    
