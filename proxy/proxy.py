#!/usr/bin/env python
import sys
import select
import time
import re
from socket import socket, AF_INET, SOCK_STREAM
import thread

# take port number and ip addesses

listen_port = int(sys.argv[1]) # listen-port
fake_ip = sys.argv[2]  # bind to this ip for outbound connections
server_ip = sys.argv[3]  # server-ip port 8080

#listen_port = 3000
#fake_ip = "127.0.0.1"
#server_ip = "127.0.0.1"


def proxy_listen():
    # Create TCP socket. This socket is used to listen from clients.
    s = socket(AF_INET, SOCK_STREAM)

    # Accept connection from client. Any ip address at the listening port would be accepted.
    s.bind(('', listen_port))
    s.listen(1)
    connection, address = s.accept()

    # Keep the connection and receive from client until the client terminate the connection.
    while 1:
        #try:
        data = connection.recv(1024)  # set the buffer size to be 1024 bytes
        print data
        proxy_server(connection, data)

        # If the connection is disconnected by the client, connect to the next client.
        #except:
        #    print "Connection terminated by client"
        #    connection, address = s.accept()


def proxy_server(connection, data):

    # Create TCP socket. This socket is used to send data to server.
    s = socket(AF_INET, SOCK_STREAM)

    # Establish connection between proxy and server.
    try:
        s.connect((server_ip, 8080))
        s.send(data)
        while True:
            # Receive reply from server. Set the buffer size to be 1024.
            reply = s.recv(1024)
            if len(reply) > 0:
                connection.send(reply)
            else:
                break
    except:
        s.close()
        connection.close()

proxy_listen()
'''
def cnn_string

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.bing("", listen_port)
    clientSocket.listen(1)
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(server_ip, 8080)

    while True:
        listenConnection, listen_ip = clientSocket.accept()
        serverConnection = serverSocket.connect()
        listen_data = listenConnection.recv(1024).decode("utf-8")
        print listen_data
        serverConnection.send(listen_data)


# Your proxy should accept connections from clients and then open up another connection with a server
'''

'''TCP Client
from socket import socket, AF_INET, SOCK_STREAM
import select

if __name__ == '__main__':
    serverName = 'localhost'
    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    sentence = raw_input('Input sentence: ')
    clientSocket.send(sentence)
    modifiedSentence = clientSocket.recv(1024)
    print ('From Server: ' +  modifiedSentence)
    clientSocket.close()

'''
'''
TCP server
from socket import socket, AF_INET, SOCK_STREAM
import time

if __name__ == '__main__':
    serverPort = 12000
    serverSocket = socket(AF_INET,SOCK_STREAM) ## LISTENING SOCKET!!!
    serverSocket.bind(('',serverPort))
    serverSocket.listen(1)
    print 'The server is ready to receive'
    while True:
        connectionSocket, addr = serverSocket.accept() ## RETURNS CONNECTION SOCKET!!!
        sentence = connectionSocket.recv(1024)

        # Processing
        capitalizedSentence = sentence.upper()
        
        connectionSocket.send(capitalizedSentence)
        print ("server handled: " + str(addr) + " with message: " + sentence)
        connectionSocket.close()
'''
