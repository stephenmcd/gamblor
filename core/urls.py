
from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns("core.views",
    url("^logout/$", "logout", name="logout"),
    url(r'^$', "index", name="index"),
)
