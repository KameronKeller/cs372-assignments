import sys
import socket

# How many bytes is the word length?
WORD_LEN_SIZE = 2

# Sets the buffer size for receiving data
RECV_BUFFER_SIZE = 4096

def usage():
    print("usage: wordclient.py server port", file=sys.stderr)

packet_buffer = b''

def get_word_length(packet_buffer):
    word_length_bytes = packet_buffer[:WORD_LEN_SIZE]
    return int.from_bytes(word_length_bytes)

def complete_word_received(packet_buffer, word_length):
    return len(packet_buffer) >= word_length + WORD_LEN_SIZE

def has_complete_packet(packet_buffer):
    # If the packet_buffer is less than the word length size, return false
    if len(packet_buffer) < WORD_LEN_SIZE:
        return False
    # Otherwise, verify the complete word has been received
    else:
        word_length = get_word_length(packet_buffer)
        return complete_word_received(packet_buffer, word_length)

def extract_packet(packet_buffer):
    word_length = get_word_length(packet_buffer)
    total_packet_length = WORD_LEN_SIZE + word_length
    return total_packet_length, packet_buffer[:total_packet_length]

def clear_received_packet(total_packet_length):
    global packet_buffer
    packet_buffer = packet_buffer[total_packet_length:]

def get_next_word_packet(s):
    """
    Return the next word packet from the stream.

    The word packet consists of the encoded word length followed by the
    UTF-8-encoded word.

    Returns None if there are no more words, i.e. the server has hung
    up.
    """

    global packet_buffer

    while True:
        if has_complete_packet(packet_buffer):
            total_packet_length, packet = extract_packet(packet_buffer)
            clear_received_packet(total_packet_length)
            return packet

        data = s.recv(RECV_BUFFER_SIZE)

        # If no data received, return None to signal a closed connection
        if len(data) == 0:
            return None
        
        packet_buffer += data


def extract_word(word_packet):
    """
    Extract a word from a word packet.

    word_packet: a word packet consisting of the encoded word length
    followed by the UTF-8 word.

    Returns the word decoded as a string.
    """

    word = word_packet[WORD_LEN_SIZE:]
    return word.decode()

# Do not modify:

def main(argv):
    try:
        host = argv[1]
        port = int(argv[2])
    except:
        usage()
        return 1

    s = socket.socket()
    s.connect((host, port))

    print("Getting words:")

    while True:
        word_packet = get_next_word_packet(s)

        if word_packet is None:
            break

        word = extract_word(word_packet)

        print(f"    {word}")

    s.close()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
