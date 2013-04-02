import os
import tornado.ioloop
import tornado.web
from consumers import PikaClient, Exchange
from handlers import WebSocketHandler
import config

class EchoHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write("Echo")

def main():

    io_loop = tornado.ioloop.IOLoop.instance()

    pc = PikaClient(io_loop)

    pc.add_exchange(Exchange('notifications', 'direct'))
    pc.add_exchange(Exchange('publications', 'fanout'))

    pc.connect(config.CLOUDAMQP_URL)

    application = tornado.web.Application([
        (r'/ws', WebSocketHandler, dict(consumer_manager = pc)),
        (r'/', EchoHandler)
    ])

    application.listen(os.environ.get("PORT", 8888))

    io_loop.start()

if __name__ == "__main__":
    main()