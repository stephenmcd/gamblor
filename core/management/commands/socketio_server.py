
from django.core.management.base import BaseCommand
from socketio.server import SocketIOServer

from core.app import GameApplication
from core import game


class Command(BaseCommand):

    def handle(self, *args, **options):
        game.autodiscover()
        SocketIOServer(("0.0.0.0", 9000), GameApplication()).serve_forever()
