from tornado.websocket import WebSocketHandler as BaseWebSocketHandler
from consumers import Consumer

class WebSocketHandler(BaseWebSocketHandler):

    def initialize(self, subscription_manager, consumer_manager):
#        self.subscription_manager = subscription_manager
        self.consumer_manager = consumer_manager

    def open(self, *args, **kwargs):
        id = self.get_argument("id")
        print "client connected: "+id
#        self.subscription_manager.subscribe(id, self)
        self.consumer_manager.add_consumer(Consumer(id, self))

    def on_message(self, message):
        pass
        #for subscriber in self.subscription_manager.get_all_subscribers():
         #   subscriber.write_message(message)

    def on_close(self):
        pass
