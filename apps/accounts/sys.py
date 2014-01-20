#coding=utf-8
import hashlib
from collective.exceptions import AlreadyExist
from core.users.models import Users
from mappino.wsgi import redis_connections



class NoUserWithSuchUsername(Exception): pass
class TokenAlreadyExists(AlreadyExist): pass
class TokenDoesNotExists(Exception): pass

class AccessRestoreHandler(object):
	def __init__(self):
		self.redis = redis_connections[1]
		self.token_prefix = 'access_restore_handler_'
		self.token_ttl = 60*60*24 # 24 hours
		self.uid_field_prefix = 'uid'


	def begin_restoring(self, username):
		if not username:
			raise ValueError('@username can not be empty.')

		# try by email
		user = Users.by_email(username)
		if user is None:
			user = Users.by_phone_number(username)
			if user is None:
				raise NoUserWithSuchUsername('Login: {0}'.format(username))

		token = self.__add_token(user)
		return token


	def token_is_present(self, token=None, user_id=None):
		if token:
			return self.redis.exist(self.token_prefix + token)
		elif user_id:
			return self.redis.exist(self.token_prefix + self.__generate_token(user_id))
		raise ValueError('No one parameter is specified.')


	def finish_restoring(self, token, password):
		if not self.token_is_present(self.token_prefix + token):
			raise TokenDoesNotExists()
		if not password:
			raise ValueError("@password can't be empty.")

		user_id = self.redis.hget(self.token_prefix + token, self.uid_field_prefix)
		if user_id is None:
			# token was deleted moment ago
			raise TokenDoesNotExists()

		user = Users.objects.filter(id = user_id).only('id')
		user.set_password(password)
		user.save()
		self.__remove_token(token)


	def __add_token(self, user_id):
		token = self.__generate_token(user_id)
		if self.token_is_present(token):
			raise TokenAlreadyExists('uid: {0}'.format(user_id))

		pipe = self.redis.pipeline()
		pipe.hset(self.token_prefix + token, self.uid_field_prefix, user_id)
		pipe.expire(self.token_prefix + token, self.token_ttl)
		pipe.execute()
		return token


	def __remove_token(self, record_id):
		if not self.token_is_present(self.token_prefix + record_id):
			raise TokenDoesNotExists()
		self.redis.delete(self.token_prefix + record_id)


	@staticmethod
	def __generate_token(user_id):
		h = hashlib.sha512()
		h.update('LdKBhKjmm1dei9mj71eT') # salt
		h.update(user_id)
		return h.hexdigest()



# fixme: please
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