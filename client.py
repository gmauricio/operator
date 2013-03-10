import pika
from pika.adapters import TornadoConnection
from consumers import ConsumerManager

class PikaClient(ConsumerManager):
    def __init__(self, io_loop, subscription_manager):
        print('PikaClient: __init__')
        self.io_loop = io_loop
        self.connected = False
        self.connecting = False
        self.connection = None
        self.channel = None
        self.subscription_manager = subscription_manager

    def connect(self):
        if self.connecting:
            print('PikaClient: Already connecting to RabbitMQ')
            return

        print('PikaClient: Connecting to RabbitMQ')
        self.connecting = True

        param = pika.ConnectionParameters(host='localhost')
        self.connection = TornadoConnection(param,
            on_open_callback=self.on_connected)
        self.connection.add_on_close_callback(self.on_closed)

    def on_connected(self, connection):
        print('PikaClient: connected to RabbitMQ')
        self.connected = True
        self.connection = connection
        self.connection.channel(self.on_channel_open)

    def on_channel_open(self, channel):
        print('PikaClient: Channel open, Declaring exchange')
        self.channel = channel

    def add_consumer(self, consumer):
        self.consumer.channel(self)

    def on_closed(self, connection):
        print('PikaClient: rabbit connection closed')
        self.io_loop.stop()

