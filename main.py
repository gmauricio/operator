import tornado.ioloop
import tornado.web
#from handlers import WebSocketHandler

#application = tornado.web.Application([
#    (r'/ws', WebSocketHandler),
#])

"""def main():
    pika.log.setup(color=True)
    io_loop = tornado.ioloop.IOLoop.instance()

    # PikaClient is our rabbitmq consumer

    pc = client.PikaClient(io_loop)

    application.pc = pc

    application.pc.connect()

    application.listen(8888)

    io_loop.start()"""

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

application = tornado.web.Application([
    (r"/", MainHandler),
])


if __name__ == "__main__":
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
