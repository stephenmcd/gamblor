
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView


admin.autodiscover()

urlpatterns = patterns("",
    ("^admin/", include(admin.site.urls)),
    #url("", include("gamblor.urls")),
    url("", include("social_auth.urls")),
    url(r'^$', lambda r: TemplateView.as_view(template_name="index.html")(r)),
)
