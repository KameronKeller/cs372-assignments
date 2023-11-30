import json

packet_buffer = b''

class PacketManager:

    def __init__(self, packet_header_size, buffer_size):
        self.packet_header_size = packet_header_size
        self.buffer_size = buffer_size

    def has_complete_packet(self, packet_buffer):
        # If the packet_buffer is less than the word length size, return false
        if len(packet_buffer) < self.packet_header_size:
            return False
        # Otherwise, verify the complete word has been received
        else:
            payload_size = self.get_payload_size(packet_buffer)
            return len(packet_buffer) >= payload_size + self.packet_header_size
        
    def clear_received_packet(self, total_packet_length):
        global packet_buffer
        packet_buffer = packet_buffer[total_packet_length:]

    def get_payload_size(self, packet_buffer):
        payload_size = packet_buffer[:self.packet_header_size]
        return int.from_bytes(payload_size)

    def extract_packet(self, packet_buffer):
        packet_length = self.get_payload_size(packet_buffer)
        total_packet_length = self.packet_header_size + packet_length
        return total_packet_length, packet_buffer[:total_packet_length]

    def receive_packet(self, socket):
        global packet_buffer
        while True:
            if self.has_complete_packet(packet_buffer):
                total_packet_length, packet = self.extract_packet(packet_buffer)
                self.clear_received_packet(total_packet_length)
                return packet

            data = socket.recv(self.buffer_size)

            # If disconnected
            if len(data) == 0:
                return 0
            
            packet_buffer += data
    
    def get_payload(self, buffer):
        payload = buffer[self.packet_header_size:]
        payload = payload.decode("utf-8")
        payload = json.loads(payload)
        return payload