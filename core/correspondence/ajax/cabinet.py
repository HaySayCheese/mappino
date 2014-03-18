#coding=utf-8
import json

from django.http.response import HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.generic import View

from collective.decorators.views import login_required_or_forbidden
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


	@method_decorator(login_required_or_forbidden)
	def dispatch(self, *args, **kwargs):
		return super(NewMessage, self).dispatch(*args, **kwargs)


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
			params = angular_parameters(request, ['message'])
		except ValueError:
			return HttpResponseBadRequest(json.dumps(
				self.codes['invalid_parameters']), content_type='application/json')

		message = params['message']
		realtor_id = request.user.id

		try:
			EventsThreads.add_message_from_realtor(tid, hid, realtor_id, message)
		except InvalidArgument:
			return HttpResponseBadRequest(json.dumps(
				self.codes['invalid_parameters']), content_type='application/json')