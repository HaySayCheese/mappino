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
    ('Dima Chizhevsky', 'dima@mappino.com', ),
)
MANAGERS = (
    ('Dima Chizhevsky', 'dima@mappino.com', ),
)
SUPPORT_EMAIL = MANAGERS[0][1]
BILLING_MANAGER_EMAIL = MANAGERS[0][1]
MODERATORS = MANAGERS[0]


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


EVE1_INTERNAL_IP = '10.133.24.200'
HUL1_INTERNAL_IP = EVE1_INTERNAL_IP


INDEXES_DATABASE_NAME = 'default'
DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME': 'mappino',
        'USER': 'mappino-user',
        'PASSWORD': passwords.DB_PASSWORD,
        'HOST': EVE1_INTERNAL_IP,
        'PORT': 6432, # pg_bounce is used
    },
}


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
    },
    'templates_etags': {
        # on several nodes templates may differ,
        # local memory is used instead of redis to avoid etags duplications on several machines.
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'templates_etags',
    },
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
    'compressor',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',

    'core.cache',
    'core.currencies',

    'core.publications.PublicationsApp',

    'core.users.UsersApp',
    'core.users.favorites.FavoritesApp',
    'core.users.notifications.NotificationsApp',
    'core.users.notifications.sms_dispatcher.SMSDispatcherApp',

    'core.support.SupportApp',

    'core.managing.ban.BanApp',
    'core.managing.managers.ManagersApp',
    'core.managing.moderators.ModeratorsApp',

    'core.markers_index.MarkersIndexApp',
    # 'core.escaped_fragments_manager',

    'core',
)


MIDDLEWARE_CLASSES = (
    # This middleware processes responses(!) and sets special cookie in some cases.
    # It is linked with authentication middleware and checks "request.user" object.
    # Django processes middlewares in reverse order, so this one must be before
    # django.authentication, otherwise request will not have "user" object.
    'middlewares.user_settings.UserCookie',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    # todo: enable csrf middleware
    # 'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'middlewares.auto_prolong_session.AutoProlongSession',
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
    'mappino.com', 'www.mappino.com',
    'mappino.com.ua', 'www.mappino.com.ua',
)
MAIN_DOMAIN_URL = 'http://mappino.com.ua'

# Визначає домен, що може бути використаний під час формування посилань.
# Використовується для всіх посилань будь-якої доменної зони,
# тому є зміст обрати для цього параметру міжнародний домен .com
REDIRECT_DOMAIN_URL = 'http://mappino.com'


STATIC_URL = '/static/'
STATIC_ROOT = 'static/'
SERVE_STATIC_FILES = False

MEDIA_URL = '/media/'
MEDIA_ROOT = 'media/'


COMPRESS_ENABLED = True
COMPRESS_STORAGE = 'compressor.storage.GzipCompressorFileStorage'
STATICFILES_FINDERS = (
    'compressor.finders.CompressorFinder',
)


ROOT_URLCONF = 'mappino.urls'
WSGI_APPLICATION = 'mappino.wsgi.application'


BASE_DIR = os.path.dirname(os.path.dirname(__file__))





