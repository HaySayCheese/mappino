#coding=utf-8
import copy
import hashlib
import json
import random
import string

from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from django.http.response import HttpResponseBadRequest, HttpResponse
from django.views.generic import View
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException

from collective.exceptions import EmptyArgument
from collective.http.cookies import set_signed_cookie
from collective.methods.request_data_getters import angular_post_parameters
from core.publications.constants import HEAD_MODELS, OBJECTS_TYPES
from core.sms_dispatcher import check_codes_sms_sender
from core.users import tasks
from core.users.models import Users
from mappino.wsgi import redis_connections


class MobilePhoneChecker(object):
	redis = redis_connections['steady']
	transaction_ttl = 60 * 60 * 2 # check code ttl in seconds.
	max_attempts_count = 3
	max_sms_per_transaction = 2

	record_prefix = 'mob_check_'
	id_field = 'id'
	code_field = 'code'
	attempts_field = 'attempts'
	sms_count_field = 'sms_count'
	phone_number_field = 'phone'

	cookie_name = 'mcheck'
	cookie_salt = 'JMH2FWWYa1ogCJR0gW4z'


	@classmethod
	def begin_check(cls, account_id, mobile_phone, request, response):
		"""
		Запукає механізм перевірки мобільного телефону рієлтора шляхом надсилання SMS з кодом.
		"""
		h = hashlib.sha256()
		h.update(str(account_id))
		h.update('E66bLuTGzEkDqQHmrSNU') # salt

		token = h.hexdigest()
		record_id = cls.record_prefix + token
		if cls.redis.exists(record_id):
			# todo: suspicious operation
			return

		code = ''.join(random.choice(string.digits) for x in range(6))

		pipe = cls.redis.pipeline()
		pipe.hset(record_id, cls.code_field, code)
		pipe.hset(record_id, cls.attempts_field, 0)
		pipe.hset(record_id, cls.id_field, account_id)
		pipe.hset(record_id, cls.sms_count_field, 1) # first sms will be sent immediately
		pipe.hset(record_id, cls.phone_number_field, mobile_phone)
		pipe.expire(record_id, cls.transaction_ttl)
		pipe.execute()

		set_signed_cookie(response, cls.cookie_name, token, salt=cls.cookie_salt,
		                  seconds_expire=cls.transaction_ttl, http_only=False)

		# Note: даний метод здійснює низку перевірок перед тим як вислати sms
		cls.send_code(mobile_phone, code, request)


	@classmethod
	def check_is_started(cls, request):
		return cls.cookie_name in request.COOKIES


	@classmethod
	def check_code(cls, code, request, response):
		if not code:
			raise EmptyArgument('"code" is empty or None.')


		key = cls.record_prefix + request.get_signed_cookie(cls.cookie_name, salt=cls.cookie_salt)
		if not cls.redis.exists(key):
			response.delete_cookie(cls.cookie_name)
			# todo: ban here
			# todo: admins email
			return False, {'attempts': cls.max_attempts_count}


		attempts_count = cls.redis.hget(key, cls.attempts_field)
		if attempts_count is None:
			# key was deleted moment ago
			response.delete_cookie(cls.cookie_name)
			return False, {'attempts': cls.max_attempts_count}

		attempts_count = int(attempts_count)
		if attempts_count >= cls.max_attempts_count - 1:
			cls.redis.delete(key)
			response.delete_cookie(cls.cookie_name)
			return False, {'attempts': cls.max_attempts_count}

		true_code = cls.redis.hget(key, cls.code_field)
		if true_code is None:
			# key was deleted moment ago
			response.delete_cookie(cls.cookie_name)
			return False, {'attempts': cls.max_attempts_count}

		if code != true_code:
			cls.redis.hincrby(key, cls.attempts_field, 1)
			return False, {'attempts': attempts_count + 1}


		uid = cls.redis.hget(key, cls.id_field)
		if not uid:
			# key was deleted moment ago
			response.delete_cookie(cls.cookie_name)
			return False, {'attempts': cls.max_attempts_count}


		# seems to be ok
		cls.redis.delete(key)
		response.delete_cookie(cls.cookie_name)
		return True, {'id': uid}


	@classmethod
	def resend_sms(cls, request, response):
		key = cls.record_prefix + request.get_signed_cookie(cls.cookie_name, salt=cls.cookie_salt)
		if not cls.redis.exists(key):
			response.delete_cookie(cls.cookie_name)
			# todo: ban ip here
			# todo: admins email
			return


		code = cls.redis.hget(key, cls.code_field)
		if code is None:
			# key was deleted moment ago
			response.delete_cookie(cls.cookie_name)
			return

		phone = cls.redis.hget(key, cls.phone_number_field)
		if phone is None:
			# key was deleted moment ago
			response.delete_cookie(cls.cookie_name)
			return


		# Перевірки розміщено тут, щоб мати змогу залочити, також, і номер.
		if request.user.is_authenticated():
			# todo: ban ip and number here
			return

		if not cls.check_is_started(request):
			# todo: ban ip and number here
			return


		attempts = cls.redis.hget(key, cls.sms_count_field)
		if attempts is None:
			# key was deleted moment ago
			response.delete_cookie(cls.cookie_name)
			return

		attempts = int(attempts)
		if attempts >= cls.max_sms_per_transaction:
			# no more sms to this number
			response.delete_cookie(cls.cookie_name)
			return


		cls.redis.hincrby(key, cls.sms_count_field, 1)
		cls.send_code(phone, code, request, resend=True)


	@classmethod
	def cancel_number_check(cls, request, response):
		key = cls.record_prefix + request.get_signed_cookie(cls.cookie_name, salt=cls.cookie_salt)
		if not cls.redis.exists(key):
			# todo: suspicious operation
			return

		cls.redis.delete(key)
		response.delete_cookie(cls.cookie_name)


	@staticmethod
	def send_code(mobile_phone, code, request, resend=False):
		# todo: тут всі перевірки на кшталт того чи варто слати SMS

		if resend:
			check_codes_sms_sender.resend(mobile_phone, code, resend)
		else:
			check_codes_sms_sender.send(mobile_phone, code, request)


class RegistrationManager(object):
	class EmailValidation(View):
		post_codes = {
			'OK': {
				'code': 0
			},
			'invalid': {
				'code': 1
			},
		    'already_in_use': {
			    'code': 2
		    }
		}

		def post(self, request, *args):
			if request.user.is_authenticated():
				return HttpResponseBadRequest('Anonymous users only.')


			try:
				email = angular_post_parameters(request, ['email'])['email']
			except (ValueError, IndexError):
				return HttpResponseBadRequest('Empty or absent parameter "email".')

			# is email valid?
			try:
				validate_email(email)
			except ValidationError:
				return HttpResponse(json.dumps(self.post_codes['invalid']), content_type='application/json')

			# is email in use?
			if not Users.email_is_free(email):
				return HttpResponse(json.dumps(self.post_codes['already_in_use']), content_type='application/json')

			# seems to be ok
			return HttpResponse(json.dumps(self.post_codes['OK']), content_type='application/json')


	class MobilePhoneValidation(View):
		post_codes = {
			'OK': {
				'code': 0
			},
			'invalid': {
				'code': 1
			},
		    'only_ua':{
			    'code': 2,
		    },
			 'already_in_use': {
			    'code': 3
		    }
		}


		def post(self, request, *args):
			if request.user.is_authenticated():
				return HttpResponseBadRequest('Anonymous users only.')


			try:
				number = angular_post_parameters(request, ['number'])['number']
			except (ValueError, IndexError):
				return HttpResponseBadRequest('Empty or absent parameter "number".')

			# is number correct?
			# todo: check me
			try:
				parsed_number = phonenumbers.parse(number, 'UA')
			except NumberParseException:
				return HttpResponse(json.dumps(self.post_codes['invalid']), content_type='application/json')

			if not phonenumbers.is_valid_number(parsed_number):
				return HttpResponse(json.dumps(self.post_codes['only_ua']), content_type='application/json')

			number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)

			# is number in use?
			if not Users.mobile_phone_number_is_free(number):
				return HttpResponse(json.dumps(self.post_codes['already_in_use']), content_type='application/json')

			# seems to be ok
			return HttpResponse(json.dumps(self.post_codes['OK']), content_type='application/json')


	class Registration(View):
		post_codes = {
			'OK': {
			    'code': 0,
		    },
		    'first_name_empty': {
			    'code': 1,
		    },
		    'last_name_empty': {
			    'code': 2,
		    },
		    'phone_empty': {
			    'code': 3,
		    },
		    'email_empty': {
			    'code': 4,
		    },
		    'password_empty': {
			    'code': 5,
		    },
		    'password_repeat_empty': {
			    'code': 6,
		    },
		    'passwords_not_match': {
			    'code': 7,
		    },

		    # --
		    'invalid_code_check': {
			    'code': 100,
		    },
		}
		redis = redis_connections['steady']
		redis_mob_check_prefix = 'mob_check_'


		def post(self, request, *args):
			if request.user.is_authenticated():
				return HttpResponseBadRequest('Anonymous users only.')


			if MobilePhoneChecker.check_is_started(request):
				try:
					data = angular_post_parameters(request, ['code'])
				except ValueError:
					return HttpResponseBadRequest('Empty or absent parameter "code".')

				response = HttpResponse()
				code = data['code']
				ok, data = MobilePhoneChecker.check_code(code, request, response)
				if not ok:
					# WARNING: deep copy is needed here
					body = copy.deepcopy(self.post_codes['invalid_code_check'])
					body['attempts'] = data['attempts']
					body['max_attempts'] = MobilePhoneChecker.max_attempts_count
					response.write(json.dumps(body))
					return response


				# seems to be ok
				uid = data['id']
				user = Users.objects.filter(id=uid).only('id')[:1][0]
				user.is_active = True
				user.save()

				return LoginManager.Login.login_user_without_password(user, request, response)


			else:
				try:
					data = angular_post_parameters(request,
					        ['name', 'surname', 'phone-number', 'email', 'password', 'password-repeat'])
				except ValueError as e:
					return HttpResponseBadRequest(e.message)


				first_name = data.get('name', '')
				if not first_name:
					return HttpResponseBadRequest(
						json.dumps(self.post_codes['first_name_empty']), content_type='application/json')

				last_name = data.get('surname', '')
				if not last_name:
					return HttpResponseBadRequest(
						json.dumps(self.post_codes['last_name_empty']), content_type='application/json')

				phone_number = data.get('phone-number', '')
				if not phone_number:
					return HttpResponseBadRequest(
						json.dumps(self.post_codes['phone_empty']), content_type='application/json')

				email = data.get('email', '')
				if not email:
					return HttpResponseBadRequest(
						json.dumps(self.post_codes['email_empty']), content_type='application/json')

				password = data.get('password', '')
				if not password:
					return HttpResponseBadRequest(
						json.dumps(self.post_codes['password_empty']), content_type='application/json')

				password_repeat = data.get('password-repeat', '')
				if not password_repeat:
					return HttpResponseBadRequest(
						json.dumps(self.post_codes['password_repeat_empty']), content_type='application/json')


				# passwords match check
				if password != password_repeat:
					return HttpResponseBadRequest(
						json.dumps(self.post_codes['passwords_not_match']), content_type='application/json')


				# ...
				# todo: request check here
				# ...


				# Дана функція зажди повертає результат ОК,
				# незалежно від того чи була насправді відіслана sms.
				# Це зроблено для того, щоб зловмисники у випадку атаки
				# не мали змоги слідкувати за тим чи надсилаються sms.
				response = HttpResponse(json.dumps(self.post_codes['OK']), content_type='application/json')

				# creating of disabled account.
				with transaction.atomic():
					user = Users.objects.create_user(email, phone_number, password)
					user.first_name = first_name
					user.last_name = last_name
					user.save()

					tasks.remove_inactive_account.apply_async(
						[user.id, ], countdown=MobilePhoneChecker.transaction_ttl)
					MobilePhoneChecker.begin_check(user.id, phone_number, request, response)

				# seems to be ok.
				return response


	class Cancel(View):
		post_codes = {
			'OK': {
				'code': 0
			}
		}


		def post(self, request, *args):
			if request.user.is_authenticated():
				return HttpResponseBadRequest('Anonymous users only.')

			response = HttpResponse(json.dumps(self.post_codes['OK']), content_type='application/json')
			MobilePhoneChecker.cancel_number_check(request, response)
			return response


	class ResendCheckSMS(View):
		post_codes = {
			'OK': {
				'code': 0
			}
		}


		def post(self, request, *args):
			if request.user.is_authenticated():
				return HttpResponseBadRequest('Anonymous users only.')

			# Дана функція зажди повертає результат ОК,
			# незалежно від того чи була насправді відіслана sms.
			# Це зроблено для того, щоб зловмисники у випадку атаки
			# не мали змоги слідкувати за тим чи надсилаються sms.
			response = HttpResponse(json.dumps(self.post_codes['OK']), content_type='application/json')
			try:
				MobilePhoneChecker.resend_sms(request, response)
			except Exception:
				pass
			return response


class LoginManager(object):
	class Login(View):
		post_codes = {
			'OK': {
			    'code': 0,
		    },
			'username_empty': {
				'code': 1,
			},
		    'password_empty': {
			    'code': 2,
		    },
		    'invalid_attempt': {
			    'code': 3,
		    },
		}


		def post(self, request, *args):
			if request.user.is_authenticated():
				return HttpResponseBadRequest('Anonymous only.')

			try:
				d = angular_post_parameters(request, ['username', 'password'])
			except ValueError:
				return HttpResponseBadRequest('Empty or absent parameter "username" or "password"')


			username = d.get('username', '')
			if not username:
				return HttpResponseBadRequest(
					json.dumps(self.post_codes['username_empty']), content_type='application/json')

			password = d.get('password', '')
			if not username:
				return HttpResponseBadRequest(
					json.dumps(self.post_codes['password_empty']), content_type='application/json')


			# attempt with phone number
			phone_number = phonenumbers.parse(username, 'UA')
			if phonenumbers.is_valid_number(phone_number):
				username = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)

			user = Users.objects.filter(mobile_phone=username).only('id')[:1]
			if not user:
				# attempt with email
				user = Users.objects.filter(email=username).only('id')[:1]
				if not user:
					return HttpResponse(
						json.dumps(self.post_codes['invalid_attempt']), content_type='application/json')


			user = user[0]
			user = authenticate(username=user.mobile_phone, password=password)
			if user is not None:
				if user.is_active:
					# seems to be ok
					response = HttpResponse(content_type='application/json')
					return self.login_user_without_password(user, request, response)

			return HttpResponse(
				json.dumps(self.post_codes['invalid_attempt']), content_type='application/json')


		@classmethod
		def login_user_without_password(cls, user, request, response):
			user.backend = 'django.contrib.auth.backends.ModelBackend'
			login(request, user)

			# WARNING: deep copy is needed here
			body = copy.deepcopy(cls.post_codes['OK'])
			body['user'] = LoginManager.on_login_data(user)
			response.write(json.dumps(body))
			return response


	class Logout(View):
		post_codes = {
			'OK': {
			    'code': 0,
		    },
		}


		def post(self, request, *args):
			if not request.user.is_authenticated():
				return HttpResponseBadRequest('Authenticated only.')

			logout(request)
			return HttpResponse(json.dumps(self.post_codes['OK']), content_type='application/json')


	class OnLogin(View):
		post_codes = {
			'OK': {
			    'code': 0,
		    },
		}


		def get(self, request, *args):
			if not request.user.is_authenticated():
				return HttpResponseBadRequest('Authenticated only.')

			# WARNING: deep copy is needed here
			body = copy.deepcopy(self.post_codes['OK'])
			body['user'] = LoginManager.on_login_data(request.user)
			return HttpResponse(json.dumps(body), content_type='application/json')


	@staticmethod
	def on_login_data(user):
		return {
			'name': user.first_name,
		    'surname': user.last_name,
		}



class Contacts(View):
	"""
	Implements operations for getting contacts of realtors on main pages of the site.
	"""
	get_codes = {
		'OK': {
			'code': 0,
		    'contacts': None, # WARN: owner's contacts here
		},
	    'invalid_parameters': {
		    'code': 1
	    },
	    'invalid_tid': {
		    'code': 2
	    },
	    'invalid_hid': {
		    'code': 3
	    },
	}


	def get(self, request, *args):
		"""
		Returns contacts of the owner of the publication accordingly to his preferences.
		"""
		try:
			tid, hid = args[0].split(':')
			tid = int(tid)
			hid = int(hid)
		except (ValueError, IndexError):
			return HttpResponseBadRequest(
				json.dumps(self.get_codes['invalid_parameters']), content_type='application/json')


		if tid not in OBJECTS_TYPES.values():
			return HttpResponseBadRequest(
				json.dumps(self.get_codes['invalid_tid']), content_type='application/json')


		model = HEAD_MODELS[tid]
		try:
			publication = model.objects.filter(id=hid).only('id', 'owner')[:1][0]
		except IndexError:
			return HttpResponseBadRequest(
				json.dumps(self.get_codes['invalid_hid']), content_type='application/json')


		data = copy.deepcopy(self.get_codes['OK']) # WARN: deep copy here
		data['contacts'] = publication.owner.contacts()
		return HttpResponse(json.dumps(data), content_type='application/json')

