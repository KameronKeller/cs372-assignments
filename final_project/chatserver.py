import sys
import socket
import select
from packetmanager import PacketManager

PACKET_HEADER_SIZE = 2
RECV_BUFFER_SIZE = 4096

def broadcast_chat(s, packet_buffers):
    message = packet_buffers[s]
    print("ccccc")
    print(message)
    for s1 in packet_buffers.keys():
        s1.sendall(message)
    packet_buffers[s] = b''

    return packet_buffers

    # s.sendall(data)

def run_server(port):

    packet_manager = PacketManager(PACKET_HEADER_SIZE, RECV_BUFFER_SIZE)

    read_set = set()
    listening_socket = socket.socket()
    listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listening_socket.bind(('', port))
    listening_socket.listen()
    read_set.add(listening_socket)

    print("waiting for connections")

    packet_buffers = {}
    socket_nicknames = {}

    while True:
        ready_to_read, _, _ = select.select(read_set, {}, {})

        for s in ready_to_read:
            if s == listening_socket:
                new_conn, _ = s.accept()
                peername = new_conn.getpeername()
                print("{}: connected".format(peername))
                read_set.add(new_conn)
                packet_buffers[new_conn] = b''
        
            else:
                packet_buffers[s] = packet_manager.receive_packet(s)
                data_length = len(packet_buffers[s])
                if len(packet_buffers[s]) > 0:
                    packet_buffers = broadcast_chat(s, packet_buffers)
                
                # If this is a hello packet:"
                socket_nicknames[s] = "placeholder nickname"


                if data_length == 0:
                    print("{}: disconnected".format(peername))
                    read_set.remove(s)
                else:
                    packet_length = packet_buffers[s][0:2]
                    print('aaaa')
                    print(int.from_bytes(packet_length))
                    print("{} bytes: {}".format(data_length, packet_buffers[s]))

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