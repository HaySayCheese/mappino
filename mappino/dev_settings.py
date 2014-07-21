#coding=utf-8

import os
from psycopg2cffi import compat

from mappino import passwords

# from mappino.wsgi import env


compat.register() # cffi hook
# import compressor.contrib.jinja2ext

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True
SMS_DEBUG = DEBUG
TEMPLATE_DEBUG = DEBUG
ENABLE_SPHINX_SEARCH = not DEBUG


ALLOWED_HOSTS = ['127.0.0.1']


SECRET_KEY = '*m9ye0^!5otq35^(rb1^5mau92$6xen5!y69c$9e20yr0etexi'
SMS_GATE_LOGIN = passwords.SMS_GATE_LOGIN
SMS_GATE_PASSWORD = passwords.SMS_GATE_PASSWORD
MANDRILL_API_KEY = passwords.MANDRILL_API_KEY


ESTIMATE_THREADS_COUNT = 4

# Визначає домен, який точно може забезпечити роботу всіх посилань.
# Як правило, це який-небудь міжнародний домен типу .com.
# Застосовується, між іншим, у формуванні посилань в шаблонах емейл-повідомлень.
REDIRECT_DOMAIN = 'http://127.0.0.1:8000'


DATABASES = {
	'default': {
		'ENGINE':'django.db.backends.postgresql_psycopg2',
		'NAME': '(dev)mappino',
		'USER': 'mappino',
		'PASSWORD': '123123',
		'HOST': '146.185.129.95',
	}
}
REDIS_DATABASES = {
	'throttle': {
		'HOST': '95.85.40.162',
	    'PORT': 6381,
	},
    'steady': {
	    'HOST': '95.85.40.162',
	    'PORT': 6381,
    },
    'celery': {
	    'HOST': '95.85.40.162',
	    'PORT': 6381,
    },
    'cache': {
	    'HOST': '95.85.40.162',
	    'PORT': 6381,
    },
    'sessions': {
	    'HOST': '95.85.40.162',
	    'PORT': 6381,
    }
}
SPHINX_SEARCH = {
	'HOST': '95.85.40.162',
    'PORT': 9306
}
CACHES = {
	'default': {
		# Даний кеш використовується django-compressor для зберігання імен зжатих файлів.
		# Явної настройки для цього указувати не треба.

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

SESSION_COOKIE_AGE = 1209600
# SESSION_SAVE_EVERY_REQUEST = True

# celery config
CELERY_REDIS_HOST = REDIS_DATABASES['celery']['HOST']
CELERY_REDIS_PORT = REDIS_DATABASES['celery']['PORT']

BROKER_URL = 'redis://' + str(CELERY_REDIS_HOST) + ':' + str(CELERY_REDIS_PORT) + '/0'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 60*60*4}
CELERY_RESULT_BACKEND = BROKER_URL

# SESSION_ENGINE = 'redis_sessions.session'
# SESSION_REDIS_HOST = REDIS_DATABASES['sessions']['HOST']
# SESSION_REDIS_PORT = REDIS_DATABASES['sessions']['PORT']
# SESSION_REDIS_DB = 0
# SESSION_REDIS_PREFIX = 'ses'

SUPPORT_EMAIL = 'Dima.Chizhevsky@gmail.com'

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
	# 'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'middlewares.auto_prolong_session.AutoProlongSession', # custom
)


ROOT_URLCONF = 'mappino.urls'
WSGI_APPLICATION = 'mappino.wsgi.application'

AUTH_USER_MODEL = 'users.Users'
SESSION_COOKIE_HTTPONLY = False

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False
USE_L10N = False
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = 'http://localhost/mappino_static/'
STATIC_ROOT = 'static/'

MEDIA_URL = 'http://localhost/mappino_media/'
MEDIA_ROOT = 'media/'

COMPRESS_ENABLED = False
COMPRESS_STORAGE = 'comprsessor.storage.GzipCompressorFileStorage'



STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'compressor.finders.CompressorFinder',
)

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
