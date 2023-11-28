import sys
import socket
import select

PACKET_HEADER_SIZE = 2

RECV_BUFFER_SIZE = 4096

def has_complete_packet(packet_buffer):
    print("called")
    print(packet_buffer)
    if len(packet_buffer) >= PACKET_HEADER_SIZE:
        packet_size = int.from_bytes(packet_buffer[0:PACKET_HEADER_SIZE])
        return len(packet_buffer) == PACKET_HEADER_SIZE + packet_size
    else:
        return False

def receive_packet(socket):
    packet_buffer = b''
    packet_buffer += socket.recv(RECV_BUFFER_SIZE)
    while True:
        if has_complete_packet(packet_buffer):
            print("complete packet received")
            return packet_buffer
        else:
            print("incomplete packet received")

        packet_buffer += socket.recv(RECV_BUFFER_SIZE)

def run_server(port):

    read_set = set()
    listening_socket = socket.socket()
    listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
                buffer = b''
                data = receive_packet(s)
                data_length = len(data)


                if data_length == 0:
                    print("{}: disconnected".format(peername))
                    read_set.remove(s)
                else:
                    packet_length = data[0:2]
                    print('aaaa')
                    print(int.from_bytes(packet_length))
                    print("{} bytes: {}".format(data_length, data))

def usage():
    print("usage: chatserver.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))