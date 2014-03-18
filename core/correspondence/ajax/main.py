#coding=utf-8
import json

from django.http.response import HttpResponseBadRequest, HttpResponse
from django.views.generic import View

from collective.exceptions import InvalidArgument
from collective.methods.request_data_getters import angular_parameters
from core.correspondence import notifications_dispatcher


class NewMessage(View):
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
		Обробляє запит на додавання нового повідомлення для рієлтора.
		"""
		try:
			tid, hid = args[0].split(':')
			tid = int(tid)
			hid = int(hid)
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
			notifications_dispatcher.send_new_message_notification(tid, hid, message, client_email, client_name)
		except InvalidArgument:
			return HttpResponseBadRequest(json.dumps(
				self.codes['invalid_parameters']), content_type='application/json')
		return HttpResponse(json.dumps(self.codes['ok']), content_type="application/json")


class NewCallRequest(View):
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
		Обробляє запит на додавання запиту на зворотній дзвінок для рієлтора.
		"""
		try:
			tid, hid = args[0].split(':')
			tid = int(tid)
			hid = int(hid)
		except ValueError:
			return HttpResponseBadRequest(json.dumps(
				self.codes['invalid_publication_id']), content_type='application/json')

		try:
			params = angular_parameters(request, ['phone_number'])
		except ValueError:
			return HttpResponseBadRequest(json.dumps(
				self.codes['invalid_parameters']), content_type='application/json')

		phone_number = params['phone_number']
		client_name = params['name'] # not required

		try:
			notifications_dispatcher.send_new_call_request_notification(tid, hid, phone_number, client_name)
		except InvalidArgument:
			return HttpResponseBadRequest(json.dumps(
				self.codes['invalid_parameters']), content_type='application/json')
		return HttpResponse(json.dumps(self.codes['ok']), content_type="application/json")