from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from db import *

app = FastAPI()

class ChunkIn(BaseModel):
    file_hash: str
    chunk_id: int
    chunk_data:str

class chunkOut(BaseModel):
    id:str
    file_hash: str
    chunk_id: int
    chunk_data:str

def doc_to_chunK(doc)->chunkOut:
    return chunkOut(
        id=str(doc["_id"]),
        file_hash=doc["file_hash"],
        chunk_id=doc["chunk_id"],
        chunk_data=doc["chunk_data"]
    )

@app.get("/")
async def greet():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
async def insert_item(item_id: int, text: str):
    if item_id < 0:
        raise HTTPException(status_code=400, detail="Item ID must be a positive integer")
    return {"item_id": item_id, "text": text}


