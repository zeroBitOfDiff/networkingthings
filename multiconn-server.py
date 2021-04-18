import selectors
import socket
import json
import types
## 
# difference between this server and the echo server is the call to 
# lsock.setblocking(False) to configure the socket in non-blocking mode 
# Calls made to this socket will no longer block

sel = selectors.DefaultSelector()

with open("./network.json") as f:
    data = f.read()
    # print(type(data))

# print(data)

d = json.loads(data)
H = d["test"]["HOST"]
P = d["test"]["PORT"]



def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print("closing connection to", data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print("echoing", repr(data.outb), "to", data.addr)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]



lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((H, P))
lsock.listen()
print('listening on', (H, P))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()