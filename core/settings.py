
from django.conf import settings


# Default account balance for new users.
DEFAULT_BALANCE = getattr(settings, "DEFAULT_BALANCE", 5000)

# Number of seconds until a game is played, after the first player joins.
BETTING_PERIOD = int(not settings.DEBUG) * 10
BETTING_PERIOD = getattr(settings, "BETTING_PERIOD", BETTING_PERIOD)
