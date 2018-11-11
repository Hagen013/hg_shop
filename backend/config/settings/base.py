import os
import environ

env = environ.Env()
env.read_env()

# Корневая директория проекта
ROOT_DIR = environ.Path(__file__) - 4  # (hg_shop/backend/config/settings/base.py - 3 = backend/)


# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)


# SECURITY SETINGS
# ------------------------------------------------------------------------------
SECRET_KEY=env('DJANGO_SECRET_KEY')
ADMIN_URL=env('DJANGO_ADMIN_URL', default='admin')


# SESSIONS SETINGS
# ------------------------------------------------------------------------------
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'


# APPLICATIONS CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
]

THIRD_PARTY_APPS = [
    'mptt',
    'rest_framework',
    'django_extensions',
    'digg_paginator',
    'django_redis',
    'imagekit'
]

LOCAL_APPS = [
    'core',
    'cart',
    'orders',
    'search',
    'sitemap',
    'api',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(ROOT_DIR.path('frontend/templates')),
        ],
        'OPTIONS': {
        'loaders': [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ],
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
                'django.template.context_processors.media',
                # Custom context processors
                'context_processors.menu_catalog.menu',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# PASSWORD VALIDATION
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# INTERNATIONALIZATION
# ------------------------------------------------------------------------------
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# MAIL SETTINGS
# ------------------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# REST API
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {  
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
    'PAGINATE_BY': 10
}


# STATIC FILES
# ------------------------------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    str(ROOT_DIR.path('frontend/static')),
)
STATIC_ROOT = str((ROOT_DIR)('compose/nginx/staticfiles'))


# REDIS SETTINGS
# ------------------------------------------------------------------------------
REDIS_PORT = env('REDIS_PORT', default=6379)
REDIS_DB = env('REDIS_DB', default=0)
REDIS_HOST = env('REDIS_HOST', default='redis')


# RABBIT SETTINGS
# ------------------------------------------------------------------------------
RABBIT_HOSTNAME = env('RABBIT_HOSTNAME', default='rabbit')

if RABBIT_HOSTNAME.startswith('tcp://'):  
    RABBIT_HOSTNAME = RABBIT_HOSTNAME.split('//')[1]

BROKER_URL = env('BROKER_URL', default='')

if not BROKER_URL:  
    BROKER_URL = 'amqp://{user}:{password}@{hostname}/{vhost}'.format(
        user=env('RABBIT_ENV_USER', default='admin'),
        password=env('RABBITMQ_DEFAULT_PASS', default='mypass'),
        hostname=RABBIT_HOSTNAME,
        vhost=env('RABBIT_ENV_VHOST', default=''))


# We don't want to have dead connections stored on rabbitmq, so we have to negotiate using heartbeats
BROKER_HEARTBEAT = '?heartbeat=30'  
if not BROKER_URL.endswith(BROKER_HEARTBEAT):  
    BROKER_URL += BROKER_HEARTBEAT

BROKER_POOL_LIMIT = 1  
BROKER_CONNECTION_TIMEOUT = 10


# CELERY SETTINGS
# ------------------------------------------------------------------------------
CELERY_RESULT_BACKEND = 'redis://%s:%d/%d' % (REDIS_HOST, REDIS_PORT, REDIS_DB)  
CELERY_REDIS_MAX_CONNECTIONS = 5

CELERY_TASK_SERIALIZER = "json"  
CELERY_ACCEPT_CONTENT = ['application/json']

CELERY_ALWAYS_EAGER=False
CELERY_IGNORE_RESULT = False


# SMTP SETTINGS
# ------------------------------------------------------------------------------

EMAILS_ADMIN = env('DJANGO_EMAILS_ADMIN')
EMAIL_HOST_USER = env('DJANGO_EMAIL_HOST_USER')
EMAIL_PORT = env('DJANGO_EMAIL_PORT')
EMAIL_HOST = env('DJANGO_EMAIL_HOST')
EMAIL_HOST_PASSWORD = env('DJANGO_EMAIL_HOST_PASSWORD')

IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = 'imagekit.cachefiles.strategies.Optimistic'

SITE_ID = 2