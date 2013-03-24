import pika
from pika.adapters import TornadoConnection
from consumers import ConsumerManager

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