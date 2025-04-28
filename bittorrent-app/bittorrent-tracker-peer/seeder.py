import os
import json
from peer.peer import Peer

def seed(peers: list, metadata_path: str):
    """
    Distribute chunk files to all connected peers.

    Args:
        peers (list): List of Peer objects representing connected peers.
        metadata_path (str): Path to the metadata file containing chunk information.
    """
    # Load metadata
    try:
        with open(metadata_path, 'r') as file:
            metadata = json.load(file)
    except FileNotFoundError:
        print(f"Metadata file not found: {metadata_path}")
        return
    except json.JSONDecodeError:
        print(f"Error decoding JSON from metadata file: {metadata_path}")
        return

    # Iterate through chunks and distribute them to peers
    for chunk_index, chunk_info in metadata.get("chunks", {}).items():
        chunk_path = chunk_info.get("path")
        if not os.path.exists(chunk_path):
            print(f"Chunk file not found: {chunk_path}")
            continue

        # Read the chunk data
        with open(chunk_path, 'rb') as chunk_file:
            chunk_data = chunk_file.read()

        # Distribute the chunk to all peers
        for peer in peers:
            try:
                print(f"Uploading chunk {chunk_index} to peer {peer.peer_id}...")
                peer.upload(chunk_index)  # Assuming `upload` sends the chunk data
            except Exception as e:
                print(f"Failed to upload chunk {chunk_index} to peer {peer.peer_id}: {str(e)}")

if __name__ == "__main__":
    # Example usage
    metadata_path = "/home/kazuki/hybrid_p2p/data_dir/chunk_data/metadata.json"
    peer1 = Peer("peer1", ("localhost", 8000), metadata_path)
    peer2 = Peer("peer2", ("localhost", 8001), metadata_path)

    # Connect peers
    peer1.connect(("localhost", 8001))
    peer2.connect(("localhost", 8000))

    # Seed chunks to peers
    seed([peer1, peer2], metadata_path)

    # Disconnect peers
    peer1.disconnect(("localhost", 8001))
    peer2.disconnect(("localhost", 8000))