#!/usr/bin/env python3

from bioinformatics.settings import *   # noqa

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "bioinfo",
        "USER": "postgres",
        "PASSWORD": "Bio@2022",
        "HOST": "10.10.0.208",
        "PORT": "5432",
    }
}
