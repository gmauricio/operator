import os
import tornado.ioloop
import tornado.web
from handlers import WebSocketHandler
import client
from subscription import SubscriptionManager


class EchoHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write("Echo")

def main():

    subscription_manager = SubscriptionManager()

    application = tornado.web.Application([
        (r'/ws', WebSocketHandler, dict(subscription_manager = subscription_manager)),
        (r'/', EchoHandler)
    ])

    io_loop = tornado.ioloop.IOLoop.instance()

    # PikaClient is our rabbitmq consumer
    pc = client.PikaClient(io_loop, subscription_manager)

    pc.connect()

    application.listen(os.environ.get("PORT", 8888))

    io_loop.start()

if __name__ == "__main__":
    main()