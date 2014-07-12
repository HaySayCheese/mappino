#coding=utf-8

import os
from mappino import passwords
from psycopg2cffi import compat


# https://docs.djangoproject.com/en/1.6/topics/settings/


DEBUG = True # todo: change me
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['mappino.com', 'mappino.com.ua']

SECRET_KEY = 'CpOFHrZ9x696TkKFIfj5-paHVO24I60nDJ9YsFkpO'
SMS_GATE_LOGIN = passwords.SMS_GATE_LOGIN
SMS_GATE_PASSWORD = passwords.SMS_GATE_PASSWORD
MANDRILL_API_KEY = passwords.MANDRILL_API_KEY

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# pypy psycopg2cffi compatible hook
compat.register()

# Визначає домен, який точно може забезпечити роботу всіх посилань.
# Як правило, це який-небудь міжнародний домен типу .com.
# Застосовується, між іншим, у формуванні посилань в шаблонах емейл-повідомлень.
REDIRECT_DOMAIN = 'http://mappino.com'


EVE_M1_IP = '10.129.177.252' # internal
HUL_M1_IP = '10.129.178.15' # internal


ESTIMATE_THREADS_COUNT = 2
DATABASES = {
	'default': {
		'ENGINE':'django.db.backends.postgresql_psycopg2',
		'NAME': 'mappino-db',
		'USER': 'mappino',
		'PASSWORD': passwords.DB_PASSWORD,
		'HOST': EVE_M1_IP,
	    'PORT': 6432,
	}
}



REDIS_DATABASES = {
	'throttle': {
		'HOST': HUL_M1_IP,
	    'PORT': 6379,
	},
    'steady': {
	    'HOST': HUL_M1_IP,
	    'PORT': 6379,
    },
    'celery': {
	    'HOST': HUL_M1_IP,
	    'PORT': 6379,
    },
    'sessions': {
	    'HOST': HUL_M1_IP,
	    'PORT': 6379,
    },
    'cache': {
	    'HOST': HUL_M1_IP,
	    'PORT': 6380, # redis-cache
    },
}
SPHINX_SEARCH = {
	'HOST': HUL_M1_IP,
    'PORT': 9306
}

SESSION_COOKIE_AGE = 1209600

# celery config
CELERY_REDIS_HOST = REDIS_DATABASES['celery']['HOST']
CELERY_REDIS_PORT = REDIS_DATABASES['celery']['PORT']
BROKER_URL = 'redis://' + str(CELERY_REDIS_HOST) + ':' + str(CELERY_REDIS_PORT) + '/0'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 60*60*4}
CELERY_RESULT_BACKEND = BROKER_URL


SUPPORT_EMAIL = 'Dima.Chizhevsky@gmail.com' # todo: change me


INSTALLED_APPS = (
	'compressor',

	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',

	'core.users',
	'core.publications',
	'core.markers_servers',
	'core.search',
	'core.support',

	'apps.cabinet.api.dirtags',
	'apps.main.api.correspondence',
)
MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	# 'django.middleware.csrf.CsrfViewMiddleware', # todo: enable csrf
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'middlewares.auto_prolong_session.AutoProlongSession', # custom
)

ROOT_URLCONF = 'mappino.urls'
WSGI_APPLICATION = 'mappino.wsgi.application'

AUTH_USER_MODEL = 'users.Users'
SESSION_COOKIE_HTTPONLY = False


USE_I18N = False
USE_L10N = False

TIME_ZONE = 'UTC'
USE_TZ = True



STATIC_URL = 'http://mappino.com.ua/static/'
STATIC_ROOT = 'static/'

MEDIA_URL = 'http://mappino.com.ua/media/'
MEDIA_ROOT = 'media/'

COMPRESS_ENABLED = True
COMPRESS_STORAGE = 'compressor.storage.GzipCompressorFileStorage'


# todo: check me
LOGGING = {
	'version': 1,
	'disable_existing_loggers': True,
	'formatters': {
		'simple': {
			'format': '%(levelname)s: %(asctime)s - %(message)s',
		    'datefmt': '%Y-%m-%d %H:%M:%S'
			},
		},
	'handlers': {
		'mail_admins': {
			'level': 'WARNING',
			'class': 'django.utils.log.AdminEmailHandler',
		},
	    'sms_dispatcher_limits_file': {
			'level': 'INFO',
	        'class': 'logging.handlers.TimedRotatingFileHandler',
	        'filename': 'logs/sms_dispatcher/limits.log',
	        'when': 'W6',
	        'backupCount': 24,
	        'formatter': 'simple'
	    },
	    'sms_dispatcher_sender_file': {
			'level': 'INFO',
	        'class': 'logging.handlers.TimedRotatingFileHandler',
	        'filename': 'logs/sms_dispatcher/sended.log',
	        'when': 'D',
	        'backupCount': 60,
	        'formatter': 'simple'
	    },
	},
	'loggers': {
		'mappino.sms_dispatcher.limits': {
			'handlers': ['sms_dispatcher_limits_file', 'mail_admins'],
			'level': 'INFO',
		    'propagate': False,
		},
	    'mappino.sms_dispatcher.sender': {
			'handlers': ['sms_dispatcher_sender_file', 'mail_admins'],
			'level': 'INFO',
		    'propagate': False,
		},
	}
}
