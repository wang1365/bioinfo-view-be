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

        'CONN_MAX_AGE': 300,  # 连接最大存活时间（秒），建议设置为60-300
        'OPTIONS': {
            'connect_timeout': 10,  # 连接超时时间
            'keepalives': 1,
            'keepalives_idle': 30,
            'keepalives_interval': 10,
            'keepalives_count': 5,
        }
    }
}
