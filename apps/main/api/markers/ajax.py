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
        'invalid_tids': {
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
        # note:
        # User will almost never positioning his viewport on the same position twice,
        # and almost never will generate requests with the same viewport coordinates.
        # as a result - there is no need to add last modified header to this view.

        if 'zoom' in request.GET:
            return cls.__markers_count_per_segment(request)
        else:
            return cls.__markers_briefs(request)


    @classmethod
    def __markers_count_per_segment(cls, request):
        """
        :returns:
            HttpJsonResponse with estimate markers count for every receiced object type
            and viewport coords (if request was handled OK), or
            HttpJsonResponse with error code (if request was not handled properly).
        """
        try:
            ne_lat, \
            ne_lng, \
            sw_lat, \
            sw_lng = cls.__parse_viewport_coordinates(request)
        except ValueError:
            return HttpJsonResponseBadRequest(cls.get_codes['invalid_coordinates'])


        try:
            tids = cls.__parse_object_types_ids(request)
        except ValueError:
            return HttpJsonResponseBadRequest(cls.get_codes['invalid_tids'])


        try:
            zoom = int(request.GET['zoom'])
        except (IndexError, ValueError):
            return HttpJsonResponseBadRequest(cls.get_codes['invalid_coordinates'])


        try:
            response = {}
            for tid in tids:
                filter_conditions = (cls.filters_parsers[tid])(request)
                response[tid] = SegmentsIndex.estimate_count(tid, ne_lat, ne_lng, sw_lat, sw_lng, zoom, filter_conditions)

        except TooBigTransaction:
            return HttpJsonResponseBadRequest(cls.get_codes['too_big_query'])
        except InvalidArgument:
            return HttpJsonResponseBadRequest(cls.get_codes['invalid_coordinates'])


        # seems to be ok
        return HttpJsonResponse(count)


    @classmethod
    def __markers_briefs(cls, request):
        """
        :returns:
            HttpJsonResponse with briefs for every receiced object type and viewport coords (if request was handled OK), or
            HttpJsonResponse with error code (if request was not handled properly).
        """
        try:
            ne_lat, \
            ne_lng, \
            sw_lat, \
            sw_lng = cls.__parse_viewport_coordinates(request)
        except ValueError:
            return HttpJsonResponseBadRequest(cls.get_codes['invalid_coordinates'])


        try:
            tids = cls.__parse_object_types_ids(request)
        except ValueError:
            return HttpJsonResponseBadRequest(cls.get_codes['invalid_tids'])


        try:
            response = {}
            for tid in tids:
                filter_conditions = (cls.filters_parsers[tid])(request)
                response[tid] = SegmentsIndex.markers(tid, ne_lat, ne_lng, sw_lat, sw_lng, filter_conditions)

        except TooBigTransaction:
            return HttpJsonResponseBadRequest(cls.get_codes['too_big_query'])
        except InvalidArgument:
            return HttpJsonResponseBadRequest(cls.get_codes['invalid_coordinates'])


        # seems to be ok
        return HttpJsonResponseBadRequest(cls.get_codes['invalid_tids'])


        @staticmethod
        def __parse_viewport_coordinates(request):
            """
            :returns:
                Parses request for viewport coordinates.
                Returns ne_lat, ne_lng, sw_lat, sw_lng in tuple

            :raises:
                ValueError if request contains ivalid data.
            """

            try:
                viewport_ne = request.GET['ne']
                viewport_sw = request.GET['sw']

                ne_lat, ne_lng = viewport_ne.split(':')
                sw_lat, sw_lng = viewport_sw.split(':')

                ne_lat = float(ne_lat)
                ne_lng = float(ne_lng)
                sw_lat = float(sw_lat)
                sw_lng = float(sw_lng)

            except (IndexError, ValueError):
                raise ValueError('Invalid viewport coordinates was received.')

            # seems to be ok
            return ne_lat, ne_lng, sw_lat, sw_lng


        @staticmethod
        def __parse_object_types_ids(request):
            """
            :returns:
                list of object types ids received from the request.

            :raises:
                ValueError even if one tid wil not pass validation.
            """
            tids = request.GET.get('tids', '').split(',')
            if not tids:
                raise ValueError('No one object type id was received.')

            # validation
            for tid in tids:
                # If ValueError will be genrated after the next line - it's OK, no need to double check for error.
                # This method raises ValueError in error cases.
                tid = int(tid)

                if tid not in OBJECTS_TYPES.values():
                    raise ValueError('Invalid type id received from the client, {}'.format(tid))

            # seems to be ok
            return tids