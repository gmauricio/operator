import pika
from pika.adapters import TornadoConnection

class ConsumerManager():

    def __init__(self):
        self.consumers = []
        self.exchanges = []

    def add_consumer(self, consumer):
        self.consumers.append(consumer)
        self.on_added_consumer(consumer)

    def on_added_consumer(self, consumer):
        pass

    def add_exchange(self, exchange):
        self.exchanges.append(exchange)

class Consumer():

    def __init__(self, id, listener, bindings=None):
        if not bindings: bindings = []
        self.bindings = bindings
        self.id = id
        self.listener = listener

    def on_message(self, body):
        self.listener.write_message(body)

    def channel(self, channel):
        self.channel = channel
        self.channel.queue_declare(self._on_queue_declared)


    def bind_to(self, exchange):
        routing_key = None
        if exchange.type is 'direct': routing_key = self.id
        self.channel.queue_bind(callback=self._on_queue_bound,
                                    exchange=exchange.name,
                                    queue=self.queue,
                                    routing_key=routing_key)

    def _on_queue_declared(self, result):
        self.queue = result.method.queue
        self._bind()
        self.channel.basic_consume(self.on_message, queue=self.queue)

    def _bind(self):
        for exchange_to_bind in self.bindings:
            self.bind_to(exchange_to_bind)

    def _on_queue_bound(self, result):
        pass

    def on_message(self, channel, method, header, body):
        self.listener.write_message(body)


class PikaClient(ConsumerManager):
    def __init__(self, io_loop):
        ConsumerManager.__init__(self)
        self.io_loop = io_loop
        self.connection = None
        self.channel = None

    def connect(self):
        param = pika.ConnectionParameters(host='localhost')
        self.connection = TornadoConnection(param,
                                            on_open_callback=self.on_connected)
        self.connection.add_on_close_callback(self.on_closed)

    def on_connected(self, connection):
        self.connection = connection
        self.connection.channel(self.on_channel_open)

    def on_channel_open(self, channel):
        self.channel = channel
        self.declare_exchanges()

    def declare_exchanges(self):
        for exchange in self.exchanges:
            self.channel.exchange_declare(callback=self._on_exchange_declared,
                                      exchange=exchange.name,
                                      exchange_type=exchange.type)

    def _on_exchange_declared(self, result):
        pass

    def on_added_consumer(self, consumer):
        consumer.channel(self.channel)

    def on_closed(self, connection):
        self.io_loop.stop()

class Exchange():
    def __init__(self, name, type):
        self.name = name
        self.type = type