import socket
import sys

required_num_command_line_args = 2

if len(sys.argv) < required_num_command_line_args:
    print("Usage: <address> [port number]")
else:
    ...