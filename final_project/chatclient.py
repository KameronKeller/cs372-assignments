import sys
import socket
import threading
import time

from chatuicurses import init_windows, read_command, print_message, end_windows
from packet import HelloPacket, ClientToServerChatPacket
from packetmanager import PacketManager

# Time in seconds for client to automatically close when server disconnects
SERVER_DISCONNECT_TIMEOUT = 3 
PACKET_HEADER_SIZE = 2
RECV_BUFFER_SIZE = 4096

def exit_client(s):
    s.close()
    end_windows()
    sys.exit()

def shutdown_client(s):
    print_message("*** Unable to send message ***")
    print_message("*** Connection was closed by the server ***")
    print_message("*** This client will exit in {} seconds ***".format(SERVER_DISCONNECT_TIMEOUT))
    time.sleep(SERVER_DISCONNECT_TIMEOUT)
    exit_client(s)

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
    server_closed_trigger = kwargs["trigger"]
    packet_manager = PacketManager(PACKET_HEADER_SIZE, RECV_BUFFER_SIZE)

    while True:
        message = packet_manager.receive_packet(s)

        # If no message received, the server is shutdown
        # Trigger the thread event to close the client
        # Else, display the message in the TUI
        if not message:
            server_closed_trigger.set()
        else:
            output = prepare_output(message)
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
    
    # Initialize the TUI
    init_windows()

    # Make the client socket and attempt to connect
    s = socket.socket()
    try:
        s.connect((host, port))
    except:
        # Close client if unable to connect
        print("*** Unable to connect to the server ***")
        exit_client(s)

    # Create an event to watch for a shutdown server
    server_closed_trigger = threading.Event()

    # Create the message displaying thread
    receiver_thread = threading.Thread(target=receive_messages, kwargs={"socket":s, "trigger":server_closed_trigger}, daemon=True)
    receiver_thread.start()

    # Create and send hello packet to server
    hello_packet = HelloPacket(nickname)
    s.sendall(hello_packet.packet)

    while True:
        try:
            command = read_command("{}> ".format(nickname))
            if server_closed_trigger.is_set():
                shutdown_client(s)
        except:
            break

        # Create and send a chat packet
        chat_packet = ClientToServerChatPacket(command)
        s.sendall(chat_packet.packet)

        # If the command is /q, exit
        if command == "/q":
            exit_client(s)

if __name__ == "__main__":
    sys.exit(main(sys.argv))