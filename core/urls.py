
from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns("core.views",
    url("^logout/$", "logout", name="logout"),
    url("^logged_in/$", "logged_in", name="logged_in"),
    url("^login_error/$", "login_error", name="login_error"),
    url(r'^$', "index", name="index"),
)
