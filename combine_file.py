from pymongo import MongoClient
import os

# MongoDB setup
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['mydatabase']
    collection = db['chunks']
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit(1)

def list_file_hashes():
    """List all available file hashes in the database."""
    hashes = collection.distinct("file_hash")
    if not hashes:
        print("No file hashes found in the database.")
        exit(1)
    return hashes

def recombine_file(file_hash: str, output_folder: str):
    try:
        # Retrieve chunks and file extension from the database
        chunks = list(collection.find({"file_hash": file_hash}).sort("chunk_id"))
        if not chunks:
            print(f"No chunks found for file hash '{file_hash}'.")
            return

        # Get the file extension from the first chunk
        file_extension = chunks[0].get("file_extension", ".recombined")  # Default to .recombined if missing

        # Recombine chunks into the original file
        output_path = os.path.join(output_folder, f"{file_hash}{file_extension}")
        with open(output_path, "wb") as f:
            for chunk in chunks:
                binary_data = bytes.fromhex(chunk["chunk_data"])  # Convert hex back to binary
                f.write(binary_data)

        print(f"File recombined and saved to '{output_path}'.")
    except Exception as e:
        print(f"Error recombining file: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Recombine all files from chunks stored in MongoDB.")
    parser.add_argument("output_folder", type=str, help="Folder to save the recombined files")
    args = parser.parse_args()

    # Ensure the output folder exists
    os.makedirs(args.output_folder, exist_ok=True)

    # Get all file hashes from the database
    hashes = list_file_hashes()

    # Recombine each file automatically
    for file_hash in hashes:
        recombine_file(file_hash, args.output_folder)