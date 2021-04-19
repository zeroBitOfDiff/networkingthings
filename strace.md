> strace -e trace=network,read,write ~/.../echo-client.py
```
socket(AF_INET, SOCK_STREAM|SOCK_CLOEXEC, IPPROTO_IP) = 3
connect(3, {sa_family=AF_INET, sin_port=htons(65432), sin_addr=inet_addr("127.0.0.1")}, 16) = 0
sendto(3, "Hello, world", 12, 0, NULL, 0) = 12
recvfrom(3, "Hello, world", 1024, 0, NULL, NULL) = 12
write(1, "Received b'Hello, world'\n", 25Received b'Hello, world'
) = 25
```