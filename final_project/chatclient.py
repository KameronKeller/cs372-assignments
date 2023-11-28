import sys
import socket
import threading

from chatuicurses import init_windows, read_command, print_message, end_windows

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

    # Loop forever sending data at random time intervals
    while True:
        try:
            command = read_command("Enter a thing> ")
        except:
            break

        string_to_send = f"{nickname}> {command}"
        string_bytes = string_to_send.encode()
        s.send(string_bytes)


if __name__ == "__main__":
    sys.exit(main(sys.argv))