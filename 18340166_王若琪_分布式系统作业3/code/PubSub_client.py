import grpc
import PubSub_pb2 as PubSub
import PubSub_pb2_grpc as rpc
import threading
from server import myserver


class PubSubClass:
    def __init__(self, address, port):
        channel = grpc.insecure_channel(address + ':' + str(port))
        self.conn = rpc.PubSubServerStub(channel)
        self.username = input("Enter your name : ")

        threading.Thread(target=self.recive, daemon=True).start()

        self.send()

    def send(self):
        message = ''
        while message != 'exit':
            message = input()
            n = PubSub.Note()
            n.name = self.username  # set the username
            n.message = message
            self.conn.SendNote(n)

    def recive(self):
        for note in self.conn.PubSubStream(PubSub.Empty()):  # this line will wait for new messages from the server!
            if note.name and note.name != self.username:
                print("{} : {}\n".format(note.name, note.message))


address, port = myserver.server_initialize(address='localhost', port=11912)

ch = PubSubClass(address, port)

while True:
    ch.receive()