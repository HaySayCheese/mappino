import redis
from django.conf import settings

redis_connections = {}

def intialize_redis_connections():
    # redis databases initialisation
    for name, params in settings.REDIS_DATABASES.iteritems():
        redis_connections[name] = redis.StrictRedis(params['HOST'], params['PORT'], 0)


