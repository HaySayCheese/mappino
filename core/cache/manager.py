#coding=utf-8
from collective.exceptions import InvalidArgument
from core import redis_connections


class AbstractCacheManager(object):
	def __init__(self, prefix='cache'):
		if not prefix:
			raise InvalidArgument('prefix is empty.')

		self.redis = redis_connections['cache']
		self.prefix = prefix