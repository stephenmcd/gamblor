
from os import makedirs
from os.path import join, exists
from urllib import urlretrieve

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from social_auth.signals import socialauth_registered

from core.settings import DEFAULT_BALANCE


class Account(models.Model):
    """
    A user's account balance.
    """
    user = models.OneToOneField(User)
    balance = models.IntegerField(default=DEFAULT_BALANCE)


@receiver(post_save, sender=User)
def user_saved(sender, **kwargs):
    """
    Create an initial account balance for new users.
    """
    Account.objects.get_or_create(user=kwargs["instance"])


@receiver(socialauth_registered, sender=None)
def avatar(sender, user, response, details, **kwargs):
    """
    Download the user's Twitter or Facebook avatar once they've
    authenticated via either service.
    """
    try:
        # twitter
        photo_url = response["profile_image_url"]
        photo_url = "_reasonably_small".join(photo_url.rsplit("_normal", 1))
    except KeyError:
        # facebook
        uid = response["id"]
        photo_url = "http://graph.facebook.com/%s/picture?type=large" % uid
    path = join(settings.MEDIA_ROOT, "photos")
    if not exists(path):
        makedirs(path)
    urlretrieve(photo_url, join(path, str(user.id)))
