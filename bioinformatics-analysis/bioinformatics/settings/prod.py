#!/usr/bin/env python3
import os

from bioinformatics.settings import *  # noqa

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": "db",
        "PORT": os.getenv("POSTGRES_PORT"),
    }
}

LOGLEVEL = os.getenv('DJANGO_LOGLEVEL', 'info').upper()
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s]%(levelname)s %(process)d [%(name)s:%(lineno)s] %(message)s',
        },
        'simple': {
            'format': '[%(asctime)s] ==> %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'db': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        '': {
            'level': LOGLEVEL,
            'handlers': ['console'],
        },
        'django.db.backends': {
            'handlers': ['db'],
            'propagate': False,
            'level': 'DEBUG',
        },
    }
}