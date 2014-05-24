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


			# l = [
			# 	{
			# 	'date': '2014-05-{0}'.format(i),
			# 	'views': random.randint(1, 30),
			# 	'contacts_requests': 5,
			# 	}
			# ]

			return HttpResponse(json.dumps([
				{
				'date': '2014-05-21',
				'views': 10,
				'contacts_requests': 5,
				},
			    {
				'date': '2014-05-22',
				'views': 14,
				'contacts_requests': 6,
				},
			    {
				'date': '2014-05-23',
				'views': 18,
				'contacts_requests': 9,
				},

			     {
				'date': '2014-05-24',
				'views': 14,
				'contacts_requests': 6,
				},
			    {
				'date': '2014-05-25',
				'views': 18,
				'contacts_requests': 9,
				},

			     {
				'date': '2014-05-26',
				'views': 14,
				'contacts_requests': 6,
				},
			    {
				'date': '2014-05-27',
				'views': 18,
				'contacts_requests': 9,
				},
			    {
				'date': '2014-05-28',
				'views': 18,
				'contacts_requests': 9,
				},
			    {
				'date': '2014-05-29',
				'views': 18,
				'contacts_requests': 9,
				},
			]), content_type='application/json')