from tornado.websocket import WebSocketHandler as BaseWebSocketHandler
from consumers import Consumer

class WebSocketHandler(BaseWebSocketHandler):

    def initialize(self, consumer_manager):
        self.consumer_manager = consumer_manager

    def open(self, *args, **kwargs):
        id = self.get_argument("id")
        print "client connected: "+id
        self.consumer_manager.add_consumer(Consumer(id, self))

    def on_message(self, message):
        pass

    def on_close(self):
        pass
