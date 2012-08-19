
from django.core.management.base import BaseCommand
from socketio.server import SocketIOServer

from core import game
from core.app import GameApplication
from core.settings import SOCKETIO_PORT


class Command(BaseCommand):
    """
    Runs the socket.io server.
    """

    def handle(self, *args, **options):
        game.autodiscover()
        app = GameApplication()
        SocketIOServer(("0.0.0.0", SOCKETIO_PORT), app).serve_forever()
