#!/usr/bin/env python3

from bioinformatics.settings import *   # noqa

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "bioinfo",
        "USER": "postgres",
        "PASSWORD": "Bio@2022",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}
