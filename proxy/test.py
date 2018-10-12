import sys

user_input = str(sys.argv)
listen_port = sys.argv[0]  # listen-port
fake_ip = sys.argv[1]  # bind to this ip for outbound connections
server_ip = sys.argv[2] 

print listen_port
print fake_ip
print server_ip