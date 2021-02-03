import datetime
import json
from concurrent import futures

import grpc

import PubSub_pb2 as PubSub
import PubSub_pb2_grpc as rpc
import redis

servers = []


class PubSubServer(rpc.PubSubServerServicer):

    def __init__(self):
        self.listening = redis.Redis(host='localhost', port=6379)
        self.listening = self.listening.pubsub()
        self.listening.subscribe('chat')
        self.sending = redis.Redis(host='localhost', port=6379, )

    # The stream which will be used to send new messages to clients
    def PubSubStream(self, request_iterator, context):
        last_timestamp = ''
        for item in self.listening.listen():
            if item['data'] != 1:
                data = json.loads(item['data'])
                if data["timestamp"] <= last_timestamp:
                    continue
                n = PubSub.Note()
                n.name = data['user']
                n.message = data['message']
                yield n
                last_timestamp = data["timestamp"]

    def SendNote(self, request: PubSub.Note, context):
        self.sending.publish('chat', json.dumps(
            {'message': request.message, 'user': request.name, 'timestamp': str(datetime.datetime.now())}))
        return PubSub.Empty()


class MyServers:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379)
        ports = self.redis.get('ports')
        if not ports:
            self.ports = []
        else:
            self.ports = json.loads(ports)

    def server_initialize(self, address, port):
        try:
            server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
            rpc.add_PubSubServerServicer_to_server(
                PubSubServer(), server)
            while port in self.ports:
                port += 1
            server.add_insecure_port(address + ':' + str(port))
            server.start()
            servers.append(server)
            self.ports.append(port)
            self.redis.set('ports', json.dumps(self.ports))
            return address, port
        except:
            pass


myserver = MyServers()
PubSubserver = PubSubServer()