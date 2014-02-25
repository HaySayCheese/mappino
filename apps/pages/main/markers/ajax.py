#coding=utf-8
import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods, condition

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



get_codes = {
	'invalid_tid': {
		'code': 1,
	},
	'invalid_coordinates': {
		'code': 2,
	},
    'too_big_query': {
		'code': 3,
	},
}
@require_http_methods('GET')
@condition(etag_func=get_markers_etag)
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
		server = MARKERS_SERVERS.get(tid, None)
		if server is None:
			raise Exception('Potentially missed tid in MARKERS_SERVERS.')
		return HttpResponse(json.dumps(server.markers(ne, sw)), content_type='application/json')

	except TooBigTransaction:
		return HttpResponse(json.dumps(get_codes['too_big_query']), content_type='application/json')