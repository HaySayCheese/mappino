#coding=utf-8
import json

from django.http.response import HttpResponseBadRequest
from django.views.generic import View

from collective.exceptions import InvalidArgument
from collective.methods.request_data_getters import angular_parameters
from core.correspondence.models import EventsThreads



class NewMessage(View):
	codes = {
		'invalid_publication_id': {
			'code': 1
		},
	    'invalid_parameters': {
		    'code': 2
	    }
	}

	def post(self, request, tid, hid):
		"""
		Обробляє запит на додавання нового повідомлення для рієлтора.
		"""
		try:
			tid = int(tid)
			hid = int(hid)
		except ValueError:
			return HttpResponseBadRequest(json.dumps(
				self.codes['invalid_publication_id']), content_type='application/json')

		try:
			params = angular_parameters(request, ['email', 'message'])
		except ValueError:
			return HttpResponseBadRequest(json.dumps(
				self.codes['invalid_parameters']), content_type='application/json')

		email = params['email']
		message = params['message']
		client_name = params['name']

		try:
			EventsThreads.add_message_from_client(tid, hid, email, message, client_name)
		except InvalidArgument:
			return HttpResponseBadRequest(json.dumps(
				self.codes['invalid_parameters']), content_type='application/json')