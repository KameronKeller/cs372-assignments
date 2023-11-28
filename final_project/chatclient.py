import sys
import socket
import threading

from chatuicurses import init_windows, read_command, print_message, end_windows
from payload import HelloPayload, ClientToServerChatPayload

def receive_messages():
    ...

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

    receiver_thread = threading.Thread(target=receive_messages, daemon=True)
    receiver_thread.start()

    # Make the client socket and connect
    s = socket.socket()
    s.connect((host, port))
    hello_payload = HelloPayload(nickname)
    hello_packet = hello_payload.build_packet()
    s.sendall(hello_packet)

    # Loop forever sending data at random time intervals
    while True:
        try:
            command = read_command("Enter a thing> ")
        except:
            break

        chat_payload = ClientToServerChatPayload(command)
        chat_packet = chat_payload.build_packet()

        # string_to_send = f"{nickname}> {command}"
        # string_bytes = string_to_send.encode()
        s.sendall(chat_packet)


if __name__ == "__main__":
    sys.exit(main(sys.argv))