"""
WSGI config for mappino project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import os
import redis

from django.conf import settings
from django.core.wsgi import get_wsgi_application



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mappino.settings")
application = get_wsgi_application()


# redis databases initialisation
redis_connections = {}
for name, params in settings.REDIS_DATABASES.iteritems():
	redis_connections[name] = redis.StrictRedis(params['HOST'], params['PORT'], 0)
