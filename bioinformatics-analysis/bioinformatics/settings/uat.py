#!/usr/bin/env python3


from bioinformatics.settings import *  # noqa

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "bioinfo",
        "USER": "postgres",
        "PASSWORD": "123456",
        "HOST": "47.116.137.79",
        "PORT": "5432",
    }
}
