#coding=utf-8
import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods

from collective.methods.request_data_getters import GET_parameter
from core.markers_servers import MARKERS_SERVERS
from core.markers_servers.exceptions import TooBigTransaction
from core.markers_servers.utils import Point
from core.publications.constants import OBJECTS_TYPES



def get_markers_etag(request):
	# Немає необхідності обробляти виключні ситуації.
	# В найгіршому випадку, etag просто не буде сформовано.
	tid = int(GET_parameter(request, 'tid'))
	viewport_ne = GET_parameter(request, 'ne')
	viewport_sw = GET_parameter(request, 'sw')

	if tid not in OBJECTS_TYPES.values():
		raise ValueError('Invalid tid.')

	ne_lat, ne_lng = viewport_ne.split(':')
	sw_lat, sw_lng = viewport_sw.split(':')
	ne = Point(ne_lat, ne_lng)
	sw = Point(sw_lat, sw_lng)

	server = MARKERS_SERVERS.get(tid, None)
	if server is None:
		raise Exception('Potentially missed tid in MARKERS_SERVERS.')
	return server.viewport_hash(ne, sw)


def parse_houses_filters(request):
	"""
	Формує об’єкт фільтрів для домів із параметрів, переданих в запиті.
	Не перевіряє передані дані на коректність.
	Перевірка відводиться функції фільтрування, яка безпосередньо володіє контекстом.
	"""
	operation_sid = request.GET.get('operation_sid')
	if operation_sid is None:
		raise ValueError('Operation sid is required.')

	operation_sid = int(operation_sid)
	conditions = {
		'operation_sid': operation_sid
	}

	if operation_sid == 0: # sale
		#-- price
		price_from = request.GET.get('price_from')
		if price_from is not None:
			conditions['price_from'] = int(price_from)

		price_to = request.GET.get('price_to')
		if price_to is not None:
			conditions['price_to'] = int(price_to)

		currency_sid = request.GET.get('currency_sid')
		if currency_sid is not None:
			conditions['currency_sid'] = int(currency_sid)

		#-- market type
		if 'new_buildings' in request.GET:
			conditions['new_buildings'] = True

		if 'secondary_market' in request.GET:
			conditions['secondary_market'] = True

		#-- rooms count
		rooms_count_from = request.GET.get('rooms_count_from')
		if rooms_count_from is not None:
			conditions['rooms_count_from'] = int(rooms_count_from)

		rooms_count_to = request.GET.get('rooms_count_to')
		if rooms_count_to is not None:
			conditions['rooms_count_to'] = int(rooms_count_to)

		#-- floors count
		floors_count_from = request.GET.get('floors_count_from')
		if floors_count_from is not None:
			conditions['floors_count_from'] = int(floors_count_from)

		floors_count_to = request.GET.get('floors_count_to')
		if floors_count_to is not None:
			conditions['floors_count_to'] = int(floors_count_to)

		#-- facilities
		if 'electricity' in request.GET:
			conditions['electricity'] = True

		if 'gas' in request.GET:
			conditions['gas'] = True

		if 'hot_water' in request.GET:
			conditions['hot_water'] = True

		if 'cold_water' in request.GET:
			conditions['cold_water'] = True

		if 'sewerage' in request.GET:
			conditions['sewerage'] = True

		heating_type_sid = request.GET.get('heating_type_sid')
		if heating_type_sid is not None:
			conditions['heating_type_sid'] = int(heating_type_sid)

	elif operation_sid == 1: # rent
		#-- price
		price_from = request.GET.get('price_from')
		if price_from is not None:
			conditions['price_from'] = int(price_from)

		price_to = request.GET.get('price_to')
		if price_to is not None:
			conditions['price_to'] = int(price_to)

		currency_sid = request.GET.get('currency_sid')
		if currency_sid is not None:
			conditions['currency_sid'] = int(currency_sid)

		#-- params
		if 'family' in request.GET:
			conditions['family'] = True

		if 'foreigners' in request.GET:
			conditions['foreigners'] = True

		#-- persons count
		persons_count_from = request.GET.get('persons_count_from')
		if persons_count_from is not None:
			conditions['persons_count_from'] = int(persons_count_from)

		persons_count_to = request.GET.get('persons_count_to')
		if persons_count_to is not None:
			conditions['persons_count_to'] = int(persons_count_to)

		#-- facilities
		if 'electricity' in request.GET:
			conditions['electricity'] = True

		if 'gas' in request.GET:
			conditions['gas'] = True

		if 'hot_water' in request.GET:
			conditions['hot_water'] = True

		if 'cold_water' in request.GET:
			conditions['cold_water'] = True

	return conditions


get_codes = {
	'invalid_tid': {
		'code': 1,
	},
	'invalid_coordinates': {
		'code': 2,
	},
	'invalid_conditions': {
		'code': 3,
	},
    'too_big_query': {
		'code': 4,
	},
}
@require_http_methods('GET')
# @condition(etag_func=get_markers_etag) # todo: enable me back
def get_markers(request):
	try:
		tid = int(GET_parameter(request, 'tid'))
	except ValueError:
		return HttpResponseBadRequest(
			json.dumps(get_codes['invalid_tid']), content_type='application/json')

	if tid not in OBJECTS_TYPES.values():
		return HttpResponseBadRequest(
			json.dumps(get_codes['invalid_tid']), content_type='application/json')

	try:
		viewport_ne = GET_parameter(request, 'ne')
		viewport_sw = GET_parameter(request, 'sw')
	except ValueError:
		return HttpResponseBadRequest(
			json.dumps(get_codes['invalid_coordinates']), content_type='application/json')

	ne_lat, ne_lng = viewport_ne.split(':')
	sw_lat, sw_lng = viewport_sw.split(':')
	ne = Point(ne_lat, ne_lng)
	sw = Point(sw_lat, sw_lng)


	try:
		if tid == OBJECTS_TYPES.house():
			conditions = parse_houses_filters(request)
		else:
			raise ValueError('Invalid tid.')

	except ValueError:
		return HttpResponseBadRequest(
			json.dumps(get_codes['invalid_conditions']), content_type='application/json')


	server = MARKERS_SERVERS.get(tid, conditions)
	if server is None:
		raise Exception('Potentially missed tid in MARKERS_SERVERS.')

	try:
		markers_briefs = server.markers(ne, sw, conditions)
		return HttpResponse(json.dumps(markers_briefs), content_type='application/json')

	except TooBigTransaction:
		return HttpResponseBadRequest(
			json.dumps(get_codes['too_big_query']), content_type='application/json')
	except ValueError:
		return HttpResponseBadRequest(
			json.dumps(get_codes['invalid_coordinates']), content_type='application/json')