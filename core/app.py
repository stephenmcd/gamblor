
from socketio import socketio_manage
from socketio.namespace import BaseNamespace


class GamblorNamespace(BaseNamespace):
    pass


class Application(object):

    def __call__(self, environ, start_response):
        if environ["PATH_INFO"].startswith("/socket.io/"):
            socketio_manage(environ, {"": GamblorNamespace})
        else:
            start_response('404 Not Found', [])
            return ['<h1>Not Found</h1>']
