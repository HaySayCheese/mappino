#coding=utf-8
import json

from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.generic import View

from apps.main.api.correspondence.utils import send_notification_about_new_message, send_notification_about_new_call_request
from collective.exceptions import InvalidArgument, InvalidHttpParameter
from collective.methods.request_data_getters import angular_parameters
from core.publications.constants import OBJECTS_TYPES, HEAD_MODELS



class SendMessageFromClient(View):
	post_codes = {
		'Ok': {
			'code': 0,
		},
		'invalid_hash_id': {
			'code': 1
		},
	    'invalid_parameters': {
		    'code': 2
	    },
	    'invalid_tid': {
			'code': 3
	    },
	}


	def post(self, request, *args):
		try:
			tid, hash_hid = args[0].split(':')
			if (tid is None) or (hash_hid is None):
				raise InvalidHttpParameter()

		except (
			IndexError, # args doesn't contains required params
			InvalidHttpParameter, # tid or hash_id is None
		):
			return HttpResponseBadRequest(
				json.dumps(self.post_codes['invalid_parameters']), content_type='application/json')


		try:
			tid = int(tid)
			if tid not in OBJECTS_TYPES.values():
				raise InvalidHttpParameter()

		except (
			InvalidHttpParameter, # tid is incorrect object type
			ValueError, # tid is not an int
		):
			return HttpResponseBadRequest(
				json.dumps(self.post_codes['invalid_tid']), content_type='application/json')


		try:
			params = angular_parameters(request, ['email', 'message'])
		except (
			ValueError, # email or message is not specified
		):
			return HttpResponseBadRequest(json.dumps(
				self.post_codes['invalid_parameters']), content_type='application/json')


		model = HEAD_MODELS.get(tid)
		try:
			publication = model.objects.filter(hash_id = hash_hid).only('id', 'owner', 'state_sid', 'body__title')[:1][0]
		except (
			IndexError, # models doesn't contains record with exact hash
		):
			return HttpResponse( # request semantically is correct
				json.dumps(self.post_codes['invalid_parameters']), content_type='application/json')


		# security checks
		if not publication.is_published():
			raise SuspiciousOperation('Attempt to comment unpublished publication.')


		try:
			send_notification_about_new_message(
				request, tid, publication,

				params['message'],
				params['email'],
				params.get('name', '') # is not required
			 )

		except (
			InvalidArgument, # message is empty
		):
			return HttpResponseBadRequest(
				json.dumps(self.post_codes['invalid_parameters']), content_type='application/json')

		return HttpResponse(json.dumps(self.post_codes['Ok']), content_type="application/json")



class SendCallRequestFromClient(View):
	post_codes = {
		'Ok': {
			'code': 0,
		},
		'invalid_hash_id': {
			'code': 1
		},
	    'invalid_parameters': {
		    'code': 2
	    }
	}

	def post(self, request, *args):
		try:
			tid, hash_hid = args[0].split(':')
			if (tid is None) or (hash_hid is None):
				raise InvalidHttpParameter()

		except (
			IndexError, # args doesn't contains required params
			InvalidHttpParameter, # tid or hash_id is None
		):
			return HttpResponseBadRequest(
				json.dumps(self.post_codes['invalid_parameters']), content_type='application/json')


		try:
			tid = int(tid)
			if tid not in OBJECTS_TYPES.values():
				raise InvalidHttpParameter()

		except (
			InvalidHttpParameter, # tid is incorrect object type
			ValueError, # tid is not an int
		):
			return HttpResponseBadRequest(
				json.dumps(self.post_codes['invalid_tid']), content_type='application/json')


		try:
			params = angular_parameters(request, ['phone_number'])
		except (
			ValueError, # email or message is not specified
		):
			return HttpResponseBadRequest(json.dumps(
				self.post_codes['invalid_parameters']), content_type='application/json')


		model = HEAD_MODELS.get(tid)
		try:
			publication = model.objects.filter(hash_id = hash_hid).only('id', 'owner', 'state_sid', 'body__title')[:1][0]
		except (
			IndexError, # models doesn't contains record with exact hash
		):
			return HttpResponse( # request semantically is correct
				json.dumps(self.post_codes['invalid_parameters']), content_type='application/json')


		# security checks
		if not publication.is_published():
			raise SuspiciousOperation('Attempt to comment unpublished publication.')


		try:
			send_notification_about_new_call_request(
				request,
				tid,
				publication,
				params['phone_number'],
				params.get('name', '') # not required
			)
		except InvalidArgument:
			return HttpResponseBadRequest(
				json.dumps(self.post_codes['invalid_parameters']), content_type='application/json')


		return HttpResponse(
			json.dumps(self.post_codes['Ok']), content_type="application/json")