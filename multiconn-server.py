import selectors

## 
# difference between this server and the echo server is the call to 
# lsock.setblocking(False) to configure the socket in non-blocking mode 
# Calls made to this socket will no longer block

sel = selectors.DefaultSelector()
# ...
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print('listening on', (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)
