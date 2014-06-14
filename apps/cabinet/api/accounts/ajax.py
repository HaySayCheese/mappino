#coding=utf-8
from copy import deepcopy
import json
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponseBadRequest, HttpResponse
import phonenumbers

from apps.classes import CabinetView
from collective.exceptions import RuntimeException
from collective.methods.request_data_getters import angular_post_parameters
from core.users.classes import UserAvatar
from core.users.constants import Preferences
from core.users.models import Users
from core.users import exceptions as users_exceptions


class AccountManager(object):
	class AccountView(CabinetView):
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

			    'nickname_already_taken': {
				    'code': 31
			    },
			    'nickname_to_short': {
				    'code': 32
			    }
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

			    'nickname': self.update_alias,


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


		def get(self, request, *args):
			"""
			Повертає JSON-відповідь з переліком контактів користувача та його налаштувань.
			"""
			user = request.user
			preferences = user.preferences()

			# На фронтенді виставлена маска, яка вже включає в себе +380,
			# тому мобільні номери треба віддати у форматі 093..
			if user.mobile_phone:
				mobile_phone_number = phonenumbers.format_number(
					phonenumbers.parse(user.mobile_phone),
					phonenumbers.PhoneNumberFormat.NATIONAL).replace(" ", '')[1:] # зайві пробіли і поч. 0 видаляються
			else:
				mobile_phone_number = ''

			if user.add_mobile_phone:
				add_mobile_phone_number = phonenumbers.format_number(
					phonenumbers.parse(user.add_mobile_phone),
					phonenumbers.PhoneNumberFormat.NATIONAL).replace(" ", '')[1:] # зайві пробіли і поч. 0 видаляються
			else:
				add_mobile_phone_number = ''

			# Стаціонарні і робочі телефони ніяк не валідуються
			landline_phone_number = user.landline_phone if user.landline_phone else ''
			add_landline_phone_number = user.add_landline_phone if user.add_landline_phone else ''


			data = {
				'account': {
					'first_name': user.first_name or '',
				    'last_name': user.last_name or '',
				    'email': user.email or '',
				    'work_email': user.work_email or '',
				    'skype': user.skype or '',
				    'avatar_url': user.avatar().url() or '',
				    'nickname': '', # todo: додати нікнейм

				    'mobile_phone': mobile_phone_number,
				    'add_mobile_phone': add_mobile_phone_number,
				    'landline_phone': landline_phone_number,
				    'add_landline_phone': add_landline_phone_number,
				},
			    'preferences': {
				    # bool values
					'allow_call_requests': preferences.allow_call_requests,
					'allow_messaging': preferences.allow_messaging,
			        'hide_email': preferences.hide_email,
			        'hide_mobile_phone_number': preferences.hide_mobile_phone_number,
			        'hide_add_mobile_phone_number': preferences.hide_add_mobile_phone_number,
			        'hide_landline_phone_number': preferences.hide_landline_phone,
			        'hide_add_landline_phone_number': preferences.hide_add_landline_phone,
					'hide_skype': preferences.hide_skype,

			        # sids
			        'send_call_request_notifications_to_sid': preferences.send_call_request_notifications_to_sid,
			        'send_message_notifications_to_sid': preferences.send_message_notifications_to_sid,
			    }
			}

			# Видалення пустих записів і надсилання
			data['account'].update((k, v) for k, v in data['account'].iteritems() if v is not None)
			return HttpResponse(json.dumps(data), content_type='application/json')


		def post(self, request, *args):
			try:
				params = angular_post_parameters(request, ['f', 'v'])
				field = params.get('f', '')
				value = params.get('v', '')
			except ValueError:
				return HttpResponseBadRequest('Invalid or absent parameter @field or @value.')

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
			if allow not in (True, False):
				return HttpResponseBadRequest('Invalid @value.')


			preferences = user.preferences()
			preferences.allow_call_requests = allow
			preferences.save()
			return HttpResponse(
				json.dumps(self.post_codes['OK']), content_type='application/json')


		def update_alias(self, user, alias):
			if user.alias == alias:
				return

			if not alias:
				user.alias = ''
				user.save()
				return

			try:
				Users.validate_alias(alias, user)

			except users_exceptions.AliasAlreadyTaken:
				return HttpResponse(
					json.dumps(self.post_codes['nickname_already_taken']), content_type='application/json')

			except users_exceptions.TooShortAlias:
				return HttpResponse(
					json.dumps(self.post_codes['nickname_to_short']), content_type='application/json')

			user.alias = alias
			user.save()
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
			if allow not in (True, False):
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
			if hide not in (True, False):
				return HttpResponseBadRequest('Invalid @value.')


			preferences = user.preferences()
			preferences.hide_email = hide
			preferences.save()
			return HttpResponse(
				json.dumps(self.post_codes['OK']), content_type='application/json')


		def update_hide_mobile_phone(self, user, hide):
			if hide not in (True, False):
				return HttpResponseBadRequest('Invalid @value.')


			preferences = user.preferences()
			preferences.hide_mobile_phone_number = hide
			preferences.save()
			return HttpResponse(
				json.dumps(self.post_codes['OK']), content_type='application/json')


		def update_hide_add_mobile_phone(self, user, hide):
			if hide not in (True, False):
				return HttpResponseBadRequest('Invalid @value.')


			preferences = user.preferences()
			preferences.hide_add_mobile_phone_number = hide
			preferences.save()
			return HttpResponse(
				json.dumps(self.post_codes['OK']), content_type='application/json')


		def update_hide_landline_phone(self, user, hide):
			if hide not in (True, False):
				return HttpResponseBadRequest('Invalid @value.')


			preferences = user.preferences()
			preferences.hide_landline_phone = hide
			preferences.save()
			return HttpResponse(
				json.dumps(self.post_codes['OK']), content_type='application/json')


		def update_hide_add_landline_phone(self, user, hide):
			if hide not in (True, False):
				return HttpResponseBadRequest('Invalid @value.')


			preferences = user.preferences()
			preferences.hide_add_landline_phone = hide
			preferences.save()
			return HttpResponse(json.dumps(self.post_codes['OK']), content_type='application/json')


		def update_hide_skype(self, user, hide):
			if hide not in (True, False):
				return HttpResponseBadRequest('Invalid @value.')


			preferences = user.preferences()
			preferences.hide_skype = hide
			preferences.save()
			return HttpResponse(
				json.dumps(self.post_codes['OK']), content_type='application/json')



	class AvatarUpdate(CabinetView):
		post_codes = {
			'OK': {
				'code': 0
			},
		    'too_large': {
			    'code': 1
		    },
		    'too_small': {
			    'code': 2,
		    },
		    'unsupported_type': {
			    'code': 3
		    },

		    'unknown_error': {
			    'code': 100
		    }
		}

		def post(self, request, *args):
			# check if request is not empty
			image = request.FILES.get('file')
			if image is None:
				return HttpResponseBadRequest('No image found in request.')

			try:
				# updating
				request.user.avatar().update(image)

			except UserAvatar.TooLargeImage:
				return HttpResponse(json.dumps(self.post_codes['too_large']), content_type='application/json')
			except UserAvatar.TooSmallImage:
				return HttpResponse(json.dumps(self.post_codes['too_small']), content_type='application/json')
			except UserAvatar.InvalidImageFormat:
				return HttpResponse(json.dumps(self.post_codes['unsupported_type']), content_type='application/json')
			except RuntimeException:
				return HttpResponse(json.dumps(self.post_codes['unknown_error']), content_type='application/json')

			# seems to be ok
			response = deepcopy(self.post_codes['OK'])
			response.update({
				'url': request.user.avatar().url()
			})
			return HttpResponse(json.dumps(response), content_type='application/json')