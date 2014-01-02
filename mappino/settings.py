"""
For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

DEBUG = True
if not DEBUG:
	import production_settings
else:
	# pypy psycopg2cffi compatible hook
	from psycopg2cffi import compat
	compat.register()

	# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
	import os
	BASE_DIR = os.path.dirname(os.path.dirname(__file__))

	SECRET_KEY = '*m9ye0^!5otq35^(rb1^5mau92$6xen5!y69c$9e20yr0etexi'
	TEMPLATE_DEBUG = True
	ALLOWED_HOSTS = []


	DATABASES = {
		'default': {
			'ENGINE':'django.db.backends.postgresql_psycopg2',
			'NAME': '(dev)mappino',
			'USER': 'mappino',
			'PASSWORD': '123123',
			'HOST': 'dev-server.binno.com.ua',
		}
	}
	INSTALLED_APPS = (
		'django.contrib.admin',
		'django.contrib.auth',
		'django.contrib.contenttypes',
		'django.contrib.sessions',
		'django.contrib.messages',
		'django.contrib.staticfiles',
	)
	MIDDLEWARE_CLASSES = (
		'django.contrib.sessions.middleware.SessionMiddleware',
		'django.middleware.common.CommonMiddleware',
		'django.middleware.csrf.CsrfViewMiddleware',
		'django.contrib.auth.middleware.AuthenticationMiddleware',
		'django.contrib.messages.middleware.MessageMiddleware',
		'django.middleware.clickjacking.XFrameOptionsMiddleware',
	)

	ROOT_URLCONF = 'mappino.urls'
	WSGI_APPLICATION = 'mappino.wsgi.application'


	# Internationalization
	# https://docs.djangoproject.com/en/1.6/topics/i18n/
	LANGUAGE_CODE = 'en-us'

	TIME_ZONE = 'UTC'

	USE_I18N = False
	USE_L10N = False
	USE_TZ = True


	# Static files (CSS, JavaScript, Images)
	# https://docs.djangoproject.com/en/1.6/howto/static-files/
	STATIC_URL = '/static/'
