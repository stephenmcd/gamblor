
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns("",
    ("^admin/", include(admin.site.urls)),
    #url("", include("gamblor.urls")),
    url("", include("social_auth.urls")),
)
