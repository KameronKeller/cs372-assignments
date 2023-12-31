import sys
import json

BYTE_SIZE = 8
ADDR_BIT_SIZE = 32

def ipv4_to_value(ipv4_addr):
    """
    Convert a dots-and-numbers IP address to a single 32-bit numeric
    value of integer type. Returns an integer type.

    Example:

    ipv4_addr: "255.255.0.0"
    return:    4294901760  (Which is 0xffff0000 hex)

    ipv4_addr: "1.2.3.4"
    return:    16909060  (Which is 0x01020304 hex)
    """
    # Split the address on the dots
    address_split = ipv4_addr.split(".")

    # Convert individual address components from strings to numbers
    hex_addr_bytes = [int(a) for a in address_split]

    # Loop over the values and bit shift by 1 byte each time
    bit_shift_value = ADDR_BIT_SIZE
    integer_representation = 0
    for num in hex_addr_bytes:
        bit_shift_value -= BYTE_SIZE

        # Bitwise-OR the previous result to the current result
        integer_representation |= (num << bit_shift_value)

    return integer_representation

def value_to_ipv4(addr):
    """
    Convert a single 32-bit numeric value of integer type to a
    dots-and-numbers IP address. Returns a string type.

    Example:

    There is only one input value, but it is shown here in 3 bases.

    addr:   0xffff0000 0b11111111111111110000000000000000 4294901760
    return: "255.255.0.0"

    addr:   0x01020304 0b00000001000000100000001100000100 16909060
    return: "1.2.3.4"
    """
    num_bytes = int(ADDR_BIT_SIZE/BYTE_SIZE)

    # A single byte of all 1's used to and values against
    one_byte_all_ones = 255
    bit_shift_value = 0
    output = []

    # Iterate over the number of bytes, shifting the addr value by 1 byte each time
    # And the address against 255 to extract the last byte
    # Insert the extracted byte to the front of an array
    for _ in range(num_bytes):
        output.insert(0, (addr >> bit_shift_value) & one_byte_all_ones)
        bit_shift_value += BYTE_SIZE

    # convert each value to a string
    output = [str(x) for x in output]

    # Join the string together to get the final value
    return ".".join(output)


def get_subnet_mask_value(slash):
    """
    Given a subnet mask in slash notation, return the value of the mask
    as a single number of integer type. The input can contain an IP
    address optionally, but that part should be discarded.

    Returns an integer type.

    Example:

    There is only one return value, but it is shown here in 3 bases.

    slash:  "/16"
    return: 0xffff0000 0b11111111111111110000000000000000 4294901760

    slash:  "10.20.30.40/23"
    return: 0xfffffe00 0b11111111111111111111111000000000 4294966784
    """

    # Get the slash value
    slash_value = int(slash.split("/")[1])

    # Set the starting at 0
    output = 0

    # Fill the value with 1s up to the number of slash values
    for i in range(ADDR_BIT_SIZE):
        output = output << 1

        # If the value should be 1, or the value with 1
        if i < slash_value:
            output |= 1
    
    return output



def ips_same_subnet(ip1, ip2, slash):
    """
    Given two dots-and-numbers IP addresses and a subnet mask in slash
    notataion, return true if the two IP addresses are on the same
    subnet.

    Returns a boolean.

    FOR FULL CREDIT: this must use your get_subnet_mask_value() and
    ipv4_to_value() functions. Don't do it with pure string
    manipulation.

    This needs to work with any subnet from /1 to /31

    Example:

    ip1:    "10.23.121.17"
    ip2:    "10.23.121.225"
    slash:  "/23"
    return: True
    
    ip1:    "10.23.230.22"
    ip2:    "10.24.121.225"
    slash:  "/16"
    return: False
    """

    subnet_value = get_subnet_mask_value(slash)

    ip_val_1 = ipv4_to_value(ip1)
    ip_val_2 = ipv4_to_value(ip2)
    
    subnet_comparison = (ip_val_1 & subnet_value) == (ip_val_2 & subnet_value)

    return subnet_comparison

def get_network(ip_value, netmask):
    """
    Return the network portion of an address value as integer type.

    Example:

    ip_value: 0x01020304
    netmask:  0xffffff00
    return:   0x01020300
    """

    return ip_value & netmask

def find_router_for_ip(routers, ip):
    """
    Search a dictionary of routers (keyed by router IP) to find which
    router belongs to the same subnet as the given IP.

    Return None if no routers is on the same subnet as the given IP.

    FOR FULL CREDIT: you must do this by calling your ips_same_subnet()
    function.

    Example:

    [Note there will be more data in the routers dictionary than is
    shown here--it can be ignored for this function.]

    routers: {
        "1.2.3.1": {
            "netmask": "/24"
        },
        "1.2.4.1": {
            "netmask": "/24"
        }
    }
    ip: "1.2.3.5"
    return: "1.2.3.1"


    routers: {
        "1.2.3.1": {
            "netmask": "/24"
        },
        "1.2.4.1": {
            "netmask": "/24"
        }
    }
    ip: "1.2.5.6"
    return: None
    """

    same_subnet = None

    for router, netmask in routers.items():
        if ips_same_subnet(ip, router, netmask["netmask"]):
            same_subnet = router

    return same_subnet