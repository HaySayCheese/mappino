#coding=utf-8
import os
from mappino import passwords
from psycopg2cffi import compat



# cffi hook (needed by pypy)
compat.register()


DEBUG = True
SMS_DEBUG = DEBUG
TEMPLATE_DEBUG = DEBUG


ADMINS = (
    ('Dima Chizhevsky', 'dima@mappino.com'),
)
MANAGERS = (
    ('Dima Chizhevsky', 'support@mappino.com')
)
SUPPORT_EMAIL =  MANAGERS[0][1]
BILLING_MANAGER_EMAIL = MANAGERS[0][1]
MODERATORS = MANAGERS[0][1]

# Configuration for emails about server error.
# This is used only for django-internal email sending mechanism,
# and is not used by the application.
#
# To send email notifications application uses mandrill library and other API keys.
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'Dima.Chizhevsky@gmail.com'
EMAIL_HOST_PASSWORD = passwords.MANDRILL_API_KEY
EMAIL_USE_TLS = True
SERVER_EMAIL = 'wall-e@mappino.com'



HUL1_INTERNAL_IP = '10.133.187.144'
EVE1_INTERNAL_IP = '10.133.187.40'


DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME': 'mappino',
        'USER': 'mappino',
        'PASSWORD': passwords.DB_PASSWORD,
        'HOST': EVE1_INTERNAL_IP,
    'PORT': 6432, # pg_bounce is used
    },
    'markers_index': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mappino-indexes',
        'USER': 'mappino',
        'PASSWORD': passwords.INDEX_DB_PASSWORD,
        'HOST': EVE1_INTERNAL_IP, # todo: create separate database for indexes
        'PORT': 6432, # pg_bounce is used
    }
}
DATABASE_ROUTERS = ['core.database_router.Router', ]


REDIS_DATABASES = {
    'throttle': {
        'HOST': HUL1_INTERNAL_IP,
        'PORT': 6379,
    },
    'steady': {
        'HOST': HUL1_INTERNAL_IP,
        'PORT': 6379,
    },
    'cache': {
        'HOST': HUL1_INTERNAL_IP,
        'PORT': 6379,
    },
    'celery': {
        'HOST': HUL1_INTERNAL_IP,
        'PORT': 6379,
    },
}

SPHINX_SEARCH_DATABASE = {
    'HOST': HUL1_INTERNAL_IP,
    'PORT': 9306
}
ENABLE_SPHINX_SEARCH = True


CACHES = {
    'default': {
        # Даний кеш неявно використовується django-compressor для зберігання імен опрацьованих файлів.

        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '{0}:{1}'.format(
            REDIS_DATABASES['cache']['HOST'],
            REDIS_DATABASES['cache']['PORT']
        ),
        'OPTIONS': {
            'DB': 15,
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 10,
                'timeout': 20
            }
        }
    }
}


BROKER_URL = 'redis://{0}:{1}/0'.format(
    REDIS_DATABASES['celery']['HOST'],
    REDIS_DATABASES['celery']['PORT']
)
BROKER_TRANSPORT_OPTIONS = {
    # If a task is not acknowledged within the Visibility Timeout
    # the task will be redelivered to another worker and executed.
    #
    # This causes problems with ETA/countdown/retry tasks
    # where the time to execute exceeds the visibility timeout;
    # in fact if that happens it will be executed again, and again in a loop.
    #
    # So you have to increase the visibility timeout
    # to match the time of the longest ETA you are planning to use.
    'visibility_timeout': 60 * 60 * 6 # in seconds
}
CELERY_RESULT_BACKEND = BROKER_URL


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',

    # 'core',
    'core.users',
    'core.ban',

    'core.publications',
    'core.favorites',
    'core.claims',
    'core.markers_index',
    'core.support',
    'core.escaped_fragments_manager',

    # todo: shift this apps into core

    'apps.main.api.correspondence',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'middlewares.auto_prolong_session.AutoProlongSession', # custom
)


SECRET_KEY = passwords.SECRET_KEY
SMS_GATE_LOGIN = passwords.SMS_GATE_LOGIN
SMS_GATE_PASSWORD = passwords.SMS_GATE_PASSWORD
MANDRILL_API_KEY = passwords.MANDRILL_API_KEY

SESSION_COOKIE_AGE = 60 * 60 * 24 * 365 * 2
SESSION_COOKIE_HTTPONLY = False

AUTH_USER_MODEL = 'users.Users'
AUTHENTICATION_BACKENDS = ('core.users.authentication_backends.SMSAuthenticationBackend', )



LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = False
USE_TZ = True


ALLOWED_HOSTS = (
    'm.w.ua1.binno.com.ua',
    'mappino.com', 'www.mappino.com',
    'mappino.com.ua', 'www.mappino.com.ua',
)
MAIN_DOMAIN_URL = 'http://mappino.com.ua'

# Визначає домен, що може бути використаний під час формування посилань.
# Використовується для всіх посилань будь-якої доменної зони,
# тому є зміст обрати для цього параметру міжнародний домен .com
REDIRECT_DOMAIN_URL = 'http://mappino.com'


STATIC_URL = 'http://mappino.com.ua/static/'
STATIC_ROOT = 'static/'
SERVE_STATIC_FILES = False

MEDIA_URL = 'http://mappino.com.ua/media/'
MEDIA_ROOT = 'media/'

COMPRESS_ENABLED = False
COMPRESS_STORAGE = 'compressor.storage.GzipCompressorFileStorage'
COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.SlimItFilter']


PROCESSES_PER_NODE_COUNT = 3


ROOT_URLCONF = 'mappino.urls'
WSGI_APPLICATION = 'mappino.wsgi.application'




BASE_DIR = os.path.dirname(os.path.dirname(__file__))





