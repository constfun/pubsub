import threading
import json
import pika
from pubsub import ZmqHub, Message

from tbclient.common import config

class RabbitHub():
    def __init__(self, exchange, routing_key):
        self._conn = pika.BlockingConnection(pika.ConnectionParameters(host='tinybullet.com'))

        self._channel = self._conn.channel()

        self._channel.exchange_declare(exchange=exchange, type='topic')
        queue = self._channel.queue_declare(exclusive=True).method.queue
        self._channel.queue_bind(exchange=exchange, queue=queue, routing_key=routing_key)

        self._channel.basic_consume(self.message_received, queue=queue, no_ack=True)

        self._receivers = {}
        self.zmq_hub = ZmqHub()

    def message_received(self, channel, method, properties, body):
        routing_key = method.routing_key
        split_key = routing_key.split('.', 1)
        if len(split_key) < 2:
            return
        message_key = split_key[1]

        try:
            data = json.loads(body)
        except ValueError:
            return

        if not isinstance(data, dict):
            return

        self.zmq_hub.send(Message(message_key)(**data))

    def send(self, message):
        raise NotImplemented()
        self._out_socket.send_json(message)

    def fileno(self):
        return self._conn.socket.fileno()

    def receive_messages(self):
        self._conn.process_data_events()

    def subscribe(self, message, receiver):
        raise NotImplemented()
        assert callable(receiver)

        if message.topic not in self._receivers:
            self._receivers[message.topic] = []

        self._receivers[message.topic].append(safeRef(receiver, self._receiver_deleted))

    def _receiver_deleted(self, receiver_ref):
        raise NotImplemented()
        for topic_receivers in self._receivers.itervalues():
            if receiver_ref in topic_receivers:
                topic_receivers.remove(receiver_ref)
