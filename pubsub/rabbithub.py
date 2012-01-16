import json
import pika
from core import Hub

class RabbitHub(Hub):
    def __init__(self, host, exchange):
        super(RabbitHub, self).__init__()

        self._conn = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.exchange = exchange

    def set_routing_key(self, routing_key):
        self._channel = self._conn.channel()

        self._channel.exchange_declare(exchange=self.exchange, type='topic')
        queue = self._channel.queue_declare(exclusive=True).method.queue
        self._channel.queue_bind(exchange=self.exchange, queue=queue, routing_key=routing_key)

        self._channel.basic_consume(self._message_received, queue=queue, no_ack=True)

    def Tx(self, topic, payload):
        raise NotImplemented()

    def receive(self):
        self._conn.process_data_events()

    def _message_received(self, channel, method, properties, body):
        # routing_key should be in the form route_key.topic
        routing_key = method.routing_key
        split_key = routing_key.split('.', 1)
        if len(split_key) < 2:
            return
        topic = split_key[1]

        try:
            payload = json.loads(body)
        except ValueError:
            return

        self.Rx(topic=topic, payload=payload)

    def fileno(self):
        return self._conn.socket.fileno()
