TCP_MAX_BYTE_LENGTH = 2
CHECKSUM_START = 16
CHECKSUM_END = 18

def get_IP_address(tcp_addrs):
    # Split the source and destination addresses
    addresses = tcp_addrs.split()

    # Reassign addresses to their own variables
    source = addresses[0]
    destination = addresses[1]

    # Split the numbers on the "."
    source_numbers = source.split(".")
    destination_numbers = destination.split(".")

    # Create buffers to hold the bytestring representation
    source_ip = b''
    destination_ip = b''

    # Build the bytestrings
    for n in source_numbers:
        source_ip += int(n).to_bytes()
    for n in destination_numbers:
        destination_ip += int(n).to_bytes()
    
    return source_ip, destination_ip

def generate_IP_pseudo_header(tcp_addrs, tcp_length):
    zero = 0x00
    ptcl = 0x06

    # Get the IP bytestrings
    source_ip_bytes, dest_ip_bytes = get_IP_address(tcp_addrs)

    # Concatenate the pseudo header
    pseudo_header = source_ip_bytes + dest_ip_bytes + zero.to_bytes() + ptcl.to_bytes() + tcp_length.to_bytes(TCP_MAX_BYTE_LENGTH)

    return pseudo_header

def extract_checksum(tcp_data):
    # Slice the checksum out of the data
    checksum = tcp_data[CHECKSUM_START:CHECKSUM_END]
    return int.from_bytes(checksum)

def get_zero_checksum(tcp_data):
    # Zero out the checksum in the data
    tcp_zero_cksum = tcp_data[:CHECKSUM_START] + b'\x00\x00' + tcp_data[CHECKSUM_END:]
    return tcp_zero_cksum

def force_even_length(tcp_zero_cksum):
    # Add an extra 0 byte if the length is odd
    if len(tcp_zero_cksum) % 2 == 1:
        tcp_zero_cksum += b'\x00'
    return tcp_zero_cksum

def extract_16_bit_words(pseudo_header, tcp_zero_cksum):
    words = []

    # Concatenate pseudo header and TCP header copy
    data = pseudo_header + tcp_zero_cksum

    offset = 0   # byte offset into data

    while offset < len(data):
        # Slice 2 bytes out and get their value:

        word = int.from_bytes(data[offset:offset + 2], "big")
        words.append(word)

        offset += 2   # Go to the next 2-byte value

    return words

def compute_checksum(pseudo_header, tcp_zero_cksum):
    tcp_zero_cksum = force_even_length(tcp_zero_cksum)
    words_16_bit = extract_16_bit_words(pseudo_header, tcp_zero_cksum)

    total = 0

    for word in words_16_bit:
        total += word
        total = (total & 0xffff) + (total >> 16)

    return (~total) & 0xffff

def compare_checksum(original, calculated):
    if original == calculated:
        print("PASS")
    else:
        print("FAIL")

def tcp_validator(tcp_addr_path, tcp_data_path):
    # Read IP file
    with open(tcp_addr_path, "r") as fp:
        tcp_addrs = fp.read()

    # Read .dat file
    with open(tcp_data_path, "rb") as fp:
        tcp_data = fp.read()
        tcp_length = len(tcp_data)

    # Generate IP pseudo header
    pseudo_header = generate_IP_pseudo_header(tcp_addrs, tcp_length)

    # Extract the original checksum
    original_checksum = extract_checksum(tcp_data)

    # Build TCP header copy with zero'd checksum
    tcp_zero_cksum = get_zero_checksum(tcp_data)

    # Compute checksum
    computed_checksum = compute_checksum(pseudo_header, tcp_zero_cksum)

    # Compare checksums
    compare_checksum(original_checksum, computed_checksum)

def main():
    for i in range(10):
        tcp_addr_path = "tcp_data/tcp_addrs_{}.txt".format(i)
        tcp_data_path = "tcp_data/tcp_data_{}.dat".format(i)
        tcp_validator(tcp_addr_path, tcp_data_path)

if __name__ == "__main__":
    main()