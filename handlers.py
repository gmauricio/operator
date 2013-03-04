from tornado.websocket import WebSocketHandler as BaseWebSocketHandler

class WebSocketHandler(BaseWebSocketHandler):

    def initialize(self, subscription_manager):
        self.subscription_manager = subscription_manager

    def open(self, *args, **kwargs):
        id = self.get_argument("id")
        self.subscription_manager.subscribe(id, self)
        #pika.log.info("WebSocket opened")

    def on_message(self, message):
        pass

    def on_close(self):
        pass
        #pika.log.info("WebSocket closed")
