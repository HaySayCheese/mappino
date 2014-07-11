"""
WSGI config for mappino project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

from django.core.wsgi import get_wsgi_application
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader
import os
import redis

from core.utils import static_hasher
from mappino import settings


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mappino.settings")
application = get_wsgi_application()

# jinja2 configs
templates = Environment(
    loader=FileSystemLoader(os.path.join(settings.BASE_DIR, 'templates')),
    trim_blocks=True,
    lstrip_blocks=True,
)

static_hasher.init()
templates.globals.update({
	'static': settings.STATIC_URL,
    'hash_static': static_hasher.hash_static,
})


# redis databases initialisation
redis_connections = {}
for name, params in settings.REDIS_DATABASES.iteritems():
	redis_connections[name] = redis.StrictRedis(params['HOST'], params['PORT'], 0)
