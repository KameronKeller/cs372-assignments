import socket
import sys

MIN_NUM_ARGS = 1
MAX_NUM_ARGS = 2
DEFAULT_PORT = 28333
RECV_BUFFER_SIZE = 4096
ENCODING = "ISO-8859-1"

def parse_args(args, default_port, req_num_args):
    port = default_port
    if len(args) == req_num_args:
        port = args[1]
    return int(port)

def receive_request(socket, recv_buff_size, encoding):
    d = socket.recv(recv_buff_size)

    while "\r\n\r\n" not in d.decode():
        d += socket.recv(recv_buff_size)
    
    response = "HTTP/1.1 200 OK\nContent-Type: text/plain\nContent-Length: 6\nConnection: close\n\nHello!"
    socket.send(response.encode(encoding))

def run_server():
        port = parse_args(sys.argv, DEFAULT_PORT, MAX_NUM_ARGS)
        s = socket.socket()
        s.bind(('', port))
        s.listen()
        while True:
            new_conn = s.accept()
            new_socket = new_conn[0]  # This is what we'll recv/send on
            receive_request(new_socket, RECV_BUFFER_SIZE, ENCODING)
            new_socket.close()

if len(sys.argv) != MIN_NUM_ARGS and len(sys.argv) != MAX_NUM_ARGS:
    print("Usage: [port number]")
else:
    run_server()