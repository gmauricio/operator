import os
import tornado.ioloop
import tornado.web
from handlers import WebSocketHandler
from subscription import SubscriptionManager


class EchoHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write("Echo")

application = tornado.web.Application([
    (r'/ws', WebSocketHandler, dict(subscription_manager = SubscriptionManager)),
    (r'/', EchoHandler)
])

def main():
    #pika.log.setup(color=True)
    io_loop = tornado.ioloop.IOLoop.instance()

    # PikaClient is our rabbitmq consumer
    #pc = client.PikaClient(io_loop)

    #application.pc = pc

    #application.pc.connect()

    application.listen(os.environ.get("PORT", 8888))

    io_loop.start()

if __name__ == "__main__":
    main()