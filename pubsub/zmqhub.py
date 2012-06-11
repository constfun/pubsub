from threading import Thread
import zmq
from core import Hub


# Create a fowarder in a separate thread with two ends, pub and sub.
# This way we can just 'connect' to this device whenever we need to subscribe to or send a signal.
# see: http://lists.zeromq.org/pipermail/zeromq-dev/2010-July/004411.html
# see: http://lists.zeromq.org/pipermail/zeromq-dev/2010-July/004399.html
class ForwarderDevice(Thread):
    daemon = True

    in_address = 'tcp://127.0.0.1:5555'
    out_address = 'tcp://127.0.0.1:5556'

    def run(self):
        context = zmq.Context.instance()

        try:
            insock = context.socket(zmq.SUB)
            insock.bind(self.in_address)
            insock.setsockopt(zmq.SUBSCRIBE, '')

            outsock = context.socket(zmq.PUB)
            outsock.bind(self.out_address)

            zmq.device(zmq.FORWARDER, insock, outsock)
        except zmq.ZMQError as ex:
            # errno 48 means failed to bind.
            # Probably means the forwarder is already running.
            if not ex.errno == 48:
                raise ex


class ZmqHub(Hub):
    _forwarder = None

    def __init__(self):
        super(ZmqHub, self).__init__()

        if ZmqHub._forwarder is None:
            ZmqHub._forwarder = ForwarderDevice()
            ZmqHub._forwarder.start()

        context = zmq.Context.instance()

        self._out_socket = context.socket(zmq.PUB)
        self._out_socket.connect(ForwarderDevice.in_address)

        self._in_socket = context.socket(zmq.SUB)
        self._in_socket.connect(ForwarderDevice.out_address)
        self._in_socket.setsockopt(zmq.SUBSCRIBE, '')

    def Tx(self, topic, payload):
        self._out_socket.send_json((topic, payload))

    def receive(self):
        try:
            while True:
                topic, payload = self._in_socket.recv_json(flags=zmq.NOBLOCK)
                self.Rx(topic=topic, payload=payload)
        except zmq.ZMQError, ex:
            if not ex.errno == zmq.EAGAIN:
                raise ex

    def fileno(self):
        return self._in_socket.FD
