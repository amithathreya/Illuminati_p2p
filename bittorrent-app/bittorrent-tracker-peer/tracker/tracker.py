import socket
import threading
import json
import signal
import sys
class Tracker :

    def __init__(self,host = "0.0.0.0",port = 8080):
        self.host = host
        self.port =port
        self.file_registration = {}
        self.running = True
        self.tracker_socket = None
        self.start()
    def start(self):
        self.tracker_socket =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.tracker_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tracker_socket.bind((self.host,self.port))
        queue_size = 100
        print("Accepting peer registration on port 8080 :")
        self.tracker_socket.listen(queue_size)
        while self.running:
            try:
                peer_socket, addr = self.tracker_socket.accept()
                print(f"Peer {addr} connected")
                thread = threading.Thread(target=self.handle_peer, args=(peer_socket,addr))
                thread.start()
            except OSError:
                break

    def register_peer(self,message):
        peer_ip = message.get("peer_ip")
        peer_port = message.get("peer_port")
        file_hash:list = message.get("file_hash")
        for file_hash in file_hash:
            if file_hash not in self.file_registration:
                self.file_registration[file_hash] = []
                self.file_registration[file_hash].append((peer_ip,peer_port))
                print(f"Peer registered for file {file_hash} with ip and port: {peer_ip}:{peer_port}")
    
    def handle_file_lookup(self,message):
        file_hash = message.get("file_hash")
        for  peers in self.file_registration[file_hash]:
                if file_hash in self.file_registration.items():
                    print(f"File found with hash {file_hash}")
                    response = {
                        "type": "file_found",
                        "file_hash": file_hash,
                        "peers": {"peer_ip":peers[0], "peer_port": peers[1]}
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
    
    def gracefull_shutdown(self,signum,frame):
        print("Shutting down tracker server...")
        self.running = False
        if self.tracker_socket:
            self.tracker_socket.close()
        print("Tracker server shut down successfully.")
        sys.exit(0)

if __name__ == '__main__':
    tracker = Tracker()
    signal.signal(signal.SIGINT, tracker.gracefull_shutdown)
    tracker.start()