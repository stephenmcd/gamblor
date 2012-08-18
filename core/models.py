
from os import makedirs
from os.path import join, exists
from urllib import urlretrieve

from django.conf import settings
from social_auth.signals import socialauth_registered


def create_profile(sender, user, response, details, **kwargs):
    try:
        # twitter
        photo_url = response["profile_image_url"]
        photo_url = "_reasonably_small".join(photo_url.rsplit("_normal", 1))
    except KeyError:
        # facebook
        photo_url = "http://graph.facebook.com/%s/picture?type=large" % response["id"]
    path = join(settings.MEDIA_ROOT, "photos")
    if not exists(path):
        makedirs(path)
    urlretrieve(photo_url, join(path, str(user.id)))

socialauth_registered.connect(create_profile, sender=None)
