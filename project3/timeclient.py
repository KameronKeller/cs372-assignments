import socket
import time

address = "time.nist.gov"
port = 37
num_bytes_recv = 4096

def system_seconds_since_1900():
    """
    The time server returns the number of seconds since 1900, but Unix
    systems return the number of seconds since 1970. This function
    computes the number of seconds since 1900 on the system.
    """

    # Number of seconds between 1900-01-01 and 1970-01-01
    seconds_delta = 2208988800

    seconds_since_unix_epoch = int(time.time())
    seconds_since_1900_epoch = seconds_since_unix_epoch + seconds_delta

    return seconds_since_1900_epoch


def main():
    # Connect to the server
    s = socket.socket()
    s.connect((address, port))

    # Receive data
    d = s.recv(num_bytes_recv)
    s.close()

    # Decode the data
    nist_seconds = int.from_bytes(d)

    # Print the value of the time server
    print("NIST time  : {}".format(nist_seconds))

    # Print the system time
    system_time = system_seconds_since_1900()
    print("System time: {}".format(system_time))
    

if __name__ == "__main__":
    main()
