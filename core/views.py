
from django.contrib.auth import logout as auth_logout
from django.contrib.messages import info, error
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _

from core.game import game_registry
from core.settings import SOCKETIO_PORT


def index(request):
    context = {
        "SOCKETIO_PORT": SOCKETIO_PORT,
        "games": game_registry.values(),
    }
    return render(request, "index.html", context)


def logged_in(request):
    info(request, _("Logged in as %s" % request.user))
    return redirect("index")


def login_error(request):
    error(request, _("An error occurred logging in"))
    return redirect("index")


def logout(request):
    auth_logout(request)
    info(request, _("Successfully logged out"))
    return redirect("index")
