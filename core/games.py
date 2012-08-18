
from random import randint

from django.contrib.auth.models import User
from gevent import sleep, spawn

from core.forms import GameForm
from core.settings import BETTING_PERIOD


game_registry = {}


class GameBase(type):
    """
    Whenever Game is subclassed, add a new game instance to the registry.
    """
    def __new__(cls, name, bases, attrs):
        attrs.setdefault("Form", GameForm)
        new = super(GameBase, cls).__new__(cls, name, bases, attrs)
        name = name.lower()
        if name != "game":
            game_registry[name] = new(name)
        return new


class Game(object):
    """
    Base class for games. Subclasses should override the bet()
    method to perform validation of game specific betting args,
    and the won() method, which receives each player's betting
    args and returns True if the args perform a win.
    """

    __metaclass__ = GameBase

    def __init__(self, name):
        self.form = self.__class__.Form()
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
        the players passing their bet_args to won(), and build a
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


class Dummy(Game):

    def won(self, bet_args):
        return randint(0, 1)
