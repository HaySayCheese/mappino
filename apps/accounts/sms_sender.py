#coding=utf-8
from mappino.wsgi import redis_connections


class SMSSender(object):
	REDIS_PREFIX = 'send_sms_throttle'

	# todo: imply checks
	MAX_COUNT_PER_USER = 3
	MAX_COUNT_PER_IP = 10
	MAX_COUNT_PER_DAY = 200

	def __init__(self):
		self.redis = redis_connections[1]

	def send(self, number, request):
		# todo: send sms here
		# todo: додати перевірку на дотримання часового інтервалу до повторної SMS
		# todo: додати обмеження на к-сть SMS в день
		# todo: додати обмеження на к-сть SMS на одну ip-адресу.
		pass



