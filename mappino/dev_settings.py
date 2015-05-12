# coding=utf-8
import os
#from psycopg2cffi import compat
from mappino import passwords



# cffi hook (needed by pypy)
#compat.register()


DEBUG = True
SMS_DEBUG = DEBUG
TEMPLATE_DEBUG = DEBUG


ADMINS = (
    ('Dima Chizhevsky', 'dima@mappino.com'),
)
MANAGERS = (
    ('Dima Chizhevsky', 'support@mappino.com'),
)
SUPPORT_EMAIL =  MANAGERS[0][1]
BILLING_MANAGER_EMAIL = MANAGERS[0][1]
MODERATORS = MANAGERS[0][1]


HUL1_PUBLIC_IP = '128.199.59.244'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '(dev)mappino-db',
        'USER': '(dev)mappino',
        'PASSWORD': '123123',
        'HOST': '127.0.0.1',
        'PORT': 5555,
    },
    'markers_index': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '(dev)mappino-index-db',
        'USER': '(dev)mappino',
        'PASSWORD': '123123',
        'HOST': '127.0.0.1',
        'PORT': 5555,
    }
}
DATABASE_ROUTERS = ['core.database_router.Router', ]


REDIS_DATABASES = {
    'throttle': {
        'HOST': HUL1_PUBLIC_IP,
        'PORT': 6380, # the real port is 6379, 6380 is set for dev
    },
    'steady': {
        'HOST': HUL1_PUBLIC_IP,
        'PORT': 6380,
    },
    'cache': {
        'HOST': HUL1_PUBLIC_IP,
        'PORT': 6380,
    },
    'celery': {
        'HOST': HUL1_PUBLIC_IP,
        'PORT': 6380,
    },
}


SPHINX_SEARCH_DATABASE = {
    'HOST': HUL1_PUBLIC_IP,
    'PORT': 9307 # the real port is 9306. 9307 is set for dev suite.
}
ENABLE_SPHINX_SEARCH = False
#

CACHES = {
    'default': {
        # Даний кеш використовується django-compressor для зберігання імен зжатих файлів.
        # Явної настройки для цього кешу указувати не треба.

        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '{0}:{1}'.format(REDIS_DATABASES['cache']['HOST'], REDIS_DATABASES['cache']['PORT']),
        'OPTIONS': {
            'DB': 1,
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
    # 'south',
    # 'compressor',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',



    'core',
    'core.billing',
    'core.users',


    'core.ban',
    'core.customers',
    'core.favorites',

    'core.publications',
    'core.claims',
    'core.markers_handler',
    'core.search',
    'core.support',
    'core.escaped_fragments_manager',

    # todo: shift this apps into core

    'apps.cabinet.api.dirtags',
    'apps.main.api.correspondence',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    # todo: enable csrf middleware
    # 'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'middlewares.auto_prolong_session.AutoProlongSession',  # custom
)


# secret key does not taken from the passwords file
# to be different from production one.
SECRET_KEY = '*m9ye0^!5otq35^(rb1^5mau92$6xen5!y69c$9e20yr0etexi'
SMS_GATE_LOGIN = passwords.SMS_GATE_LOGIN
SMS_GATE_PASSWORD = passwords.SMS_GATE_PASSWORD
MANDRILL_API_KEY = passwords.MANDRILL_API_KEY
LIQPAY_PUBLIC_KEY = passwords.LIQPAY_PUBLIC_KEY
LIQPAY_PRIVATE_KEY = passwords.LIQPAY_PRIVATE_KEY


SESSION_COOKIE_AGE = 60*60*24*14 # 14 days
SESSION_COOKIE_HTTPONLY = False # session cookie is used by the frontend js


LANGUAGE_CODE = 'en-us' # todo: change correct lang code
TIME_ZONE = 'UTC' # todo: change correct time zone
USE_I18N = False
USE_L10N = False
USE_TZ = True


ALLOWED_HOSTS = ['127.0.0.1']
DOMAIN_URL = 'http://mappino.com.ua'

# Визначає домен, який точно може забезпечити роботу всіх посилань.
# Як правило, це який-небудь міжнародний домен типу .com.
# Застосовується, між іншим, у формуванні посилань в шаблонах емейл-повідомлень.
REDIRECT_DOMAIN_URL = 'http://127.0.0.1:8000'


STATIC_URL = 'http://localhost/mappino_static/'
STATIC_ROOT = 'static/'
SERVE_STATIC_FILES = False

MEDIA_URL = 'http://localhost/mappino_media/'
MEDIA_ROOT = 'media/'

COMPRESS_ENABLED = False
COMPRESS_STORAGE = 'comprsessor.storage.GzipCompressorFileStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'compressor.finders.CompressorFinder',
)



PROCESSES_PER_NODE_COUNT = 3


ROOT_URLCONF = 'mappino.urls'
WSGI_APPLICATION = 'mappino.wsgi.application'


AUTH_USER_MODEL = 'users.Users'
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

























