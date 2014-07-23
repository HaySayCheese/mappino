#coding=utf-8
import os
from mappino import passwords
from psycopg2cffi import compat


DEBUG = False
TEMPLATE_DEBUG = DEBUG
SMS_DEBUG = DEBUG


# pypy psycopg2cffi compatible hook
compat.register()


SECRET_KEY = passwords.SECRET_KEY
SMS_GATE_LOGIN = passwords.SMS_GATE_LOGIN
SMS_GATE_PASSWORD = passwords.SMS_GATE_PASSWORD
MANDRILL_API_KEY = passwords.MANDRILL_API_KEY


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ESTIMATE_THREADS_COUNT = 2


ALLOWED_HOSTS = ['mappino.com', 'mappino.com.ua']

# Визначає домен, що може бути використаний під час формування посилань.
# Використовується для всіх посилань будь-якої доменної зони,
# тому є зміст обрати для цього параметру міжнародний домен .com
REDIRECT_DOMAIN = 'http://mappino.com'

# Визначає ел. адресу, на яку приходять всі листи в сапорт.
# На даний момент адреса одна і балансування немає
SUPPORT_EMAIL = 'support@mappino.com'


EVE_M1_INTERNAL_IP = '10.129.177.252'
HUL_M1_INTERNAL_IP = '10.129.178.15'
DATABASES = {
	'default': {
		'ENGINE':'django.db.backends.postgresql_psycopg2',
		'NAME': 'mappino-db',
		'USER': 'mappino',
		'PASSWORD': passwords.DB_PASSWORD,
		'HOST': EVE_M1_INTERNAL_IP,
	    'PORT': 6432,
	}
}
REDIS_DATABASES = {
	'throttle': {
		'HOST': HUL_M1_INTERNAL_IP,
	    'PORT': 6379,
	},
    'steady': {
	    'HOST': HUL_M1_INTERNAL_IP,
	    'PORT': 6379,
    },
    'celery': {
	    'HOST': HUL_M1_INTERNAL_IP,
	    'PORT': 6379,
    },
    'sessions': {
	    'HOST': HUL_M1_INTERNAL_IP,
	    'PORT': 6379,
    },
    'cache': {
	    'HOST': HUL_M1_INTERNAL_IP,
	    'PORT': 6380, # NOTE: redis-cache is on the different port
    },
}
SPHINX_SEARCH = {
	'HOST': HUL_M1_INTERNAL_IP,
    'PORT': 9306
}
CACHES = {
	'default': {
		# Даний кеш нуявно використовується django-compressor для зберігання імен опрацьованих файлів.

		'BACKEND': 'redis_cache.RedisCache',
	    'LOCATION': '{0}:{1}'.format(
		    REDIS_DATABASES['cache']['HOST'],
		    REDIS_DATABASES['cache']['PORT']
	    ),
	    'OPTIONS': {
		    'DB': 0,
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
	'visibility_timeout': 60*60*4
}
CELERY_RESULT_BACKEND = BROKER_URL


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
SESSION_COOKIE_AGE = 1209600


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
