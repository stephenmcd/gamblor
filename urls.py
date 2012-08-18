
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

from core import game


admin.autodiscover()
game.autodiscover()


urlpatterns = patterns("",
    ("^admin/", include(admin.site.urls)),
    url("", include("social_auth.urls")),
    url("", include("core.urls")),
)
