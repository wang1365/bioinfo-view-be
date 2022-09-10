#!/usr/bin/env python3
import os

from bioinformatics.settings import *  # noqa

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": 'bioinfo',
        "USER": "postgres",
        "PASSWORD": "Bio@2022",
        "HOST": "localhost",
        "PORT": 5432,
    }
}
