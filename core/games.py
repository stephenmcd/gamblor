
from random import choice, randint

from django.contrib.auth.models import User
from django import forms
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
            if name != "dummy":
                del game_registry["dummy"]
            game_registry[name] = new(name)
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


    def turn(self):
        """
        Takes an actual turn of the game - called within a separate
        greenlet on the first call to bet(). We iterate through each of
        the players passing their bet_args to outcome() which multiplies
        the amount bet, and build a results dict we can broadcast back
        to all sockets.
        """
        sleep(BETTING_PERIOD)
        results = {}
        for user_id, player in self.players.items():
            result = self.outcome(*player["bet_args"])
            results[user_id] = player["amount"] * result
            if results[user_id] > 0:
                # Put a positive bet amount back into the user's account.
                user = User.objects.get(id=user_id)
                user.account.balance += (results[user_id] * 2)
                user.account.save()
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


ROULETTE_CHOICES = range(0, 37)


class Roulette(Game):

    class Form(GameForm):
        number = forms.ChoiceField(choices=[(c, c) for c in ROULETTE_CHOICES])

    def turn(self):
        self.landed_on = str(choice(ROULETTE_CHOICES))
        super(Roulette, self).turn()

    def outcome(self, choice):
        return (choice == self.landed_on) * len(ROULETTE_CHOICES)
