#coding=utf-8
import urllib
import datetime

from collective.exceptions import InvalidArgument, ResourceThrottled
from core.constants import GLOBAL_REDIS_PREFIXES
from mappino import settings
from mappino.wsgi import redis_connections


class BaseSMSSender(object):
	def process_query(self, number, message):
		# if settings.DEBUG:
		# 	return True

		if not message:
			raise InvalidArgument('Message can not be empty')
		if not number:
			raise InvalidArgument('Number can not be empty.')
		# todo: додати перевірку номеру на відповідність формату

		params = urllib.urlencode({
			'login': settings.SMS_GATE_LOGIN,
			'psw': settings.SMS_GATE_PASSWORD,
		    'phones': '+380'+str(number),
		    'mes': message,
		    'charset': 'utf-8'
		})

		# Відправляти повторно, якщо перша передача не пройшла.
		return self.__send_request(params) or self.__send_request(params)


	@staticmethod
	def __send_request(params):
		response = urllib.urlopen("http://smsc.ru/sys/send.php", params).read()
		return 'OK' in response


class RegistrationCheckCodesSender(BaseSMSSender):
	MAX_ATTEMPTS_PER_DAY = 12 # з одного ip

	def __init__(self):
		self.redis = redis_connections['throttle']
		self.redis_prefix = GLOBAL_REDIS_PREFIXES.registration_check_code_throttle()

	def throttle(self, request):
		key = self.redis_prefix + self.__get_client_ip(request)

		if self.redis.exists(key):
			attempts_count = int(self.redis.get(key))
			if attempts_count >= self.MAX_ATTEMPTS_PER_DAY:
				raise ResourceThrottled()

			pipe = self.redis.pipeline()
			pipe.incr(key)
			pipe.expireat(key, self.__zero_timestamp())
			pipe.execute()
		else:
			pipe = self.redis.pipeline()
			pipe.set(key, 1)
			pipe.expireat(key, self.__zero_timestamp())
			pipe.execute()


	def resend(self, number, code, request):
		self.throttle(request)
		return self.process_query(number, 'Ваш проверочный код mappino: {0}'.format(code))


	def send(self, number, code, request):
		self.throttle(request)
		return self.process_query(number, 'Добро пожаловать на mappino. Ваш код: {0}'.format(code))


	@staticmethod
	def __get_client_ip(request):
		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
		if x_forwarded_for:
			ip = x_forwarded_for.split(',')[0]
		else:
			ip = request.META.get('REMOTE_ADDR')
		return ip


	@staticmethod
	def __zero_timestamp():
		"""
		Повертає різницю між поточним часом і 00:00 наступного дня.
		"""
		return datetime.datetime.now().replace(
			hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)