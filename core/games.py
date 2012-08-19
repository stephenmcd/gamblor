
from random import choice, randint

from django.forms import ChoiceField

from core.game import Game


ROULETTE_CHOICES = range(0, 37)
CRAP_WINS = (7, 11)
CRAP_LOSES = (2, 3, 12)


class Roulette(Game):
    """
    Simplified Roulette - we can only bet on single numbers, not groups.
    """

    class Form(Game.Form):
        """
        Adds a choice field for each of the numbers on the wheel.
        """
        number = ChoiceField(choices=[(c, c) for c in ROULETTE_CHOICES])

    def turn(self):
        """
        Each turn assigns a random choice from the numbers on the wheel.
        """
        self.landed_on = str(choice(ROULETTE_CHOICES))
        callback_args = ("roulette_landed_on", self.landed_on)
        super(Roulette, self).turn(self.broadcast, callback_args)

    def outcome(self, choice):
        """
        Payout is multiplied by the odds, eg: number of items on the wheel.
        """
        return (choice == self.landed_on) * len(ROULETTE_CHOICES)


class Craps(Game):
    """
    Simplified Craps - we only roll once more if we hit point,
    eg: no wins or losses on the first roll.
    """

    def roll_dice(self):
        """
        Random pair of dice rolls.
        """
        once = lambda: randint(1, 6)
        return [once(), once()]

    def turn(self):
        """
        Roll once for a win or a loss, then again for a point.
        """
        self.rolled = self.roll_dice()
        total = sum(self.rolled)
        if total in CRAP_WINS + CRAP_LOSES:
            self.wins = CRAP_WINS
        else:
            # Point hit (no wins or losses) - just roll again.
            self.pause()
            self.broadcast("craps_rolled", self.rolled, True)
            # Winning amount needs to be the point.
            self.wins = (total,)
            self.rolled = self.roll_dice()
        self.broadcast("craps_rolled", self.rolled)
        super(Craps, self).turn()

    def outcome(self):
        """
        Sequence of possible wins either contains standard 7/11, or
        a point if rolled.
        """
        return int(sum(self.rolled) in self.wins)
