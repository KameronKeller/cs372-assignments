import socket
import sys

required_num_command_line_args = 2
default_port = 80

if len(sys.argv) < required_num_command_line_args:
    print("Usage: <address> [port number]")
else:
    web_address = sys.argv[1]
    port = default_port
    if len(sys.argv) > required_num_command_line_args:
        port = sys.argv[2]
    
    s = socket.socket()
    s.connect((web_address, port))