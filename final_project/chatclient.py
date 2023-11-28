import sys
import socket
import threading

from chatuicurses import init_windows, read_command, print_message, end_windows
from payload import HelloPayload, ClientToServerChatPayload, LeavePayload
from packetmanager import PacketManager

PACKET_HEADER_SIZE = 2
RECV_BUFFER_SIZE = 4096

def prepare_output(message):
    message_type = message["type"]
    output = ""
    match message_type:
        case "join":
            output = "*** {} has joined the chat".format(message["nick"])
        case "chat":
            output = "{}: {}".format(message["nick"], message["message"])
        case "leave":
            output = "*** {} has left the chat".format(message["nick"])
    return output

def receive_messages(**kwargs):
    s = kwargs["socket"]
    packet_manager = PacketManager(PACKET_HEADER_SIZE, RECV_BUFFER_SIZE)

    while True:
        data = packet_manager.receive_packet(s)
        message = packet_manager.get_payload(data)
        output = prepare_output(message)
        if len(data) > 0: # can this condition somehow be abstracted into the receive packets method?
            print_message(output)

def usage():
    print("usage: chatclient.py nickname host port", file=sys.stderr)

def main(argv):
    try:
        nickname = argv[1]
        host = argv[2]
        port = int(argv[3])
    except:
        usage()
        return 1
    
    init_windows()

    # Make the client socket and connect
    s = socket.socket()
    s.connect((host, port))

    receiver_thread = threading.Thread(target=receive_messages, kwargs={"socket":s}, daemon=True)
    receiver_thread.start()

    hello_payload = HelloPayload(nickname)
    hello_packet = hello_payload.build_packet()
    s.sendall(hello_packet)

    # Loop forever sending data at random time intervals
    while True:
        try:
            command = read_command("{}> ".format(nickname))
        except:
            break
        
        #     leave_payload = LeavePayload(nickname) # this isn't the correct way
        #     leave_packet = leave_payload.build_packet()
        #     s.sendall(leave_packet)
        # else:
        chat_payload = ClientToServerChatPayload(command)
        chat_packet = chat_payload.build_packet()
        s.sendall(chat_packet)
        if command == "/q":
            s.close()
            end_windows()
            sys.exit()

        # string_to_send = f"{nickname}> {command}"
        # string_bytes = string_to_send.encode()
        # s.sendall(chat_packet)


if __name__ == "__main__":
    sys.exit(main(sys.argv))