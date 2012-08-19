
from random import randint

from django.conf import settings
from django.contrib.auth.models import User
from gevent import sleep, spawn

from core.forms import GameForm
from core.settings import BETTING_PERIOD


registry = {}


def autodiscover():
    """
    Look for any ``games`` modules in installed apps to ensure they
    get registered.
    """
    for app in settings.INSTALLED_APPS:
        try:
            __import__("%s.games" % app)
        except ImportError:
            pass


class GameBase(type):
    """
    Whenever Game is subclassed, add a new game instance to the registry.
    """
    def __new__(cls, name, bases, attrs):
        attrs.setdefault("Form", GameForm)
        new = super(GameBase, cls).__new__(cls, name, bases, attrs)
        name = name.lower()
        # Don't register the base Game class, and don't register the
        # Dummy game if we have others - we don't know which order
        # they'll be registered in, so we block Dummy if we have any
        # games, and remove Dummy if it's registered and another game
        # is registered.
        if name != "game" and not (name == "dummy" and registry):
            if name != "dummy" and "dummy" in registry:
                del registry["dummy"]
            registry[name] = new(name)
        return new


class Game(object):
    """
    Base class for games. Subclasses should override the bet()
    method to perform validation of game specific betting args,
    and the outcome() method, which receives each player's betting
    args and returns True if the args perform a win.
    """

    __metaclass__ = GameBase

    def __init__(self, name):
        self.name = name
        self.template = "games/%s.html" % self.name
        self.form = self.__class__.Form()
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
            spawn(self.turn)
        user_id = namespace.user["id"]
        self.players.setdefault(user_id, {"amount": 0})
        self.players[user_id]["namespace"] = namespace
        self.players[user_id]["amount"] += amount
        self.players[user_id]["bet_args"] = bet_args
        return True

    def broadcast(self, *args):
        """
        Piggyback the first connected player's namespace to
        broadcast a message.
        """
        for player in self.players.values():
            if player["namespace"].socket.connected:
                player["namespace"].broadcast_event(*args)
                break

    def pause(self):
        """
        Pause for settings.BETTING_PERIOD - used to simulate dice roll,
        wheel spin, etc.
        """
        sleep(BETTING_PERIOD)

    def turn(self, callback=None, callback_args=None, callback_kwargs=None):
        """
        Takes an actual turn of the game - called within a separate
        greenlet on the first call to bet(). We iterate through each of
        the players passing their bet_args to outcome() which multiplies
        the amount bet, and build a results dict we can broadcast back
        to all sockets.
        """
        self.pause()
        results = {}
        for user_id, player in self.players.items():
            result = self.outcome(*player["bet_args"])
            results[user_id] = player["amount"] * result
            if results[user_id] > 0:
                # Put a positive bet amount back into the user's account.
                user = User.objects.get(id=user_id)
                user.account.balance += (results[user_id] * 2)
                user.account.save()
        if callback:
            callback_args = callback_args or ()
            callback_kwargs = callback_kwargs or {}
            callback(*callback_args, **callback_kwargs)
        self.broadcast("game_end", self.name, results)
        self.reset()

    def reset(self):
        self.players = {}


class Dummy(Game):
    """
    Default game with no input - just randomly win lose or draw.
    If any other games are registered, this one is removed.
    """
    def outcome(self):
        # Give back 0 (lose), 1 (even) or 2 (win) times the bet.
        return randint(0, 2)
