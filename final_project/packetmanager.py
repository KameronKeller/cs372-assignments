class PacketManager:

    def __init__(self, packet_header_size, buffer_size):
        self.packet_header_size = packet_header_size
        self.buffer_size = buffer_size

    def has_complete_packet(self, packet_buffer):
        if len(packet_buffer) >= self.packet_header_size:
            packet_size = int.from_bytes(packet_buffer[0:self.packet_header_size])
            return len(packet_buffer) == self.packet_header_size + packet_size
        else:
            return False

    def receive_packet(self, socket):
        packet_buffer = b''
        packet_buffer += socket.recv(self.buffer_size)
        while True:
            if self.has_complete_packet(packet_buffer):
                return packet_buffer

            packet_buffer += socket.recv(self.buffer_size)