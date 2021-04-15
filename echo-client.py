import socket
import json


with open("./network.json") as f:
    data = f.read()
    # print(type(data))

# print(data)

d = json.loads(data)
H = d["test"]["HOST"]
P = d["test"]["PORT"]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((H, P))
    s.sendall(b'Hello, world')
    data = s.recv(1024)

print('Received', repr(data))