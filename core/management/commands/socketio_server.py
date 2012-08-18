
from django.core.management.base import BaseCommand
from socketio.server import SocketIOServer

from core.app import Application


class Command(BaseCommand):

    def handle(self, *args, **options):
        SocketIOServer(("0.0.0.0", 9000), Application()).serve_forever()


