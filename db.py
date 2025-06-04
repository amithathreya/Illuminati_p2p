from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
collection = db['chunks']

def insert_chunk(id,text):
    collection.insert_one({
    "chunk_id": id,
    "text": text
    })
    print(f"Inserted chunk with id {id} and text: {text}")
