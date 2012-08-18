
from django.conf import settings


# Default account balance for new users.
DEFAULT_BALANCE = getattr(settings, "DEFAULT_BALANCE", 5000)
