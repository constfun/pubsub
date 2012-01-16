import sys
import traceback
from saferef import safeRef

class Hub(object):
    def __init__(self):
        self._receivers = {}
        self._forward_to_hubs = []

    def send(self, message):
        topic, payload = message
        self.Tx(topic=topic, payload=payload)

    def Rx(self, topic, payload):
        for hub in self._forward_to_hubs:
            hub.Tx(topic=topic, payload=payload)

        if topic not in self._receivers:
            return

        if not isinstance(payload, dict):
            return

        for receiver_ref in self._receivers[topic]:
            try:
                receiver_ref()(**payload)
            except:
                # TODO: log instead of print
                ex_type, ex_val, tb = sys.exc_info()
                traceback.print_tb(tb)
                print 'Error in message callback. Skipping. ex_type: %s ex_val: %s' % (ex_type, ex_val)

    def forward_to_hub(self, hub):
        assert hub is not self
        assert self not in hub._forward_to_hubs

        if hub not in self._forward_to_hubs:
            self._forward_to_hubs.append(hub)

    def subscribe(self, message, receiver):
        assert callable(receiver)

        if message.topic not in self._receivers:
            self._receivers[message.topic] = []

        self._receivers[message.topic].append(safeRef(receiver, self._receiver_deleted))

    def _receiver_deleted(self, receiver_ref):
        for topic_receivers in self._receivers.itervalues():
            if receiver_ref in topic_receivers:
                topic_receivers.remove(receiver_ref)


class Message:
    def __init__(self, topic):
        self.topic = topic

    # Support 'message_with_payload(like="so")'
    def __call__(self, **payload):
        return (self.topic, payload)

    #... and also unpacking of 'an_empty_message'
    def __iter__(self):
        for item in (self.topic, {}):
            yield item
