import socket
import sys

REQ_NUM_ARGS = 1
DEFAULT_PORT = 28333
RECV_BUFFER_SIZE = 4096
ENCODING = "ISO-8859-1"

def parse_args(args, default_port, req_num_args):
    port = default_port
    if len(args) > req_num_args:
        port = args[1]
    return port

# def build_request(web_address, encoding):
#     http_header = "GET / HTTP/1.1\r\n"
#     host = "Host: {}\r\n".format(web_address)
#     connection_command = "Connection: close\r\n\r\n"
#     req = http_header + host + connection_command
#     return req.encode(encoding)

def receive_request(socket, recv_buff_size):
    socket.recv()

    while len(d) != 0:
        print(d)
        d = socket.recv(recv_buff_size)

def run_server():
        port = parse_args(sys.argv, DEFAULT_PORT, REQ_NUM_ARGS)
        # req = build_request(web_address, ENCODING)
        s = socket.socket()
        s.bind(('', port))
        s.listen()
        new_conn = s.accept()
        new_socket = new_conn[0]  # This is what we'll recv/send on
        receive_request(new_socket, RECV_BUFFER_SIZE)

        # s.connect((web_address, port))
        # s.sendall(req)
        # receive_response(s, RECV_BUFFER_SIZE)
        # s.close()

if len(sys.argv) < REQ_NUM_ARGS:
    print("Usage: [port number]")
else:
    run_server()