import json
import logging

packet_buffer = b''

class PacketManager:

    def __init__(self, packet_header_size, buffer_size):
        logging.basicConfig(filename='packetmanager.log', encoding='utf-8', level=logging.DEBUG)
        self.packet_header_size = packet_header_size
        self.buffer_size = buffer_size

    def has_complete_packet(self, packet_buffer):
        # If the packet_buffer is less than the word length size, return false
        if len(packet_buffer) < self.packet_header_size:
            return False
        # Otherwise, verify the complete word has been received
        else:
            payload_size = self.get_payload_size(packet_buffer)
            logging.debug("---------")
            logging.debug(packet_buffer)
            logging.debug("payload_size: {}".format(payload_size))
            logging.debug("len(packet_buffer): {}".format(len(packet_buffer)))
            logging.debug("2 + payload_size: {}".format(self.packet_header_size + payload_size))
            logging.debug("---------")
            return len(packet_buffer) >= payload_size + self.packet_header_size

    # def has_complete_packet(self, packet_buffer):
    #     if len(packet_buffer) < self.packet_header_size:
    #         return False
    #     else:

    #     if len(packet_buffer) >= self.packet_header_size:
    #         packet_size = int.from_bytes(packet_buffer[0:self.packet_header_size])
    #         logging.debug("---------")
    #         logging.debug(packet_buffer)
    #         logging.debug("packet_size: {}".format(packet_size))
    #         logging.debug("len(packet_buffer): {}".format(len(packet_buffer)))
    #         logging.debug("2 + packet_size: {}".format(self.packet_header_size + packet_size))
    #         logging.debug("---------")
    #         return len(packet_buffer) == self.packet_header_size + packet_size
    #     else:
    #         return False
        
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
                logging.debug(packet_buffer)
                total_packet_length, packet = self.extract_packet(packet_buffer)
                self.clear_received_packet(total_packet_length)
                logging.debug("packet")
                logging.debug(packet)
                return packet

            data = socket.recv(self.buffer_size)
            logging.debug(data)

            # If disconnected
            if len(data) == 0:
                return 0
            
            packet_buffer += data
        # packet_buffer += data
    
    def get_payload(self, buffer):
        payload = buffer[self.packet_header_size:]
        payload = payload.decode("utf-8")
        payload = json.loads(payload)
        return payload