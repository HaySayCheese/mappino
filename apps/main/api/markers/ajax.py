#coding=utf-8
import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import View

from apps.main.api.markers.utils import parse_houses_filters, parse_flats_filters, parse_apartments_filters, \
	parse_cottages_filters, parse_rooms_filters, parse_trades_filters, parse_offices_filters, \
	parse_warehouses_filters, parse_businesses_filters, parse_caterings_filters, parse_garages_filters, \
	parse_lands_filters
from collective.exceptions import InvalidArgument
from core.markers_servers import MARKERS_SERVERS, MARKERS_PER_SEGMENT_COUNT_MANAGER
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


class Markers(View):
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


	@classmethod
	def get(cls, request, *args):
		if 'zoom' in request.GET:
			return cls.__markers_per_segment_count(request)
		else:
			return cls.__markers(request)


	@classmethod
	def __markers_per_segment_count(cls, request):
		# todo: add last modified header for a 5m

		try:
			tid = int(request.GET['tid'])
			if not tid in OBJECTS_TYPES.values():
				raise ValueError()

		except (IndexError, ValueError):
			return HttpResponseBadRequest(
				json.dumps(cls.get_codes['invalid_tid']), content_type='application/json')


		try:
			viewport_ne = request.GET['ne']
			viewport_sw = request.GET['sw']
		except IndexError:
			return HttpResponseBadRequest(
				json.dumps(cls.get_codes['invalid_coordinates']), content_type='application/json')

		ne_lat, ne_lng = viewport_ne.split(':')
		ne_lat, ne_lng = float(ne_lat), float(ne_lng)

		sw_lat, sw_lng = viewport_sw.split(':')
		sw_lat, sw_lng = float(sw_lat), float(sw_lng)


		try:
			zoom = int(request.GET['zoom'])
		except (IndexError, ValueError):
			return HttpResponseBadRequest(
				json.dumps(cls.get_codes['invalid_coordinates']), content_type='application/json')


		count = MARKERS_PER_SEGMENT_COUNT_MANAGER.estimate_count(tid, ne_lat, ne_lng, sw_lat, sw_lng, zoom)
		return HttpResponse(json.dumps(count), 'application/json')


	@classmethod
	def __markers(cls, request):
		# todo: add last modified header for a 5m

		try:
			tid = int(request.GET['tid'])
			if not tid in OBJECTS_TYPES.values():
				raise ValueError()

		except (IndexError, ValueError):
			return HttpResponseBadRequest(
				json.dumps(cls.get_codes['invalid_tid']), content_type='application/json')


		try:
			viewport_ne = request.GET['ne']
			viewport_sw = request.GET['sw']
		except IndexError:
			return HttpResponseBadRequest(
				json.dumps(cls.get_codes['invalid_coordinates']), content_type='application/json')

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
				json.dumps(cls.get_codes['too_big_query']), content_type='application/json')
		except InvalidArgument:
			return HttpResponseBadRequest(
				json.dumps(cls.get_codes['invalid_coordinates']), content_type='application/json')