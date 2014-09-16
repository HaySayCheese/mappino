#coding=utf-8
from django.views.generic import View

from apps.main.api.markers.utils import *
from collective.exceptions import InvalidArgument
from collective.http.responses import HttpJsonResponseBadRequest, HttpJsonResponse
from core.markers_handler import SegmentsIndex
from core.markers_handler.exceptions import TooBigTransaction
from core.publications.constants import OBJECTS_TYPES


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

	filters_parsers =  {
		OBJECTS_TYPES.flat(): parse_flats_filters,
		OBJECTS_TYPES.house(): parse_houses_filters,
		OBJECTS_TYPES.room(): parse_rooms_filters,

		OBJECTS_TYPES.land(): parse_lands_filters,
		OBJECTS_TYPES.garage(): parse_garages_filters,

		OBJECTS_TYPES.office(): parse_offices_filters,
		OBJECTS_TYPES.trade(): parse_trades_filters,
		OBJECTS_TYPES.warehouse(): parse_warehouses_filters,
		OBJECTS_TYPES.business(): parse_businesses_filters,
		OBJECTS_TYPES.catering(): parse_caterings_filters,
	}


	@classmethod
	def get(cls, request, *args):
		if 'zoom' in request.GET:
			return cls.__markers_count_per_segment(request)

		return cls.__markers(request)


	@classmethod
	def __markers_count_per_segment(cls, request):
		# todo: add last modified header for a 5m

		try:
			tid = int(request.GET['tid'])
			if not tid in OBJECTS_TYPES.values():
				raise ValueError()

		except (IndexError, ValueError):
			return HttpJsonResponseBadRequest(cls.get_codes['invalid_tid'])


		try:
			viewport_ne = request.GET['ne']
			viewport_sw = request.GET['sw']

		except IndexError:
			return HttpJsonResponseBadRequest(cls.get_codes['invalid_coordinates'])

		ne_lat, ne_lng = viewport_ne.split(':')
		ne_lat, ne_lng = float(ne_lat), float(ne_lng)

		sw_lat, sw_lng = viewport_sw.split(':')
		sw_lat, sw_lng = float(sw_lat), float(sw_lng)


		try:
			zoom = int(request.GET['zoom'])
		except (IndexError, ValueError):
			return HttpJsonResponseBadRequest(cls.get_codes['invalid_coordinates'])

		conditions = (cls.filters_parsers[tid])(request)
		count = SegmentsIndex.estimate_count(tid, ne_lat, ne_lng, sw_lat, sw_lng, zoom, conditions)
		return HttpJsonResponse(count)


	@classmethod
	def __markers(cls, request):
		# todo: add last modified header for a 5m

		try:
			tid = int(request.GET['tid'])
			if not tid in OBJECTS_TYPES.values():
				raise ValueError()

		except (IndexError, ValueError):
			return HttpJsonResponseBadRequest(cls.get_codes['invalid_tid'])


		try:
			viewport_ne = request.GET['ne']
			viewport_sw = request.GET['sw']

		except IndexError:
			return HttpJsonResponseBadRequest(cls.get_codes['invalid_coordinates'])

		try:
			ne_lat, ne_lng = viewport_ne.split(':')
			sw_lat, sw_lng = viewport_sw.split(':')

			ne_lat = float(ne_lat)
			ne_lng = float(ne_lng)
			sw_lat = float(sw_lat)
			sw_lng = float(sw_lng)

		except ValueError:
			return HttpJsonResponseBadRequest(cls.get_codes['invalid_coordinates'])


		try:
			conditions = (cls.filters_parsers[tid])(request)
			return HttpJsonResponse(
				SegmentsIndex.markers(tid, ne_lat, ne_lng, sw_lat, sw_lng, conditions))

		except TooBigTransaction:
			return HttpJsonResponseBadRequest(cls.get_codes['too_big_query'])
		except InvalidArgument:
			return HttpJsonResponseBadRequest(cls.get_codes['invalid_coordinates'])