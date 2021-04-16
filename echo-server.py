# https://realpython.com/python-sockets/#background

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
    s.bind((H, P))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)