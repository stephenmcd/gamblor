
from random import choice, randint

from django.forms import ChoiceField

from core.game import Game


ROULETTE_CHOICES = range(0, 37)


class Roulette(Game):

    class Form(Game.Form):
        number = ChoiceField(choices=[(c, c) for c in ROULETTE_CHOICES])

    def turn(self):
        self.landed_on = str(choice(ROULETTE_CHOICES))
        self.broadcast("roulette_landed_on", self.landed_on)
        super(Roulette, self).turn()

    def outcome(self, choice):
        return (choice == self.landed_on) * len(ROULETTE_CHOICES)


class Craps(Game):

    def roll_dice(self):
        once = lambda: randint(1, 6)
        return [once(), once()]

    def turn(self):
        self.wins = (7, 11)
        self.loses = (2, 3, 12)
        self.rolled = self.roll_dice()
        total = sum(self.rolled)
        if total not in self.wins + self.loses:
            self.pause()
            self.broadcast("craps_rolled", self.rolled, True)
            self.wins = (total,)
            self.rolled = self.roll_dice()
        self.broadcast("craps_rolled", self.rolled)
        super(Craps, self).turn()

    def outcome(self):
        return int(sum(self.rolled) in self.wins)
