#! /usr/bin/env python
import sys
import select
import time
import re
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from thread import *

# Take arguments port number and ip addesses through sys.argv.

# Convert listen_port to Integer.
listen_port = int(sys.argv[1])
fake_ip = sys.argv[2]
server_ip = sys.argv[3]


class ConnHandler:

    def __init__(self, listen_socket):
        self.client, _ = listen_socket.accept()
        self.server = None
        self.buffer_size = 4096
        self.received = 1

    def process_connection(self):
        request = self.client.recv(self.buffer_size)
        if len(request) > 0:
            self.server = socket(AF_INET, SOCK_STREAM)
            self.server.bind((fake_ip, 0))
            try:
                self.server.connect((server_ip, 8080))
                request = request.decode()
                searchobj = re.search('big_buck_bunny', request)
                if searchobj is not None:
                    request = request.replace("big_buck_bunny", "big_buck_bunny_nolist")
                    request = request.encode()
                self.server.send(request)
                self.received = 0
            except Exception:
                print "Server not available now. Try Later"
                self.client.close()
                return

            inputs = [self.client, self.server]
            while True:
                readable, writeable, errs = select.select(inputs, [], inputs, 3)
                if errs:
                    break
                for soc in readable:
                    try:
                        data = soc.recv(self.buffer_size)
                    except Exception:
                        print "Connection Lost"
                        self.server.close()
                        self.client.close()
                        return
                    if data:
                        if soc is self.client:
                            try:
                                while self.received == 0:
                                    time.sleep(0.001)
                                data = data.decode()
                                searchobj = re.search('big_buck_bunny', data)
                                if searchobj is not None:
                                    data = data.replace("big_buck_bunny", "big_buck_bunny_nolist")
                                    data = data.encode()
                                self.server.send(data)
                                self.received = 0
                            except Exception:
                                print "Server lost"
                                self.client.close()
                                return
                        elif soc is self.server:
                            try:
                                self.client.send(data)
                                self.received = 1
                                #seachobj = re.search('text/xml')
                                #log_str = str()
                            except Exception:
                                print "Client lost"
                                self.server.close()
                                return
                    else:
                        break
            self.client.close()
            self.server.close()


if __name__ == '__main__':
    # Create TCP socket. This socket is used to listen from clients.
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    try:
        s.bind(('', listen_port))
        # Allow at most 5 connection
        s.listen(5)
    except Exception:
        print "Fail to start proxy."
        sys.exit(1)


    ''' Call the proxy_listen function in a while loop, such that if client close the connection, the proxy can listen to another client, if the server shut down, the proxy
    can inform the client and continue working when the server recovers.'''
    while True:
        try:
            start_new_thread(ConnHandler(s).process_connection, ())
            # print "Connection to client was terminated."

        except KeyboardInterrupt:
            s.close()
            sys.exit(2)


