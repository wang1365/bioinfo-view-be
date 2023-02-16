#!/usr/bin/env python3


from bioinformatics.settings import *  # noqa

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
