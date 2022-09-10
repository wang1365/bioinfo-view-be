#!/usr/bin/env python3


from bioinformatics.settings import *  # noqa

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "bioinfo_uat",
        "USER": "postgres",
        "PASSWORD": "Bio@2022",
        "HOST": "47.116.137.79",
        "PORT": "5432",
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
