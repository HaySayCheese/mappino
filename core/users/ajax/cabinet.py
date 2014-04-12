#coding=utf-8
import json

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.http.response import HttpResponseBadRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View

from collective.decorators.views import login_required_or_forbidden
from collective.exceptions import InvalidArgument, EmptyArgument, RuntimeException, DuplicateValue
from collective.methods.request_data_getters import angular_post_parameters
from collective.validators import validate_mobile_phone_number
from core.users.models import UsersManager


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

