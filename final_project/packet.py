import json


class Packet:
    def __init__(self, data):
        self.data = data
        self.payload = self.create_payload(self.data)
        self.payload_size = (len(self.payload)).to_bytes(length=2, byteorder="big")
        self.packet = self.build_packet()

    def create_payload(self, data):
        json_data = json.dumps(data)
        return json_data.encode("utf-8")

    def build_packet(self):
        return self.payload_size + self.payload


class HelloPacket(Packet):
    def __init__(self, nick):
        self.data = {"type": "hello", "nick": nick}
        Packet.__init__(self, self.data)


class ClientToServerChatPacket(Packet):
    def __init__(self, message):
        self.data = {"type": "chat", "message": message}
        Packet.__init__(self, self.data)


class ServerToClientChatPacket(Packet):
    def __init__(self, nick, message):
        self.data = {"type": "chat", "nick": nick, "message": message}
        Packet.__init__(self, self.data)


class JoinPacket(Packet):
    def __init__(self, nick):
        self.data = {"type": "join", "nick": nick}
        Packet.__init__(self, self.data)


class LeavePacket(Packet):
    def __init__(self, nick):
        self.data = {"type": "leave", "nick": nick}
        Packet.__init__(self, self.data)
