from pymongo import MongoClient

try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['mydatabase']
    collection = db['chunks']

    result = collection.delete_many({})
    print(f"Deleted {result.deleted_count} documents from the database.")
except Exception as e:
    print(f"Error clearing the database: {e}")