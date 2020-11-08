import socket
import sys
import select

# Broadcast message


def broadcast(sock, message):
    for socket in servers:
        try:
            if socket != server and socket != sock:
                socket.send(message)
        except:
            # Remove disconnected client
            socket.close
            servers.remove(socket)


servers = []
buff = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(("0.0.0.0", 9876))

# up to 10 clients
server.listen(10)

# True indicates if the specific client has not sent any message
servers.append(server)

while True:
    # Monitor client
    reads, writes, err = select.select(servers, [], [])

    for sock in reads:

        # Check for new client
        if sock == server:
            sockfd, addr = server.accept()
            servers.append(sockfd)
        else:
            try:
                data = sock.recv(buff)
                if data:
                    broadcast(sock, data)

            except:
                sock.close()
                servers.remove(sock)
                continue

server.close()
