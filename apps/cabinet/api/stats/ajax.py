import json

from datetime import timedelta
from django.utils.timezone import now
from django.http.response import HttpResponseBadRequest, HttpResponse
from django.views.decorators.cache import cache_control

from apps.cabinet.api.stats.ga import auth
from apps.classes import CabinetView
from collective.methods.request_data_getters import GET_parameter


class Stats(object):
	class PublicationsVisits(CabinetView):
		get_codes = {
			'invalid_params': {
				'code': 1
			}
		}


		@cache_control(must_revalidate=True, max_age=(now() + timedelta(days=1)).replace(hour=0,minute=0,second=0))
		def get(self, request, *args):
			"""
			:param args:
				args[0]: tid - id the publication's type.
				args[1]: hid - id of the publication's head record.

			:param request:
				count: (int) - count of days in output data.
				May be equal to 7, 14, and 31.

			:return:
				Returns JSON-response with publications views and call_requests.

			CACHE_CONTROL:
				next day at 00:00
			"""
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


			current_date = now()
			data = [
				{
					'date': (current_date - timedelta(days=i)).strftime('%Y-%m-%dT00:00:00Z'),
				    'views': 0,
				    'contacts_requests': 0,
				} for i in xrange(count)
			]


			service = auth.initialize_service()
			views_data = service.data().ga().get(
				ids='ga:86963950',
				start_date = (current_date - timedelta(days=count)).strftime('%Y-%m-%d'),
				end_date = current_date.strftime('%Y-%m-%d'),
				metrics='ga:totalEvents',
				dimensions='ga:eventCategory,'
				           'ga:eventLabel,'
				           'ga:eventAction,'
				           'ga:date',
				filters='ga:eventCategory==publication:dialog:detailed;'
				        'ga:eventAction==data_requested;'
				        'ga:eventLabel=={0}:{1}'.format(tid, hid),
			    fields='rows'
			).execute()

			if 'rows' in views_data: # data requests may be absent at all
				for contacts_record in views_data['rows']:
					for data_record in data:
						date = contacts_record[3]
						views_date = ''.join([date[:4], '-', date[4:6], '-', date[6:8]])

						# pudb.set_trace()
						if views_date in data_record['date']:
							data_record['views'] = int(contacts_record[4])


			contacts_data = service.data().ga().get(
				ids='ga:86963950',
				start_date = (current_date - timedelta(days=count)).strftime('%Y-%m-%d'),
				end_date = current_date.strftime('%Y-%m-%d'),
				metrics='ga:totalEvents',
				dimensions='ga:eventCategory,'
				           'ga:eventLabel,'
				           'ga:eventAction,'
				           'ga:date',
				filters='ga:eventCategory==publication:dialog:detailed;'
				        'ga:eventAction==contacts_requested;'
				        'ga:eventLabel==0:4',
			    fields='rows'
			).execute()

			if 'rows' in contacts_data: # call requests may be absent at all
				for contacts_record in contacts_data['rows']:
					for data_record in data:
						date = contacts_record[3]
						views_date = ''.join([date[:4], '-', date[4:6], '-', date[6:8]])

						if views_date in data_record['date']:
							data_record['contacts_requests'] = int(contacts_record[4])


			return HttpResponse(json.dumps(data), content_type='application/json')