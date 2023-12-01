import sys
import socket
import select
from packetmanager import PacketManager
from packet import JoinPacket, ServerToClientChatPacket, LeavePacket

PACKET_HEADER_SIZE = 2
RECV_BUFFER_SIZE = 4096

def prepare_response(s, message, nicknames):
    message_type = message["type"]
    packet = None
    is_disconnected = False

    # Build a response based on the message type
    match message_type:
        case "hello":
            packet = JoinPacket(message["nick"])
            nicknames[s] = message["nick"]
        case "chat":
            chat_message = message["message"]

            # If the message is /q, set the is disconnect flag
            if chat_message == "/q":
                packet = LeavePacket(nicknames[s])
                is_disconnected = True
            else:
                packet = ServerToClientChatPacket(nicknames[s], message["message"])

    response = packet.packet
    return response, is_disconnected

    
def broadcast_chat(s, packet_buffers, nicknames):
    # Get the buffer from this socket
    buffer = packet_buffers[s]

    # Prepare the response
    response, is_disconnected = prepare_response(s, buffer, nicknames)

    # Send out the response to all connected clients
    for s1 in packet_buffers.keys():
        s1.sendall(response)

    # If the client is disconnected, remove it from the dicts
    if is_disconnected:
        packet_buffers.pop(s, None)
        nicknames.pop(s, None)

    return packet_buffers


def run_server(port):

    packet_manager = PacketManager(PACKET_HEADER_SIZE, RECV_BUFFER_SIZE)

    # Create a set to hold sockets to listen to
    read_set = set()

    # Create the listening socket
    listening_socket = socket.socket()

    # Allow server to be reused on same port
    listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Setup the listening socket and add to read_set
    listening_socket.bind(('', port))
    listening_socket.listen()
    read_set.add(listening_socket)

    print("Waiting for connections...")

    # Keeps track of each sockets buffer
    packet_buffers = {}

    # Keeps track of each sockets nickname
    nicknames = {}

    while True:
        # Retrieve the next socket that has data ready
        ready_to_read, _, _ = select.select(read_set, {}, {})

        for s in ready_to_read:

            # Watch for new connections
            if s == listening_socket:
                # Accept a new connection
                new_conn, _ = s.accept()
                peername = new_conn.getpeername()
                print("{}: connected".format(peername))

                # Keep track of the connected sockets
                read_set.add(new_conn)

                # Setup an empty buffer in the packet buffer
                packet_buffers[new_conn] = b''
        
            else:
                # Receive incoming data from a connection
                data = packet_manager.receive_packet(s)

                # If there is no data, the client has disconnected
                if not data:
                    print("{}: disconnected".format(peername))
                    read_set.remove(s)
                else:
                    packet_buffers[s] = data
                    packet_buffers = broadcast_chat(s, packet_buffers, nicknames)
                    

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