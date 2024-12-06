from wsgiref.simple_server import make_server, WSGIServer, WSGIRequestHandler
from socketserver import ThreadingMixIn


class ThreadingWSGIServer(ThreadingMixIn, WSGIServer):
    daemon_threads = True


class NoLoggingWSGIRequestHandler(WSGIRequestHandler):
    def log_message(self, format, *args):
        pass


class WebServer:
    def __init__(self, wsgi_app, listen="127.0.0.1", port=8080):
        self.wsgi_app = wsgi_app
        self.listen = listen
        self.port = port
        self.server = make_server(
            self.listen, self.port, self.wsgi_app, ThreadingWSGIServer, NoLoggingWSGIRequestHandler
        )

    def serve_forever(self):
        self.server.serve_forever()
