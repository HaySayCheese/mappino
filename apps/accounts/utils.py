#coding=utf-8
import hashlib
import random
import string
from __builtin__ import unicode

from django.db import transaction

from collective.exceptions import AlreadyExist, RecordAlreadyExists
from collective.http.cookies import set_signed_cookie
from core.sms_dispatcher import check_codes_sms_sender
from core.users.models import Users
from mappino.wsgi import redis_connections


class NoUserWithSuchUsername(Exception): pass
class TokenDoesNotExists(Exception): pass
class TokenAlreadyExists(AlreadyExist):
	def __init__(self, message, token):
		Exception.__init__(self, message)
		self.token = token

class AccessRestoreHandler(object):
	def __init__(self):
		self.redis = redis_connections['steady']
		self.token_prefix = 'access_restore_handler_'
		self.token_ttl = 60*60*24 # 24 hours
		self.uid_field_name = 'uid'


	def begin_restoring(self, username):
		if not username:
			raise ValueError('@username can not be empty.')

		# try by email
		user = Users.by_email(username)
		if user is None:
			user = Users.by_phone_number(username)
			if user is None:
				raise NoUserWithSuchUsername('Login: {0}'.format(username))

		# todo: додати тротлінг
		# Повторне повідомлення надсилається навіть тоді, коли token вже пристуній.
		try:
			token = self.__add_token(user.id)
		except TokenAlreadyExists as e:
			token = e.token

		# todo: реалізуй мене
		#send_mail(
		#	subject = 'mappino: восстановление пароля',
		#    message = templates.get_templat('email/access_restore/index.html').render({
		#	    'domain': settings.DOMAIN,
		#	    'token': token,
		#    }),
		#	from_email = settings.ROBOT_MAIL_ACCOUNT,
		#    recipient_list=[user.email]
		#)


	def token_is_present(self, token=None, user_id=None):
		if token:
			return self.redis.exists(self.token_prefix + token)
		elif user_id:
			return self.redis.exists(self.token_prefix + self.__generate_token(user_id))
		raise ValueError('No one parameter is specified.')


	def finish_restoring(self, token, password):
		if not self.token_is_present(token):
			raise TokenDoesNotExists()
		if not password:
			raise ValueError("@password can't be empty.")

		user_id = self.redis.hget(self.token_prefix + token, self.uid_field_name)
		if user_id is None:
			# token was deleted moment ago
			raise TokenDoesNotExists()

		self.__remove_token(token)
		user = Users.objects.filter(id = user_id).only('id')[0]
		user.set_password(password)
		user.save()
		return user



	def __add_token(self, user_id):
		token = self.__generate_token(user_id)
		if self.token_is_present(token):
			raise TokenAlreadyExists('uid: {0}'.format(user_id), token)

		pipe = self.redis.pipeline()
		pipe.hset(self.token_prefix + token, self.uid_field_name, user_id)
		pipe.expire(self.token_prefix + token, self.token_ttl)
		pipe.execute()
		return token


	def __remove_token(self, record_id):
		if not self.token_is_present(record_id):
			raise TokenDoesNotExists()
		self.redis.delete(self.token_prefix + record_id)


	@staticmethod
	def __generate_token(user_id):
		h = hashlib.sha512()
		h.update('LdKBhKjmm1dei9mj71eT') # salt
		h.update(unicode(user_id))
		return h.hexdigest()



class PhoneAlreadyInQueue(RecordAlreadyExists): pass
class InvalidCheckCode(ValueError): pass

class MobilePhonesChecker(object):
	def __init__(self):
		self.redis = redis_connections['steady']
		self.record_prefix = 'mob_check_'
		self.code_field_name = 'code'
		self.attempts_field_name = 'attempts'
		self.name_field_name =  'name'
		self.surname_field_name = 'surname'
		self.email_field_name = 'email'
		self.phone_number_field_name = 'number'
		self.password_field = 'pass'

		self.max_attempts_count = 3
		self.record_ttl = 60*60*2 # 2 hours

		self.cookie_name = 'mcheck'
		self.cookie_salt = 'JMH2FWWYa1ogCJR0gW4z'


	def number_check_is_started(self, request):
		return self.cookie_name in request.COOKIES


	def begin_number_check(self, name, surname, email, phone, user_password, request, response):
		if not phone:
			raise ValueError('Empty or absent @phone')
		if not user_password:
			raise ValueError('Empty or absent @user_password')


		uid = self.__generate_record_id(phone)
		key = self.record_prefix + uid
		code = self.__generate_check_code()

		pipe = self.redis.pipeline()
		pipe.hset(key, self.code_field_name, code)
		pipe.hset(key, self.attempts_field_name, 0)
		pipe.hset(key, self.name_field_name, name)
		pipe.hset(key, self.surname_field_name, surname)
		pipe.hset(key, self.email_field_name, email)
		pipe.hset(key, self.phone_number_field_name, phone)
		pipe.hset(key, self.password_field, user_password)
		pipe.expire(key, self.record_ttl)
		pipe.execute()

		set_signed_cookie(response, self.cookie_name, uid, salt=self.cookie_salt,
		                  days_expire=1, http_only=False)

		# hint: send throttling implemented in SMSSender
		# no need to do it here
		check_codes_sms_sender.send(phone, code, request)


	def cancel_number_check(self, request, response):
		key = self.record_prefix + request.get_signed_cookie(self.cookie_name, salt=self.cookie_salt)
		if not self.redis.exists(key):
			raise InvalidCheckCode()

		self.redis.delete(key)
		response.delete_cookie(self.cookie_name)


	def check_code(self, code, request, response):
		if not code:
			raise ValueError('@code is empty or None')

		key = self.record_prefix + request.get_signed_cookie(self.cookie_name, salt=self.cookie_salt)
		if not self.redis.exists(key):
			response.delete_cookie(self.cookie_name)
			raise Exception(
				'RUNTIME WARNING: key {0} is not in redis database but present in users cookie.'.format(key))

		attempts_count = self.redis.hget(key, self.attempts_field_name)
		if attempts_count is None:
			# key was deleted moment ago
			response.delete_cookie(self.cookie_name)
			return False, {'attempts': self.max_attempts_count}

		attempts_count = int(attempts_count)
		if attempts_count >= self.max_attempts_count - 1:
			self.redis.delete(key)
			response.delete_cookie(self.cookie_name)
			return False, {'attempts': self.max_attempts_count}

		true_code = self.redis.hget(key, self.code_field_name)
		if true_code is None:
			# key was deleted moment ago
			response.delete_cookie(self.cookie_name)
			return False, {'attempts': self.max_attempts_count}

		if code != true_code:
			self.redis.hincrby(key, self.attempts_field_name, 1)
			return False, {'attempts': attempts_count + 1}

		name = self.redis.hget(key, self.name_field_name)
		surname = self.redis.hget(key, self.surname_field_name)
		email = self.redis.hget(key, self.email_field_name)
		phone = self.redis.hget(key, self.phone_number_field_name)
		password = self.redis.hget(key, self.password_field)
		self.redis.delete(key)

		if (not name) or (not surname) or (not phone) or (not password):
			# key was deleted moment ago
			response.delete_cookie(self.cookie_name)
			return False, {'attempts': self.max_attempts_count}

		# account creation
		with transaction.atomic():
			user = Users.objects.create_user(email, phone, password)
			user.name = name
			user.surname = surname
			user.is_active = True
			user.save()

		user_data = {
			'phone': phone,
		    'password': password,
		}
		response.delete_cookie(self.cookie_name)
		return True, user_data


	def resend_sms(self, request, response):
		uid = request.get_signed_cookie(self.cookie_name, salt=self.cookie_salt)
		key = self.record_prefix + uid
		if not self.redis.exists(key):
			response.delete_cookie(self.cookie_name)
			raise InvalidCheckCode()

		code = self.__generate_check_code()

		pipe = self.redis.pipeline()
		pipe.hset(key, self.code_field_name, code)
		pipe.hset(key, self.attempts_field_name, 0)
		pipe.expire(key, self.record_ttl)
		pipe.execute()

		set_signed_cookie(response, self.cookie_name, uid, salt=self.cookie_salt,
		                  days_expire=1, http_only=False)

		# hint: send throttling implemented in SMSSender
		# no need to do it here
		phone = self.redis.hget(key, self.phone_number_field_name)
		check_codes_sms_sender.resend(phone, code, request)


	@staticmethod
	def __generate_record_id(phone):
		h = hashlib.sha1()
		h.update(phone)
		h.update('E66bLuTGzEkDqQHmrSNU') # salt
		return h.hexdigest()

	@staticmethod
	def __generate_check_code():
		return ''.join(random.choice(string.digits) for x in range(6))