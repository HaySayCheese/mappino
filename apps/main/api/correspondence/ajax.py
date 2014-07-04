#coding=utf-8
import json

from django.http import HttpResponseBadRequest, HttpResponse
from django.views.generic import View

from apps.main.api.correspondence.utils import send_new_message_notification, send_new_call_request_notification
from collective.exceptions import InvalidArgument
from collective.methods.request_data_getters import angular_parameters
from core.publications.constants import HEAD_MODELS


class SendMessageFromClient(View):
	codes = {
		'ok': {
			'code': 0,
		},
		'invalid_publication_id': {
			'code': 1
		},
	    'invalid_parameters': {
		    'code': 2
	    }
	}

	def post(self, request, *args):
		"""
		Надсилає власнику оголошення повідомлення від зацікавелного клієнта @message на адресу @email.
		Якщо передано параметр @name - його буде використано в листі.
		"""
		try:
			tid, hash_hid = args[0].split(':')
			tid = int(tid)
		except (ValueError, IndexError):
			return HttpResponseBadRequest(json.dumps(
				self.codes['invalid_publication_id']), content_type='application/json')

		try:
			params = angular_parameters(request, ['email', 'message'])
		except ValueError:
			return HttpResponseBadRequest(json.dumps(
				self.codes['invalid_parameters']), content_type='application/json')

		message = params['message']
		client_email = params['email']
		client_name = params.get('name') # not required


		try:
			send_new_message_notification(request, tid, hash_hid, message, client_email, client_name)
		except InvalidArgument:
			return HttpResponseBadRequest(
				json.dumps(self.codes['invalid_parameters']), content_type='application/json')

		return HttpResponse(json.dumps(self.codes['ok']), content_type="application/json")



class SendCallRequestFromClient(View):
	codes = {
		'ok': {
			'code': 0,
		},
		'invalid_publication_id': {
			'code': 1
		},
	    'invalid_parameters': {
		    'code': 2
	    }
	}

	def post(self, request, *args):
		"""
		Надсилає власнику оголошення запит на зворотній дзвінок на номер @phone-number.
		Якщо передано параметр @name - його буде використано в повідомленні.
		"""
		try:
			tid, hash_hid = args[0].split(':')
			tid = int(tid)
		except ValueError:
			return HttpResponseBadRequest(json.dumps(
				self.codes['invalid_publication_id']), content_type='application/json')

		try:
			params = angular_parameters(request, ['phone_number'])
		except ValueError:
			return HttpResponseBadRequest(json.dumps(
				self.codes['invalid_parameters']), content_type='application/json')

		phone_number = params['phone_number']
		client_name = params.get('name') # not required


		try:
			send_new_call_request_notification(request, tid, hash_hid, phone_number, client_name)
		except InvalidArgument:
			return HttpResponseBadRequest(
				json.dumps(self.codes['invalid_parameters']), content_type='application/json')

		return HttpResponse(json.dumps(self.codes['ok']), content_type="application/json")