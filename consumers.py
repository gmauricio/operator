class ConsumerManager():

    def __init__(self):
        self.consumers = []

    def add_consumer(self, consumer):
        self.consumers.append(consumer)
        self.on_added_consumer(consumer)

    def on_added_consumer(self, consumer):
        pass


class Consumer():

    def __init__(self, id, listener):
        self.id = id
        self.listener = listener

    def on_message(self, body):
        self.listener.write_message(body)

    def channel(self, channel):
        self.channel = channel
        self.channel.exchange_declare(callback=self._on_exchange_declared,
                                      exchange='notifications',
                                      exchange_type='direct')

    def _on_exchange_declared(self, result):
        self.channel.queue_declare(self._on_queue_declared)

    def _on_queue_declared(self, result):
        self.queue = result.method.queue
        self.channel.queue_bind(callback=self._on_queue_bound,
                                exchange='notifications',
                                queue=self.queue,
                                routing_key=self.id)

    def _on_queue_bound(self, result):
        self.channel.basic_consume(self.on_message, queue=self.queue)

    def on_message(self, channel, method, header, body):
        print('PikaClient: message received: %s' % body)
        self.listener.write_message(body)