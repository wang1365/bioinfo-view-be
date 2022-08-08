#!/usr/bin/env python3


from bioinformatics.settings import *  # noqa

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "bioinfo",
        "USER": "postgres",
        "PASSWORD": "123456",
        "HOST": "db",
        "PORT": "5432",
    }
}
