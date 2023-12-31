# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select

RECV_BUFFER_SIZE = 4096

def run_server(port):

    read_set = set()
    listening_socket = socket.socket()
    listening_socket.bind(('', port))
    listening_socket.listen()
    read_set.add(listening_socket)

    print("waiting for connections")

    while True:
        ready_to_read, _, _ = select.select(read_set, {}, {})

        for s in ready_to_read:
            if s == listening_socket:
                new_conn, _ = s.accept()
                peername = new_conn.getpeername()
                print("{}: connected".format(peername))
                read_set.add(new_conn)
        
            else:
                data = s.recv(RECV_BUFFER_SIZE)
                data_length = len(data)

                if data_length == 0:
                    print("{}: disconnected".format(peername))
                    read_set.remove(s)
                else:
                    print("{} {} bytes: {}".format(peername, data_length, data))


#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
