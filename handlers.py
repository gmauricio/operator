from tornado.websocket import WebSocketHandler as BaseWebSocketHandler

class WebSocketHandler(BaseWebSocketHandler):

    def open(self, *args, **kwargs):
        pass
        #pika.log.info("WebSocket opened")

    def on_close(self):
        pass
        #pika.log.info("WebSocket closed")
