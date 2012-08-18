
from Cookie import Cookie

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from socketio import socketio_manage
from socketio.mixins import BroadcastMixin
from socketio.namespace import BaseNamespace
from redis import Redis, ConnectionPool


redis = Redis(connection_pool=ConnectionPool())


class GamblorNamespace(BaseNamespace, BroadcastMixin):

    def on_start(self):
        try:
            cookie = Cookie(self.environ["HTTP_COOKIE"])
            session_key = cookie["sessionid"].value
            session = Session.objects.get(session_key=session_key)
            user_id = session.get_decoded().get("_auth_user_id")
            user = User.objects.get(id=user_id)
        except (KeyError, ObjectDoesNotExist):
            self.user = None
        else:
            self.user = {"name": user.username, "id": user.id}
            self.broadcast_event_not_me("join", self.user)
            redis.sadd("users", self.user)
        self.emit("users", list(redis.smembers("users")))

    def recv_disconnect(self):
        self.disconnect()
        if self.user:
            redis.srem("users", self.user)
            self.broadcast_event_not_me("leave", self.user)


class Application(object):

    def __call__(self, environ, start_response):
        if environ["PATH_INFO"].startswith("/socket.io/"):
            socketio_manage(environ, {"": GamblorNamespace})
        else:
            start_response('404 Not Found', [])
            return ['<h1>Not Found</h1>']
