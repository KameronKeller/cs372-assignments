import json

class Payload:

    def __init__(self, data):
        self.data = data
        self.payload = self.create_payload(self.data)

    def create_payload(self, data):
        json_data = json.dumps(data)
        return json_data.encode("utf-8")

    def build_packet(self):
        payload_size = (len(self.payload)).to_bytes(length=2, byteorder='big')
        # print("AAA")
        # print(int.from_bytes(payload_size))
        # print(payload_size)
        # print(self.payload)
        # print(payload_size + self.payload)
        # payload_size = payload_size.encode("utf-8")
        return payload_size + self.payload
    
class HelloPayload(Payload):

    def __init__(self, nick):
        self.data = {
            "type": "hello",
            "nick": nick
        }
        Payload.__init__(self, self.data)

class ClientToServerChatPayload(Payload):

    def __init__(self, message):
        self.data = {
            "type": "chat",
            "message": message
        }
        Payload.__init__(self, self.data)

class ServerToClientChatPayload(Payload):

    def __init__(self, nick, message):
        self.data = {
            "type": "chat",
            "nick": nick,
            "message": message
        }
        Payload.__init__(self, self.data)

class JoinPayload(Payload):

    def __init__(self, nick):
        self.join = {
            "type": "join",
            "nick": nick
        }
        Payload.__init__(self, self.data)

class LeavePayload(Payload):

    def __init__(self, nick):
        self.leave = {
            "type": "leave",
            "nick": nick
        }
        Payload.__init__(self, self.data)
