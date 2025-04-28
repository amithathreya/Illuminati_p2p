import socket
import json


HOST,PORT = "0.0.0.0",8080

message = {"type":"register", "peer_ip":"0.0.0.0", "peer_port": 8080, "file_hash": ["1234567890abcdef", "abcdef1234567890"]}

data = json.dumps(message)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((HOST,PORT))
    sock.sendall(data.encode())

    response = sock.recv(4096)
    print("Received response:", response.decode())
finally:
    sock.close()

print(f'sent message: {data}')
print(f'received response: {response.decode()}')