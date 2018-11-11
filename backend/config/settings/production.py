from .base import *
from django.utils import six

DEBUG = False

# SECURITY CONFIGURATION
# ------------------------------------------------------------------------------
SECRET_KEY = env('DJANGO_SECRET_KEY')
ADMIN_URL=env('DJANGO_ADMIN_URL', default='axeront')

SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    'DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    'DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', default=True)
SECURE_BROWSER_XSS_FILTER = True

SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)

X_FRAME_OPTIONS = 'DENY'

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['torgosvet.ru'])




MEDIA_ROOT = "/var/media/"
MEDIA_URL = '/media/'


# SMTP CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader', ]),
]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': True
        }
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": 'redis://%s:%d/%d' % (REDIS_HOST, REDIS_PORT, REDIS_DB),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "example"
    }
}

# DATABASE CONFIGURATION START
# ------------------------------------------------------------------------------
POSTGRES_DATABASE = env('DJANGO_POSTGRES_DATABASE')
POSTGRES_USER = env('DJANGO_POSTGRES_USER')
POSTGRES_PASSWORD = env('DJANGO_POSTGRES_PASSWORD')
POSTGRES_HOST = env('DJANGO_POSTGRES_HOST')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': POSTGRES_DATABASE,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': POSTGRES_HOST,
        'PORT': '5432',
    }
}
# DATABASE CONFIGURATION END
# ------------------------------------------------------------------------------
