#coding=utf-8
import redis
from django.conf import settings

from signals import initialize_all_signals


initialize_all_signals()

# redis databases initialisation
redis_connections = {}
for name, params in settings.REDIS_DATABASES.iteritems():
	redis_connections[name] = redis.StrictRedis(params['HOST'], params['PORT'], 0)


