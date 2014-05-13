#coding=utf-8
import json
from collective.decorators.views import login_required_or_forbidden
from collective.exceptions import EmptyArgument, InvalidArgument, DuplicateValue, RuntimeException
from collective.methods.request_data_getters import angular_post_parameters
from collective.validators import validate_mobile_phone_number
from core.users.constants import Preferences
from core.users.models import UsersManager, Users
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
from django.http import HttpResponseBadRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View
import phonenumbers


class AccountManager(object):
	class AccountView(View):
		def __init__(self):
			super(AccountManager.AccountView, self).__init__()
			self.post_codes = {
				'OK': {
					'code': 0
				},

			    'invalid_email': {
				    'code': 10
			    },
			    'duplicated_email': {
					'code': 11
			    },

			    'invalid_phone': {
				    'code': 20
			    },
			    'duplicated_phone': {
				    'code': 21
			    },
			}

			self.update_methods = {
				'first_name': self.update_first_name,
				'last_name': self.update_last_name,
			    'email': self.update_email,
			    'work_email': self.update_work_email,
			    'mobile_phone': self.update_mobile_phone_number,
			    'add_mobile_phone': self.update_add_mobile_phone_number,
			    'landline_phone': self.update_landline_phone_number,
			    'add_landline_phone': self.update_add_landline_phone_number,
			    'skype': self.update_skype,


				'allow_call_requests': self.update_allow_call_request,
			    'send_call_request_notifications_to_sid': self.update_send_call_request_notifications_to_sid,

				'allow_messaging': self.update_allow_messaging,
			    'send_message_notifications_to_sid': self.update_send_call_request_notifications_to_sid,

				'hide_email': self.update_hide_email,
			    'hide_mobile_phone_number': self.update_hide_mobile_phone,
			    'hide_add_mobile_phone_number': self.update_hide_add_mobile_phone,
			    'hide_landline_phone_number': self.update_hide_landline_phone,
			    'hide_add_landline_phone_number': self.update_hide_add_landline_phone,
			    'hide_skype': self.update_hide_skype,
			}


		@method_decorator(login_required_or_forbidden)
		def dispatch(self, *args, **kwargs):
			return super(AccountManager.AccountView, self).dispatch(*args, **kwargs)


		def get(self, request, *args):
			user = request.user
			preferences = user.preferences()


			# phones formatting
			if user.mobile_phone:
				mobile_phone_number = phonenumbers.format_number(
					phonenumbers.parse(user.mobile_phone),
					phonenumbers.PhoneNumberFormat.NATIONAL).replace(" ", '')[1:]
			else:
				mobile_phone_number = ''


			if user.add_mobile_phone:
				add_mobile_phone_number = phonenumbers.format_number(
					phonenumbers.parse(user.add_mobile_phone),
					phonenumbers.PhoneNumberFormat.NATIONAL).replace(" ", '')[1:]
			else:
				add_mobile_phone_number = ''


			if user.landline_phone:
				landline_phone_number = user.landline_phone
			else:
				landline_phone_number = ''


			if user.add_landline_phone:
				add_landline_phone_number = user.add_landline_phone
			else:
				add_landline_phone_number = ''


			data = {
				'account': {
					'first_name': user.first_name or '',
				    'last_name': user.last_name or '',
				    'email': user.email or '',
				    'work_email': user.work_email or '',
				    'mobile_phone': mobile_phone_number,
				    'add_mobile_phone': add_mobile_phone_number,
				    'landline_phone': landline_phone_number,
				    'add_landline_phone': add_landline_phone_number,
				    'skype': user.skype or ''
				},
			    'preferences': {
				    # bool values
					'allow_call_requests': preferences.allow_call_requests,
					'allow_messaging': preferences.allow_messaging,

			        'hide_email': preferences.hide_email,
			        'hide_mobile_phone_number': preferences.hide_mobile_phone_number,
			        'hide_add_mobile_phone_number': preferences.hide_add_mobile_phone_number,

			        'hide_landline_phone': preferences.hide_landline_phone,
			        'hide_add_landline_phone': preferences.hide_add_landline_phone,
					'hide_skype': preferences.hide_skype,

			        # sids
			        'send_call_request_notifications_to_sid': preferences.send_call_request_notifications_to_sid,
			        'send_message_notifications_to_sid': preferences.send_message_notifications_to_sid,
			    }
			}

			# clearing empty parameters and forming response
			data['account'].update((k, v) for k, v in data['account'].iteritems() if v is not None)

			return HttpResponse(json.dumps(data), content_type='application/json')


		def post(self, request, *args):
			try:
				data = angular_post_parameters(request, ['f', 'v'])
			except ValueError:
				return HttpResponseBadRequest('Invalid or absent parameter @field or @value.')

			field = data.get('f', '')
			value = data.get('v', '')

			if field == '':
				return HttpResponseBadRequest('Invalid or absent parameter @field')
				# (value can be empty)


			update_method = self.update_methods.get(field)
			if update_method is None:
				return HttpResponseBadRequest('Invalid parameter @field.')

			return update_method(request.user, value)


		def update_first_name(self, user, name):
			"""
			@name is required.
			"""
			if not name:
				return HttpResponseBadRequest('@value can\'t be empty.')

			user.first_name = name
			user.save()
			return HttpResponse(json.dumps(
				self.post_codes['OK']), content_type='application/json')


		def update_last_name(self, user, name):
			"""
			@name is required.
			"""
			if not name:
				return HttpResponseBadRequest('@value can\'t be empty.')

			user.last_name = name
			user.save()
			return HttpResponse(json.dumps(
				self.post_codes['OK']), content_type='application/json')


		def update_email(self, user, email):
			"""
			@email is required.
			"""
			if not email:
				return HttpResponseBadRequest('@value can\'t be empty.')

			if user.email == email:
				return HttpResponse(json.dumps(
					self.post_codes['OK']), content_type='application/json')


			try:
				validate_email(email)
			except ValidationError:
				return HttpResponse(json.dumps(
					self.post_codes['invalid_email']), content_type='application/json')


			# check for duplicates
			if not Users.email_is_free(email):
				return HttpResponse(json.dumps(
					self.post_codes['duplicated_email']), content_type='application/json')


			user.email = email
			user.save()
			return HttpResponse(json.dumps(
				self.post_codes['OK']), content_type='application/json')


		def update_work_email(self, user, email):
			"""
			@email may be empty.
			"""
			if not email:
				user.work_email = ''
				user.save()
				return HttpResponse(json.dumps(
					self.post_codes['OK']), content_type='application/json')


			try:
				validate_email(email)
			except ValidationError:
				return HttpResponse(json.dumps(
					self.post_codes['invalid_email']), content_type='application/json')


			# check for duplicates
			if not Users.email_is_free(email):
				return HttpResponse(json.dumps(
					self.post_codes['duplicated_email']), content_type='application/json')


			user.work_email = email
			user.save()
			return HttpResponse(json.dumps(
				self.post_codes['OK']), content_type='application/json')


		def update_mobile_phone_number(self, user, phone):
			"""
			@phone is required.
			"""
			if not phone:
				return HttpResponseBadRequest('@value can\'t be empty.')


			try:
				phone = phonenumbers.parse(phone)
				if not phonenumbers.is_valid_number(phone):
					raise ValidationError('Invalid number.')
			except (phonenumbers.NumberParseException, ValidationError):
				return HttpResponse(json.dumps(
					self.post_codes['invalid_phone']), content_type='application/json')


			phone = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164)
			if user.mobile_phone == phone:
				# already the same
				return HttpResponse(json.dumps(
					self.post_codes['OK']), content_type='application/json')


			# check for duplicates
			if not user.mobile_phone_number_is_free(phone):
				return HttpResponse(json.dumps(
					self.post_codes['duplicated_phone']), content_type='application/json')


			user.mobile_phone = phone
			user.save()
			return HttpResponse(json.dumps(
				self.post_codes['OK']), content_type='application/json')


		def update_add_mobile_phone_number(self, user, phone):
			"""
			@phone may be empty.
			"""
			if not phone:
				user.add_mobile_phone = ''
				user.save()
				return HttpResponse(json.dumps(
					self.post_codes['OK']), content_type='application/json')


			try:
				phone = phonenumbers.parse(phone)
				if not phonenumbers.is_valid_number(phone):
					raise ValidationError('Invalid number.')
			except (phonenumbers.NumberParseException, ValidationError):
				return HttpResponse(json.dumps(
					self.post_codes['invalid_phone']), content_type='application/json')


			phone = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164)
			if user.add_mobile_phone == phone:
				# already the same
				return HttpResponse(json.dumps(
					self.post_codes['OK']), content_type='application/json')


			# check for duplicates
			if user.mobile_phone == phone:
				return  HttpResponse(
					json.dumps(self.post_codes['duplicated_phone']), content_type='application/json')


			user.add_mobile_phone = phone
			user.save()
			return HttpResponse(json.dumps(
				self.post_codes['OK']), content_type='application/json')


		def update_landline_phone_number(self, user, phone):
			"""
			@phone may be empty.
			"""
			if not phone:
				user.landline_phone = ''
				user.save()
				return HttpResponse(json.dumps(
					self.post_codes['OK']), content_type='application/json')


			# check for duplicates
			if user.add_landline_phone:
				return HttpResponse(json.dumps(
					self.post_codes['duplicated_phone']), content_type='application/json')


			user.landline_phone = phone
			user.save()
			return HttpResponse(json.dumps(
				self.post_codes['OK']), content_type='application/json')


		def update_add_landline_phone_number(self, user, phone):
			"""
			@phone may be empty.
			"""
			if not phone:
				user.add_landline_phone = ''
				user.save()
				return HttpResponse(json.dumps(
					self.post_codes['OK']), content_type='application/json')


			# check for duplicates
			if user.landline_phone == phone:
				return HttpResponse(json.dumps(
					self.post_codes['duplicated_phone']), content_type='application/json')


			user.add_landline_phone = phone
			user.save()
			return HttpResponse(json.dumps(
				self.post_codes['OK']), content_type='application/json')


		def update_skype(self, user, login):
			"""
			@login may be empty.
			"""
			user.skype = login
			user.save()
			return HttpResponse(json.dumps(
				self.post_codes['OK']), content_type='application/json')


		def update_allow_call_request(self, user, allow):
			if allow is not bool:
				return HttpResponseBadRequest('Invalid @value.')


			preferences = user.preferences()
			preferences.allow_call_requests = allow
			preferences.save()
			return HttpResponse(
				json.dumps(self.post_codes['OK']), content_type='application/json')


		def update_send_call_request_notifications_to_sid(self, user, sid):
			sid = int(sid)
			if sid not in Preferences.CALL_REQUEST_NOTIFICATIONS.values():
				return HttpResponseBadRequest('Invalid @value.')

			preferences = user.preferences()
			preferences.send_call_request_notifications_to_sid = sid
			preferences.save()
			return HttpResponse(
				json.dumps(self.post_codes['OK']), content_type='application/json')


		def update_allow_messaging(self, user, allow):
			if allow is not bool:
				return HttpResponseBadRequest('Invalid @value.')


			preferences = user.preferences()
			preferences.allow_messaging = allow
			preferences.save()
			return HttpResponse(
				json.dumps(self.post_codes['OK']), content_type='application/json')


		def update_send_message_notifications_to_sid(self, user, sid):
			sid = int(sid)
			if sid not in Preferences.MESSAGE_NOTIFICATIONS.values():
				return HttpResponseBadRequest('Invalid @value.')

			preferences = user.preferences()
			preferences.send_message_notifications_to_sid = sid
			preferences.save()
			return HttpResponse(
				json.dumps(self.post_codes['OK']), content_type='application/json')


		def update_hide_email(self, user, hide):
			if hide is not bool:
				return HttpResponseBadRequest('Invalid @value.')


			preferences = user.preferences()
			preferences.hide_email = hide
			preferences.save()
			return HttpResponse(
				json.dumps(self.post_codes['OK']), content_type='application/json')


		def update_hide_mobile_phone(self, user, hide):
			if hide is not bool:
				return HttpResponseBadRequest('Invalid @value.')


			preferences = user.preferences()
			preferences.hide_mobile_phone_number = hide
			preferences.save()
			return HttpResponse(
				json.dumps(self.post_codes['OK']), content_type='application/json')


		def update_hide_add_mobile_phone(self, user, hide):
			if hide is not bool:
				return HttpResponseBadRequest('Invalid @value.')


			preferences = user.preferences()
			preferences.hide_add_mobile_phone_number = hide
			preferences.save()
			return HttpResponse(
				json.dumps(self.post_codes['OK']), content_type='application/json')


		def update_hide_landline_phone(self, user, hide):
			if hide is not bool:
				return HttpResponseBadRequest('Invalid @value.')


			preferences = user.preferences()
			preferences.hide_landline_phone = hide
			preferences.save()
			return HttpResponse(
				json.dumps(self.post_codes['OK']), content_type='application/json')


		def update_hide_add_landline_phone(self, user, hide):
			if hide is not bool:
				return HttpResponseBadRequest('Invalid @value.')


			preferences = user.preferences()
			preferences.hide_add_landline_phone = hide
			preferences.save()
			return HttpResponse(json.dumps(self.post_codes['OK']), content_type='application/json')


		def update_hide_skype(self, user, hide):
			if hide is not bool:
				return HttpResponseBadRequest('Invalid @value.')


			preferences = user.preferences()
			preferences.hide_skype = hide
			preferences.save()
			return HttpResponse(
				json.dumps(self.post_codes['OK']), content_type='application/json')



class Account(View):
	post_codes = {
		'OK': {
		    'code': 0
	    },
	    'invalid_parameters': {
		    'code': 1
	    },

	    #--
	    'empty_first_name': {
		    'code': 10
	    },

	    #--
	    'empty_last_name': {
		    'code': 20
	    },

	    #--
	    'empty_email': {
		    'code': 30
	    },
	    'invalid_email': {
		    'code': 31
	    },

	    #--
	    'empty_work_email': {
		    'code': 40
	    },
	    'invalid_work_email': {
		    'code': 41
	    },

	    #--
	    'empty_mobile_phone': {
		    'code': 50
	    },
	    'invalid_mobile_phone': {
		    'code': 51
	    },
	    'duplicated_mobile_phone': {
		    'code': 52
	    },

	    #--
	    'empty_add_mobile_phone': {
		    'code': 60
	    },
	    'invalid_add_mobile_phone': {
		    'code': 61
	    },
	    'duplicated_add_mobile_phone': {
		    'code': 62
	    },

	    #--
	    'empty_landline_phone': {
		    'code': 70
	    },

	    #--
	    'empty_add_landline_phone': {
		    'code': 80
	    },

		#--
	    'invalid_field': {
		    'code': 1000
	    },
	}


	@method_decorator(login_required_or_forbidden)
	def dispatch(self, *args, **kwargs):
		return super(Account, self).dispatch(*args, **kwargs)


	def post(self, request, *args):
		"""
		Updates user data.
		Request must contains two parameters:
			"f" — field name that should be updated.
			"v" — value that should be used for update.
				  Value can be empty. In this case the field will be cleared.
		"""
		try:
			data = angular_post_parameters(request, ['f'])
		except ValueError:
			return HttpResponseBadRequest(
				json.dumps(self.post_codes['invalid_parameters']), content_type='application/json')


		field = data['f']
		value = data.get('v', '') # WARN: may be empty
		user = request.user


		if field == 'first_name':
			try:
				self.update_first_name(user, value)
				return HttpResponse(json.dumps(self.post_codes['OK']), content_type='application/json')

			except EmptyArgument:
				return HttpResponseBadRequest(
					json.dumps(self.post_codes['empty_first_name']), content_type='application/json')


		elif field == 'last_name':
			try:
				self.update_last_name(user, value)
				return HttpResponse(json.dumps(self.post_codes['OK']), content_type='application/json')

			except EmptyArgument:
				return HttpResponseBadRequest(
					json.dumps(self.post_codes['empty_last_name']), content_type='application/json')


		# todo: додати підтвердження емейлу по ссилці
		# todo: додати підтвердження робочого емейлу по ссилці


		elif field == 'mobile_phone':
			try:
				self.update_mobile_phone(user, value)
				return HttpResponse(json.dumps(self.post_codes['OK']), content_type='application/json')

			except EmptyArgument:
				return HttpResponseBadRequest(
					json.dumps(self.post_codes['empty_mobile_phone']), content_type='application/json')
			except InvalidArgument:
				return HttpResponseBadRequest(
					json.dumps(self.post_codes['invalid_mobile_phone']), content_type='application/json')
			except DuplicateValue:
				return HttpResponseBadRequest(
					json.dumps(self.post_codes['duplicated_mobile_phone']), content_type='application/json')


		elif field == 'add_mobile_phone':
			try:
				self.update_add_mobile_phone(user, value)
				return HttpResponse(json.dumps(self.post_codes['OK']), content_type='application/json')

			except EmptyArgument:
				return HttpResponseBadRequest(
					json.dumps(self.post_codes['empty_add_mobile_phone']), content_type='application/json')
			except InvalidArgument:
				return HttpResponseBadRequest(
					json.dumps(self.post_codes['invalid_add_mobile_phone']), content_type='application/json')
			except DuplicateValue:
				return HttpResponseBadRequest(
					json.dumps(self.post_codes['duplicated_add_mobile_phone']), content_type='application/json')


		elif field == 'landline_phone':
			try:
				self.update_landline_phone(user, value)
				return HttpResponse(json.dumps(self.post_codes['OK']), content_type='application/json')

			except EmptyArgument:
				return HttpResponseBadRequest(
					json.dumps(self.post_codes['empty_landline_phone']), content_type='application/json')


		elif field == 'add_landline_phone':
			try:
				self.update_add_landline_phone(user, value)
				return HttpResponse(json.dumps(self.post_codes['OK']), content_type='application/json')

			except EmptyArgument:
				return HttpResponseBadRequest(
					json.dumps(self.post_codes['empty_add_landline_phone']), content_type='application/json')


		# todo: додати завантаження аватарки


		# no one field was updated
		return HttpResponseBadRequest(
			json.dumps(self.post_codes['invalid_field']), content_type='application/json')


	@classmethod
	def update_first_name(cls, user, first_name):
		if not user:
			# RuntimeException is preferred InvalidArgument because of "user" is system parameter
			# and if it is None — than error occurred in code.
			raise RuntimeException()


		if not first_name:
			raise EmptyArgument()

		user.name = first_name
		user.save()


	@classmethod
	def update_last_name(cls, user, last_name):
		if not user:
			# RuntimeException is preferred InvalidArgument because of "user" is system parameter
			# and if it is None — than error occurred in code.
			raise RuntimeException()


		if not last_name:
			raise EmptyArgument()

		user.surname = last_name
		user.save()


	# todo: update_email
	# todo: update_work_email


	@classmethod
	def update_mobile_phone(cls, user, mobile_phone):
		if not user:
			# RuntimeException is preferred InvalidArgument because of "user" is system parameter
			# and if it is None — than error occurred in code.
			raise RuntimeException()


		if not mobile_phone:
			raise EmptyArgument()

		try:
			mobile_phone = UsersManager.normalize_phone_number(mobile_phone)
			validate_mobile_phone_number(mobile_phone)
		except ValidationError:
			raise InvalidArgument('Invalid "mobile_phone": {0}'.format(mobile_phone))

		if user.mobile_phone == mobile_phone:
			return
		else:
			try:
				user.mobile_phone = mobile_phone
				user.save()
			except IntegrityError:
				raise DuplicateValue('Integrity error occurred. phone {0} already exists.'.format(mobile_phone))


	@classmethod
	def update_add_mobile_phone(cls, user, mobile_phone):
		if not user:
			# RuntimeException is preferred InvalidArgument because of "user" is system parameter
			# and if it is None — than error occurred in code.
			raise RuntimeException()


		if not mobile_phone:
			raise EmptyArgument()

		try:
			mobile_phone = UsersManager.normalize_phone_number(mobile_phone)
			validate_mobile_phone_number(mobile_phone)
		except ValidationError:
			raise InvalidArgument('Invalid "mobile_phone": {0}'.format(mobile_phone))

		if user.add_mobile_phone == mobile_phone:
			return
		else:
			try:
				user.add_mobile_phone = mobile_phone
				user.save()
			except IntegrityError:
				raise DuplicateValue('Integrity error occurred. phone {0} already exists.'.format(mobile_phone))


	@classmethod
	def update_landline_phone(cls, user, phone):
		if not user:
			# RuntimeException is preferred InvalidArgument because of "user" is system parameter
			# and if it is None — than error occurred in code.
			raise RuntimeException()


		if not phone:
			raise EmptyArgument()

		# landline phone is not personal, therefor it may not be unique.
		# no need for checks here.

		user.landline_phone = phone
		user.save()


	@classmethod
	def update_add_landline_phone(cls, user, phone):
		if not user:
			# RuntimeException is preferred InvalidArgument because of "user" is system parameter
			# and if it is None — than error occurred in code.
			raise RuntimeException()


		if not phone:
			raise EmptyArgument()

		# landline phone is not personal, therefor it may not be unique.
		# no need for checks here.

		user.add_landline_phone = phone
		user.save()