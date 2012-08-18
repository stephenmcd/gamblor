
from django.contrib.auth import logout as auth_logout
from django.contrib.messages import info, error
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _


def index(request):
    return render(request, "index.html", {})

def logout(request):
    auth_logout(request)
    info(request, _("Successfully logged out"))
    return redirect("index")
