from hashlib import md5

from django.contrib.sites.models import Site


def get_current_site():
    site = Site.objects.get_current()
    return site


def get_md5(str):
    m = md5(str.encode("utf-8"))
    return m.hexdigest()
