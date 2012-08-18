
from random import choice

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
