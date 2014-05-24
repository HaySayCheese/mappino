import json
import random

from apps.cabinet.api.classes import CabinetView
from collective.methods.request_data_getters import GET_parameter
from django.http.response import HttpResponseBadRequest, HttpResponse


class Stats(object):
	class PublicationsVisits(CabinetView):
		get_codes = {
			'invalid_params': {
				'code': 1
			}
		}


		def get(self, request, *args):
			if not args:
				return HttpResponseBadRequest('Not enough parameters.')

			tid, hid = args[0].split(':')
			tid = int(tid)
			hid = int(hid)

			try:
				count = int(GET_parameter(request, 'count'))
			except ValueError:
				return HttpResponseBadRequest(json.dumps(
					self.get_codes['invalid_params']), content_type='application/json')


			if count not in [7, 14, 30]:
				return HttpResponseBadRequest(json.dumps(
					self.get_codes['invalid_params']), content_type='application/json')


			l = [
				{
				'date': '2014-05-{0}'.format(i),
				'views': random.randint(10, 30),
				'contacts_requests': random.randint(1, 30),
				} for i in xrange(20)
			]

			return HttpResponse(json.dumps(l), content_type='application/json')