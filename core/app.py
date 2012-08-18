
from Cookie import Cookie

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import SESSION_KEY
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils.translation import ugettext_lazy as _
from socketio import socketio_manage
from socketio.mixins import BroadcastMixin
from socketio.namespace import BaseNamespace
from redis import Redis, ConnectionPool

from core.games import game_registry


redis = Redis(connection_pool=ConnectionPool())


class Game(object):
    """
    Base class for games. Subclasses should override the bet()
    method to perform validation of game specific betting args,
    and the won() method, which receives each player's betting
    args and returns True if the args perform a win.
    """

    def __init__(self, name):
        self.name = name
        self.reset()

    def bet(self, namespace, amount, bet_args):
        """
        Called each time a player bets. When there are no players,
        a greenlet is spawned that will trigger the play of a
        turn of the game.

        Player's socketio namespace is passed through so that we
        have a way to broadcast back results once the turn is complete.

        The bet_args argument will be specific for each type of game.

        Subsequent calls to bet() for the same player prior to the turn
        being played, will update their betting arguments, and increase
        their bet.
        """
        if not self.players:
            spawn(self.play)
        user_id = namespace.user["id"]
        self.players.setdefault(user_id, {"amount": 0})
        self.players[user_id]["namespace"] = namespace
        self.players[user_id]["amount"] += amount
        self.players[user_id]["bet_args"] = bet_args
        return True

    def play(self):
        """
        Takes an actual turn of the game - called within a separate
        greenlet on the first call to bet(). We iterate through each of
        the players passing their betting_args to won(), and build a
        results dict we can broadcast back to all sockets. We piggyback
        the first player we find that's still connected, to broadcast
        the results back.
        """
        sleep(BETTING_PERIOD)
        broadcaster = None
        results = {}
        for user_id, player in self.players.items():
            results[user_id] = player["amount"]
            if self.won(player["bet_args"]):
                # Put double the bet amount back into the user's account.
                user = User.objects.get(id=user_id)
                user.account.balance += (results[user_id] * 2)
                user.account.save()
            else:
                results[user_id] *= -1
            if broadcaster is None and player["namespace"].socket.connected:
                broadcaster = player["namespace"]
        if broadcaster is not None:
            broadcaster.broadcast_event("game_end", self.name, results)
        self.reset()

    def reset(self):
        self.players = {}

    def won(self, bet_args):
        return randint(0, 1)


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
        for game in game_registry.values():
            self.emit("game_users", game.name, game.players.keys())

    def recv_disconnect(self):
        """
        Socket disconnected - if the user was authenticated, remove
        them from redis and broadcast their leave event.
        """
        self.disconnect()
        if self.user:
            redis.srem("users", self.user)
            self.broadcast_event_not_me("leave", self.user)

    def on_bet(self, game_name, amount, *bet_args):
        """
        Takes a bet for a game.
        """
        import pdb; pdb.set_trace()
        try:
            assert self.user is not None       # Must have a user
            assert isinstance(amount, int)     # Amount must be int
            assert amount > 0                  # Amount must be positive
            assert game_name in game_registry  # Game must be valid
        except AssertionError:
            return
        user = User.objects.get(id=self.user["id"])
        user.account.balance -= amount
        if user.account.balance < 0:
            self.emit("notice", _("You don't have that amount to bet"))
        else:
            game = game_registry[game_name]
            if game.bet(self, amount, bet_args):
                user.account.save()
            self.broadcast_event("game_users", game_name, game.players.keys())


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
