from collective.constants import AbstractConstant


class RedisPrefixes(AbstractConstant):
	def __init__(self):
		super(RedisPrefixes, self).__init__()
		self.set_ids({
			# sms dispatcher
			'registration_check_code_throttle': 'c-code-thr'
		})

	def registration_check_code_throttle(self):
		return self.ids['registration_check_code_throttle']

GLOBAL_REDIS_PREFIXES = RedisPrefixes()