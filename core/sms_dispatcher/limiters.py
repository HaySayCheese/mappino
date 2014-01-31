#coding=utf-8
import logging
import datetime
from core.sms_dispatcher.exceptions import SMSLimitException
from mappino.wsgi import redis_connections


class BaseCountSMSLimiter(object):
	def __init__(self, prefix, max_attempts_count, log_directive):
		if not prefix or not log_directive:
			raise ValueError('Invalid parameters')
		if max_attempts_count <= 0:
			raise ValueError('Invalid parameters')

		super(BaseCountSMSLimiter, self).__init__()

		self.logger = logging.getLogger('mappino.sms_dispatcher.limiter')
		self.redis = redis_connections['steady']
	
		self.prefix = prefix
		self.max_attempts_count = max_attempts_count
		self.log_directive = log_directive


	def check_transaction(self, number=None, request=None):
		return True


	def check_count(self, param):
		if not param:
			raise ValueError('invalid key')

		key = self.prefix + param
		if self.redis.exists(key):
			attempts_count = int(self.redis.get(key))
			if attempts_count >= self.max_attempts_count:
				self.logger.warn('{0} reached limit ({1})'.format(param, self.max_attempts_count))
				raise SMSLimitException('Count reached.')

			pipe = self.redis.pipeline()
			pipe.incr(key)
			pipe.expireat(key, self.__zero_timestamp())
			pipe.execute()

		else:
			pipe = self.redis.pipeline()
			pipe.set(key, 1)
			pipe.expireat(key, self.__zero_timestamp())
			pipe.execute()

		return True


	@staticmethod
	def __zero_timestamp():
		return datetime.datetime.now().replace(
			hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)



class PerDayCountSMSLimiter(BaseCountSMSLimiter):
	def check_transaction(self, number=None, request=None):
		if not number:
			raise ValueError('empty number')

		return self.check_count(number)



class PerIPCountSMSLimiter(BaseCountSMSLimiter):
	def check_transaction(self, number=None, request=None):
		if not request:
			raise ValueError('empty request')

		return self.check_count(self.__get_client_ip(request))


	@staticmethod
	def __get_client_ip(request):
		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
		if x_forwarded_for:
			ip = x_forwarded_for.split(',')[0]
		else:
			ip = request.META.get('REMOTE_ADDR')
		return ip



