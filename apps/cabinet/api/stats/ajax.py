import json

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


			return HttpResponse(json.dumps([
				{
				'date': '2014-05-21T10:15:00Z',
				'views': 10,
				'contacts_requests': 5,
				},
			    {
				'date': '2014-05-22T10:15:00Z',
				'views': 14,
				'contacts_requests': 6,
				},
			    {
				'date': '2014-05-24T10:15:00Z',
				'views': 18,
				'contacts_requests': 9,
				}
			]), content_type='application/json')