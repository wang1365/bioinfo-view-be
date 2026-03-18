#!/usr/bin/env python3

import os

from bioinformatics.settings import *  # noqa


def _int_env(name, default):
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "bioinfo",
        "USER": "postgres",
        "PASSWORD": "Bio@2022",
        "HOST": "10.10.0.208",
        "PORT": "5432",

        'CONN_MAX_AGE': _int_env("DB_CONN_MAX_AGE", 60),  # 本地联调可设 DB_CONN_MAX_AGE=0，避免连接长时间占用
        'OPTIONS': {
            'connect_timeout': 10,  # 连接超时时间
            'keepalives': 1,
            'keepalives_idle': 30,
            'keepalives_interval': 10,
            'keepalives_count': 5,
        }
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://10.10.0.208:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # "PASSWORD": "yourpassword", # 换成你自己密码
        },
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
