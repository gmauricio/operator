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
        print('PikaClient: Connecting to RabbitMQ')

        param = pika.ConnectionParameters(host='localhost')
        self.connection = TornadoConnection(param,
            on_open_callback=self.on_connected)
        self.connection.add_on_close_callback(self.on_closed)

    def on_connected(self, connection):
        print('PikaClient: connected to RabbitMQ')
        self.connection = connection
        self.connection.channel(self.on_channel_open)

    def on_channel_open(self, channel):
        print('PikaClient: Channel open')
        self.channel = channel

    def on_added_consumer(self, consumer):
        consumer.channel(self.channel)

    def on_closed(self, connection):
        print('PikaClient: rabbit connection closed')
        self.io_loop.stop()

