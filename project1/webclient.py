import socket
import sys

required_num_command_line_args = 2
default_port = 80

if len(sys.argv) < required_num_command_line_args:
    print("Usage: <address> [port number]")
else:
    web_address = sys.argv[1]
    req = "GET / HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n".format(web_address).encode("ISO-8859-1")
    port = default_port
    if len(sys.argv) > required_num_command_line_args:
        port = sys.argv[2]
    
    s = socket.socket()
    s.connect((web_address, port))
    s.sendall(req)
    d = s.recv(4096)
    print(d)
    if len(d) == 0:
        print("complete")