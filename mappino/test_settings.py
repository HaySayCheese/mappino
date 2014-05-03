#coding=utf-8
"""
For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from mappino import passwords


#   МЕГА ПАТЧ
#	pypy psycopg2cffi compatible hook
from psycopg2cffi import compat
compat.register()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ESTIMATE_THREADS_COUNT = 4

# Визначає домен, який точно може забезпечити роботу всіх посилань.
# Як правило, це який-небудь міжнародний домен типу .com.
# Застосовується, між іншим, у формуванні посилань в шаблонах емейл-повідомлень.
REDIRECT_DOMAIN = 'http://127.0.0.1:8000' # todo: зміни мене повністю!


SECRET_KEY = '*m9ye0^!5otq35^(rb1^5mau92$6xen5!y69c$9e20yr0etexi'
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1']

SMS_GATE_LOGIN = passwords.SMS_GATE_LOGIN
SMS_GATE_PASSWORD = passwords.SMS_GATE_PASSWORD
MANDRILL_API_KEY = passwords.MANDRILL_API_KEY


DATABASES = {
	'default': {
		'ENGINE':'django.db.backends.sqlite3',
		'NAME': 'memory:(dev)mappino',
	}
}
REDIS_DATABASES = {
	'throttle': {
		'HOST': '185.14.186.102',
	    'PORT': 6379,
	},
    'steady': {
	    'HOST': '185.14.186.102',
	    'PORT': 6379,
    },
    'celery': {
	    'HOST': '185.14.186.102',
	    'PORT': 6379,
    },
    'cache': {
	    'HOST': '185.14.186.102',
	    'PORT': 6379,
    },
    'sessions': {
	    'HOST': '185.14.186.102',
	    'PORT': 6379,
    }
}
SPHINX_SEARCH = {
	'HOST': '185.14.186.102',
    'PORT': 9306
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

MEDIA_URL = 'http://localhost/mappino_media/'
MEDIA_ROOT = '/media/work/web-projects/mappino/media/'

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
