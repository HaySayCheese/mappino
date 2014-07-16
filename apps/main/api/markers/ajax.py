#coding=utf-8
import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods, condition

from apps.main.api.markers.utils import parse_houses_filters, parse_flats_filters, parse_apartments_filters, \
	parse_cottages_filters, parse_rooms_filters, parse_trades_filters, parse_offices_filters, \
	parse_warehouses_filters, parse_businesses_filters, parse_caterings_filters, parse_garages_filters, \
	parse_lands_filters
from collective.exceptions import InvalidArgument
from collective.methods.request_data_getters import GET_parameter
from core.markers_servers import MARKERS_SERVERS
from core.markers_servers.servers import BaseMarkersManager
from core.markers_servers.classes import Point
from core.publications.constants import OBJECTS_TYPES


FILTERS_PARSERS =  {
	OBJECTS_TYPES.house(): parse_houses_filters,
	OBJECTS_TYPES.flat(): parse_flats_filters,
	OBJECTS_TYPES.apartments(): parse_apartments_filters,
	OBJECTS_TYPES.cottage(): parse_cottages_filters,
	OBJECTS_TYPES.room(): parse_rooms_filters,
	OBJECTS_TYPES.trade(): parse_trades_filters,
	OBJECTS_TYPES.office(): parse_offices_filters,
	OBJECTS_TYPES.warehouse(): parse_warehouses_filters,
	OBJECTS_TYPES.business(): parse_businesses_filters,
	OBJECTS_TYPES.catering(): parse_caterings_filters,
	OBJECTS_TYPES.garage(): parse_garages_filters,
	OBJECTS_TYPES.land(): parse_lands_filters,
}


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
@condition(etag_func=get_markers_etag)
def markers(request):
	# todo: rewrite in view style
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


	filters_parse_method = FILTERS_PARSERS.get(tid)
	if filters_parse_method is None:
		raise Exception('Potentially missed tid in FILTERS_PARSERS.')
	conditions = filters_parse_method(request)


	server = MARKERS_SERVERS.get(tid, conditions)
	if server is None:
		raise Exception('Potentially missed tid in MARKERS_SERVERS.')

	try:
		markers_briefs = server.markers(ne, sw, conditions)
		return HttpResponse(json.dumps(markers_briefs), content_type='application/json')

	except BaseMarkersManager.TooBigTransaction:
		return HttpResponseBadRequest(
			json.dumps(get_codes['too_big_query']), content_type='application/json')
	except InvalidArgument:
		return HttpResponseBadRequest(
			json.dumps(get_codes['invalid_coordinates']), content_type='application/json')