import socket
import threading
import json
class Tracker :

    def __init__(self,host = "0.0.0.0",port = 8080):
        self.host = host
        self.port =port
        self.file_registration = {}
        self.start()
    def start(self):
        tracker_socket =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        tracker_socket.bind(("0.0.0.0",8080))
        queue_size = 100
        print("Accepting peer registration on port 8080 :")
        tracker_socket.listen(queue_size)
        while True:
            peer_socket, addr = tracker_socket.accept()
            print(f"Peer {addr} connected")
            thread = threading.Thread(target=self.handle_peer, args=(peer_socket,addr))
            thread.start()

    def register_peer(self,message):
        peer_ip = message.get("peer_ip")
        peer_port = message.get("peer_port")
        file_hashs:list = message.get("file_hash")
        for file_hash in file_hashs:
            if file_hash not in self.file_registration:
                self.file_registration[file_hash] = []
                self.file_registration[file_hash].append((peer_ip,peer_port))
                print(f"Peer registered for file {file_hash} with ip and port: {peer_ip}:{peer_port}")
    
    def handle_file_lookup(self,message):
        file_name = message.get("file_name")
        for file_hash , peers in self.file_registration.items():
            if file_name in file_hash:
                print(f"File {file_name} found with hash {file_hash}")
                response = {
                    "type": "file_found",
                    "file_hash": file_hash,
                    "peers": [{"peer_ip": peer["peer_ip"], "peer_port": peer["peer_port"]} for peer in peers]
                }
                return response
        return {"type":"error" , "message":"File not found"}    

    def handle_peer(self, peer_socket, addr):
        print(f'[+] new connection from {addr}')
        try:
            data = peer_socket.recv(4096).decode()
            if not data:
                return 
            message = json.loads(data)
            message_type = message.get("type")
            if message_type == "register":
                self.register_peer(message)
                response = {"type":"success" , "message":"Peer registered successfully"}
            elif message_type == "file_request":
                response  = self.handle_file_lookup(message)
            else:
                response = {"type":"error", "message":"Invalid request type"}
            peer_socket.send(json.dumps(response).encode())
        except json.JSONDecodeError:
            print("Error decoding JSON from peer")
            response = {"type":"error", "message":"Invalid JSON format"}
            peer_socket.send(json.dumps(response).encode())
        except Exception as e:
            print(f"Error handling peer request: {e}")
            response = {"type":"error", "message":"Internal server error"}
            peer_socket.send(json.dumps(response).encode())
        finally:
            peer_socket.close()

if __name__ == '__main__':
    tracker = Tracker()
    tracker.accept_peer_registration()