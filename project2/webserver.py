import socket
import sys
from request import Request
from response import Response

MIN_NUM_ARGS = 1
MAX_NUM_ARGS = 2
DEFAULT_PORT = 28333
RECV_BUFFER_SIZE = 4096

def parse_args(args, default_port, req_num_args):
    port = default_port
    if len(args) == req_num_args:
        port = args[1]
    return int(port)

def receive_request(socket, recv_buff_size):
    request_buffer = socket.recv(recv_buff_size)

    while "\r\n\r\n" not in request_buffer.decode():
        request_buffer += socket.recv(recv_buff_size)
    
    request = Request(request_buffer)
    print("File requested: {}".format(request.file_name))
    response = Response(request)
    socket.send(response.build_response())

def run_server():
        port = parse_args(sys.argv, DEFAULT_PORT, MAX_NUM_ARGS)
        listening_socket = socket.socket()
        listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listening_socket.bind(('', port))
        listening_socket.listen()
        while True:
            new_conn = listening_socket.accept()
            new_socket = new_conn[0]  # This is what we'll recv/send on
            receive_request(new_socket, RECV_BUFFER_SIZE)
            new_socket.close()

if len(sys.argv) != MIN_NUM_ARGS and len(sys.argv) != MAX_NUM_ARGS:
    print("Usage: [port number]")
else:
    run_server()