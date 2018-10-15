#! /usr/bin/env python
import sys
import select
import time
import re
from socket import socket, AF_INET, SOCK_STREAM
import thread

# take port number and ip addesses through sys.argv
listen_port = int(sys.argv[1]) # listen-port
fake_ip = sys.argv[2]  # bind to this ip for outbound connections
server_ip = sys.argv[3]


def proxy_listen():
    # Create TCP socket. This socket is used to listen from clients.
    s = socket(AF_INET, SOCK_STREAM)
    socket_outbound = socket(AF_INET, SOCK_STREAM)
    socket_outbound.bind((fake_ip, 4000))

    
    # Accept connection from client. Any ip address at the listening port would be accepted.
    try:
        s.bind(('', listen_port))
        s.listen(1)
        socket_listen, address = s.accept()
    except:
        s.close()
        socket_outbound.close()
        return

    try:
        socket_outbound.connect((server_ip, 8080))
    except:
        print "Server not available now. Try later"
        s.close()
        socket_outbound.close()
        return
    # Keep the connection and receive from client until the client terminate the connection.
    while 1:
        data = socket_listen.recv(1024)  # set the buffer size to be 1024 bytes
        if len(data) > 0:
            # Send data to the server.
            try:
                socket_outbound.send(data + "\n")
            except:
                print "Connection to server was terminated.\nDisconnect the client"
                socket_listen.close()
                s.close()
                socket_outbound.close()
                return

            # Receive data from server.
            try:
                reply = socket_outbound.recv(1024)
            except:
                print "Connection to server was terminated.\nDisconnect the client"
                socket_listen.close()
                s.close()
                socket_outbound.close()
                return

            if len(reply) > 0:
                try:
                    socket_listen.send(reply + "\n")
                except:
                    print "Connection to client was terminated.\nDisconnect the server"
                    socket_outbound.close()
                    s.close()
                    return
            else:
                print "Connection to server was terminated.\nDisconnect the client"
                socket_listen.close()
                s.close()
                socket_outbound.close()
                return

        # If the connection is disconnected by the client, connect to the next client.
        else:
            print "Connection to client was terminated.\nDisconnect the server"
            socket_outbound.close()
            s.close()
            return

while True:
    proxy_listen()

