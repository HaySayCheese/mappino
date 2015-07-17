#coding=utf-8
from collective.exceptions import InvalidArgument
from core import redis_connections


class AbstractCacheManager(object):
	def __init__(self, prefix='cache'):
		if not prefix:
			raise InvalidArgument('prefix is empty.')

		self.redis = redis_connections['cache']
		self.prefix = prefix


class CountersCacheManager(AbstractCacheManager):
	def __init__(self):
		super(CountersCacheManager, self).__init__('counters_cache')


	def __key(self, tid, hash_id):
		return '{0}:{1}'.format(tid, hash_id)


	def etag(self, tid, hash_id):
		etag = self.redis.hget(self.prefix, self.__key(tid, hash_id))
		if etag is None:
			etag = 0
			self.redis.hset(self.prefix, self.__key(tid, hash_id), etag)
		return etag


	def increment_etag(self, tid, hash_id):
		self.redis.incr(self.__key(tid, hash_id))