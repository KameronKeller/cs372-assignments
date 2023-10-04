import socket
import sys

MIN_NUM_ARGS = 2
MAX_NUM_ARGS = 3
DEFAULT_PORT = 80
RECV_BUFFER_SIZE = 4096
ENCODING = "ISO-8859-1"

def parse_args(args, default_port, req_num_args):
    web_address = args[1]
    port = default_port
    if len(args) == req_num_args:
        port = args[2]
    return web_address, int(port)

def build_request(web_address, encoding):
    http_header = "GET / HTTP/1.1\r\n"
    host = "Host: {}\r\n".format(web_address)
    connection_command = "Connection: close\r\n\r\n"
    req = http_header + host + connection_command
    return req.encode(encoding)

def receive_response(socket, recv_buff_size):
    d = socket.recv(recv_buff_size)
    receive_buffer = d

    while len(d) != 0:
        d = socket.recv(recv_buff_size)
        receive_buffer += d

    print(receive_buffer.decode())

def run_client():
        web_address, port = parse_args(sys.argv, DEFAULT_PORT, MAX_NUM_ARGS)
        req = build_request(web_address, ENCODING)
        s = socket.socket()
        s.connect((web_address, port))
        s.sendall(req)
        receive_response(s, RECV_BUFFER_SIZE)
        s.close()

if len(sys.argv) != MIN_NUM_ARGS and len(sys.argv) != MAX_NUM_ARGS:
    print("Usage: <address> [port number]")
else:
    run_client()