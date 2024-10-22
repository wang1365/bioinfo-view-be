"""
Django settings for bioinformatics project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = "lm44m5=bg*+f^2v^2&rfl)cs5e&5g+50@*p7!u-j&@fmg1yv-_"

SECRET_KEY = (os.environ.get("DJANGO_SECRET_KEY")
              or "lm44m5=bg*+f^2v^2&rfl)cs5e&5g+50@*p7!u-j&@fmg1yv-_")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    'corsheaders',
    'django_extensions',
    'rest_framework',
    "account",
    "project",
    "sample",
    "task",
    "rbac",
    "flow",
    "config",
    "appearance",
    "patient",
    "report",
    "resource_limit",
    # "django_filters"
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "middlewares.security.SecurityMiddleware",
    "middlewares.logging.LoggingMiddleware",
]

ROOT_URLCONF = "bioinformatics.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "bioinformatics.wsgi.application"

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'
#
# TIME_ZONE = 'UTC'
#
# USE_I18N = True
#
# USE_L10N = True
#
# USE_TZ = True
LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = "/static/"

# email config
# EMAIL_HOST_PASSWORD = "vefqvvmganwtebfe"
# EMAIL_HOST_USER = "2514553187@qq.com"
# EMAIL_HOST = "smtp.qq.com"
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = "天之谷 <2514553187@qq.com>"

MEDIA_URL = "/media/"

EMAIL_SENDER = "reporting2@nanodigmbio.com"
EMAIL_HOST = "smtp.qiye.163.com"
EMAIL_PORT = 994
EMAIL_PASSWORD = "Nano2020"

# AUTH_USER_MODEL = "account.Account"
SITE_ID = 1
APPEND_SLASH = False
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES",
                                        60 * 600)

MAX_TASK = os.getenv("MAX_TASK", 10)

SAMPLE_SHELL_ENV = {
    # "文库编号": "library_type",
    # "样本类型2": "sample_type",
    # "index编号": "index_number",
    # "测序平台": "platform",
    # "测序类型": "test_type",
    # "探针内容": "prob_content",
    # "fastq1文件地址": "fastq1_path",
    # "fastq2文件地址": "fastq2_path",
    # "bam1文件地址": "bam1_path",
    # "bam1比对软件": "bam1_tool",
    # "bam2文件地址": "bam2_path",
    # "bam2比对软件": "bam2_tool",
    # "标准品": "standard_code",
    # "backup1": "backup1",
    # "backup2": "backup2",
    # "backup3": "backup3",
    # "backup4": "backup4",
    # "backup5": "backup5",
    # "backup6": "backup6",
    # "backup7": "backup7",
    # "backup8": "backup8",
    # "backup9": "backup9",
    # "backup10": "backup10",
}


BAM_PATH = os.getenv("BAM_PATH", "/nano/bam")

TASK_RESULT_DIR = os.getenv("TASK_RESULT_DIR", "/tmp")

MOVE_OTHERS_DIR = os.getenv("MOVE_OTHERS_DIR", "/nano/result/other")
MOVE_QC_DIR = os.getenv("MOVE_QC_DIR", "/nano/result/qc")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",  # 这里直接使用redis别名作为host ip地址
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # "PASSWORD": "yourpassword", # 换成你自己密码
        },
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

DISABLE_JOB_RUN = False

# REST_FRAMEWORK = {
#    # 过滤器默认后端
#     'DEFAULT_FILTER_BACKENDS': (
#            'django_filters.rest_framework.DjangoFilterBackend',),
# }