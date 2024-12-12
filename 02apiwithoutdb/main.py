from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel 
from typing import List

app = FastAPI()

# Define the data model
class Item(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    on_offer: bool

# In-memory storage
items: List[Item] = []

@app.get("/")
def read_root():
    return {"message":"Welcome to FastAPI"}
# Create an item
@app.post("/items/", response_model=Item)
def create_item(item: Item):
    if any(existing_item.id == item.id for existing_item in items):
        raise HTTPException(status_code=400, detail="Item with this ID already exists")
    items.append(item)
    return item

# Read all items
@app.get("/items/", response_model=List[Item])
def get_items():
    return items

# Read a single item by ID
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# Update an item
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(items):
        if item.id == item_id:
            items[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

# Delete an item
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for index, item in enumerate(items):
        if item.id == item_id:
            del items[index]
            return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")
