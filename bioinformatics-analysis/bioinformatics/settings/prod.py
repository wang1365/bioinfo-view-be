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

log_dir = os.path.join(os.getenv('BIO_ROOT'), 'logs', 'web')
os.makedirs(log_dir, exist_ok=True)
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
        'file': {
            # 实际开发建议使用ERROR
            'level': 'INFO',
            'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
            # 日志位置,日志文件名,日志保存目录必须手动创建，注：这里的文件路径要注意BASE_DIR代表的是小love
            'filename': os.path.join(log_dir, "bioinformatics.log"),
            # 日志文件的最大值,这里我们设置300M
            'maxBytes': 300 * 1024 * 1024,
            # 日志文件的数量,设置最大日志数量为10
            'backupCount': 10,
            # 日志格式:详细格式
            'formatter': 'verbose',
            # 文件内容编码
            'encoding': 'utf-8'
        },
    },
    'loggers': {
        '': {
            'level': LOGLEVEL,
            'handlers': ['console', 'file'],
        },
        'django.db.backends': {
            'handlers': ['db', 'file'],
            'propagate': False,
            'level': 'DEBUG',
        },
    }
}
