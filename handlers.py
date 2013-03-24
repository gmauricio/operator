from tornado.websocket import WebSocketHandler as BaseWebSocketHandler
from consumers import Consumer, Exchange

class WebSocketHandler(BaseWebSocketHandler):

    def initialize(self, consumer_manager):
        self.consumer_manager = consumer_manager

    def open(self, *args, **kwargs):
        id = self.get_argument("id")
        consumer_bindings = [
            Exchange('notifications', 'direct')
        ]
        self.consumer_manager.add_consumer(Consumer(id, self, consumer_bindings))

    def on_message(self, message):
        pass

    def on_close(self):
        pass
