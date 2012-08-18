
from Cookie import Cookie

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import SESSION_KEY
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from socketio import socketio_manage
from socketio.mixins import BroadcastMixin
from socketio.namespace import BaseNamespace
from redis import Redis, ConnectionPool


redis = Redis(connection_pool=ConnectionPool())


class GamblorNamespace(BaseNamespace, BroadcastMixin):
    """
    Per-user socket.io namespace for event handlers.
    """

    def on_start(self):
        """
        Set up the initial user. We only have access to the
        HTTP environment, so we use the session ID in the cookie
        and look up a user with it. If a valid user is found, we
        add them to the user set in redis, and broadcast their
        join event to everyone else.
        """
        try:
            cookie = Cookie(self.environ["HTTP_COOKIE"])
            session_key = cookie[settings.SESSION_COOKIE_NAME].value
            session = Session.objects.get(session_key=session_key)
            user_id = session.get_decoded().get(SESSION_KEY)
            user = User.objects.get(id=user_id)
        except (KeyError, ObjectDoesNotExist):
            self.user = None
        else:
            self.user = {"name": user.username, "id": user.id}
            self.broadcast_event_not_me("join", self.user)
            redis.sadd("users", self.user)
        # Send the current set of users to the new socket.
        self.emit("users", list(redis.smembers("users")))

    def recv_disconnect(self):
        """
        Socket disconnected - if the user was authenticated, remove
        them from redis and broadcast their leave event.
        """
        self.disconnect()
        if self.user:
            redis.srem("users", self.user)
            self.broadcast_event_not_me("leave", self.user)


class Application(object):
    """
    Standard socket.io wsgi application.
    """

    def __call__(self, environ, start_response):
        if environ["PATH_INFO"].startswith("/socket.io/"):
            socketio_manage(environ, {"": GamblorNamespace})
        else:
            start_response('404 Not Found', [])
            return ['<h1>Not Found</h1>']
