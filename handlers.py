from tornado.websocket import WebSocketHandler as BaseWebSocketHandler

class WebSocketHandler(BaseWebSocketHandler):

    def initialize(self, subscription_manager):
        self.subscription_manager = subscription_manager

    def open(self, *args, **kwargs):
        id = self.get_argument("id")
        print "client connected: "+id
        self.subscription_manager.subscribe(id, self)

    def on_message(self, message):
        for subscriber in self.subscription_manager.get_all_subscribers():
            subscriber.write_message(message)

    def on_close(self):
        pass
