import os
import hashlib
from pymongo import MongoClient
import asyncio

# MongoDB setup
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['mydatabase']
    collection = db['chunks']
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit(1)

async def split_and_store_file(file_path):
    try:
        with open(file_path, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()

        chunk_size = 256 * 1024  
        chunk_id = 0

        with open(file_path, "rb") as f:
            while chunk := f.read(chunk_size):
                chunk_data = chunk.hex()  
                await store_chunk(file_hash, chunk_id, chunk_data)
                chunk_id += 1

        print(f"File '{file_path}' split and stored successfully.")
    except Exception as e:
        print(f"Error processing file '{file_path}': {e}")

async def store_chunk(file_hash, chunk_id, chunk_data):
    try:
        collection.insert_one({
            "file_hash": file_hash,
            "chunk_id": chunk_id,
            "chunk_data": chunk_data
        })
        print(f"Stored chunk {chunk_id} for file hash {file_hash}.")
    except Exception as e:
        print(f"Error storing chunk {chunk_id}: {e}")

async def process_folder(folder_path):
    if not os.path.isdir(folder_path):
        print(f"{folder_path} is not a valid directory.")
        return

    tasks = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            tasks.append(split_and_store_file(file_path))

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Split files into chunks and store in MongoDB.")
    parser.add_argument("folder_path", type=str, help="Path to the folder containing files")
    args = parser.parse_args()

    asyncio.run(process_folder(args.folder_path))
