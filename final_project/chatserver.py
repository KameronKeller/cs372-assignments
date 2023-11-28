import sys
import socket
import select
from packetmanager import PacketManager
from payload import JoinPayload, ServerToClientChatPayload, LeavePayload

PACKET_HEADER_SIZE = 2
RECV_BUFFER_SIZE = 4096

def prepare_response_to(message):
    message_type = message["type"]
    packet = None
    match message_type:
        case "hello":
            join_message = JoinPayload(message["nick"])
            packet = join_message.build_packet()
            # return join_packet
        case "chat":
            chat_message = message["message"]
            if chat_message == "/q":
                leave_message = LeavePayload("placeholder nick")
                packet = leave_message.build_packet()
            else:
                chat_message = ServerToClientChatPayload("placeholder nick", message["message"])
                packet = chat_message.build_packet()
            # return chat_packet
    return packet

    

def broadcast_chat(s, packet_buffers, packet_manager):
    message = packet_buffers[s]
    print(message)
    # response = b''
    # if message == 0:
    #     print("MADE IT HERE")

    #     response = leave_packet
    #     print(response)
    # else:
    response = prepare_response_to(packet_manager.get_payload(message))
    for s1 in packet_buffers.keys():
        s1.sendall(response)

    # Reset the packet buffer after it has been sent
    packet_buffers[s] = b''

    return packet_buffers


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
                # print("{}: connected".format(peername))
                read_set.add(new_conn)
                packet_buffers[new_conn] = b''
        
            else:
                data = packet_manager.receive_packet(s)
                # if data == 0:
                #     packet_buffers[s] = 0
                #     # send leavepacket
                #     # remove socket from dictionaries
                # else:
                packet_buffers[s] = data
                data_length = len(data)
                if len(data) > 0:
                    packet_buffers = broadcast_chat(s, packet_buffers, packet_manager)
                    
                    # If this is a hello packet:"
                    socket_nicknames[s] = "placeholder nickname"


                # if data_length == 0:
                #     print("{}: disconnected".format(peername))
                #     read_set.remove(s)
                # else:
                #     packet_length = packet_buffers[s][0:2]
                #     print('aaaa')
                #     print(int.from_bytes(packet_length))
                #     print("{} bytes: {}".format(data_length, packet_buffers[s]))

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