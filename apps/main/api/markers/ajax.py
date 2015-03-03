#coding=utf-8
import json

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
        'invalid_request': {
            'code': 5,
        }
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
    }


    @classmethod
    def get(cls, request, *args):
        # note:
        # User will almost never positioning his viewport on the same position twice,
        # and almost never will generate requests with the same viewport coordinates.
        # as a result - there is no need to add last modified header to this view or other cache.

        try:
            params = json.loads(request.GET.get('p', ''))
        except ValueError:
            # json decoder will throw value error on attempt to decode empty string
            return HttpJsonResponseBadRequest(cls.get_codes['invalid_request'])


        try:
            zoom = int(params['zoom'])
        except ValueError:
            return HttpJsonResponseBadRequest(cls.get_codes['invalid_request'])

        if zoom <= 14:
            return cls.__markers_count_per_segment(params)
        else:
            return cls.__markers_briefs(params)


    @classmethod
    def __markers_count_per_segment(cls, params):
        """
        :returns:
            HttpJsonResponse with estimate markers count for every received object type
            and viewport coordinates (if request was handled OK), or
            HttpJsonResponse with error code (if request was not handled properly).
        """
        try:
            ne_lat, \
            ne_lng, \
            sw_lat, \
            sw_lng = cls.__parse_viewport_coordinates(params)
        except ValueError:
            return HttpJsonResponseBadRequest(cls.get_codes['invalid_coordinates'])


        try:
            tids_and_filters = cls.__parse_tids_and_filters(params)
        except ValueError:
            return HttpJsonResponseBadRequest(cls.get_codes['invalid_tids'])


        try:
            zoom = int(params['zoom'])
        except (IndexError, ValueError):
            return HttpJsonResponseBadRequest(cls.get_codes['invalid_request'])


        try:
            response = {}
            already_present_ids = [] # list is more efficient here than the set.
                                     # all the received ids will be already unique.

            # Generating unique set of markers counters for all panels.
            # All the markers ids will be intersected to prevent counters duplication on front-end.
            for tid, panel, filters in tids_and_filters:

                # Generating of the filters objects.
                # This object is used to perform filtering based on parameters
                # that was spcified on front-end.
                filter_conditions = (cls.filters_parsers[tid])(filters)

                # Segments generation.
                # This method will also return ids (not hash ids) of the publications from the viewport.
                # This ids will be used on next iterations to exclude duplicates.
                segments, received_ids = SegmentsIndex.estimate_count(
                    tid, ne_lat, ne_lng, sw_lat, sw_lng, zoom, filter_conditions, already_present_ids)

                if segments:
                    response[panel] = segments

                # on the next iteration we need to receive only ids
                # that was not received on previous iterations
                already_present_ids += received_ids

        except TooBigTransaction:
            return HttpJsonResponseBadRequest(cls.get_codes['too_big_query'])
        except InvalidArgument:
            return HttpJsonResponseBadRequest(cls.get_codes['invalid_coordinates'])


        # seems to be ok
        return HttpJsonResponse(response)


    @classmethod
    def __markers_briefs(cls, params):
        """
        :returns:
            HttpJsonResponse with briefs for every receiced object type and viewport coords (if request was handled OK), or
            HttpJsonResponse with error code (if request was not handled properly).
        """
        try:
            ne_lat, \
            ne_lng, \
            sw_lat, \
            sw_lng = cls.__parse_viewport_coordinates(params)
        except ValueError:
            return HttpJsonResponseBadRequest(cls.get_codes['invalid_coordinates'])


        try:
            tids_and_filters = cls.__parse_tids_and_filters(params)
        except ValueError:
            return HttpJsonResponseBadRequest(cls.get_codes['invalid_tids'])


        try:
            response = {}
            already_present_ids = [] # list is more efficient here than the set.
                                     # all the received ids will be already unique.

            # Generating unique set of markers briefs for all panels.
            # All the markers ids will be intersected to prevent markers duplication on front-end.
            for tid, panel, filters in tids_and_filters:

                # Generating of the filters objects.
                # This object is used to perform filtering based on parameters
                # that was spcified on front-end.
                filter_conditions = (cls.filters_parsers[tid])(filters)

                # Generating of the briefs.
                # This method will also return ids (not hash ids) of the publications from the viewport.
                # This ids will be used on next iterations to exclude duplicates.
                briefs, received_ids = SegmentsIndex.markers(
                    tid, ne_lat, ne_lng, sw_lat, sw_lng, filter_conditions, already_present_ids)

                if briefs:
                    response[panel] = briefs

                # on the next iteration we need to receive only ids
                # that was not received on previous iterations
                already_present_ids += received_ids

        except TooBigTransaction:
            return HttpJsonResponseBadRequest(cls.get_codes['too_big_query'])
        except InvalidArgument:
            return HttpJsonResponseBadRequest(cls.get_codes['invalid_coordinates'])


        # seems to be ok
        return HttpJsonResponse(response)


    @staticmethod
    def __parse_viewport_coordinates(params):
        """
        :param params: JSON object (dict in this method) with request parameters.

        :returns:
            Parses request's params for viewport coordinates.
            Returns ne_lat, ne_lng, sw_lat, sw_lng in tuple.

        :raises:
            ValueError if request contains invalid data.
        """

        try:
            viewport = params['viewport']
            ne_lat = float(viewport['ne_lat'])
            ne_lng = float(viewport['ne_lng'])
            sw_lat = float(viewport['sw_lat'])
            sw_lng = float(viewport['sw_lng'])

        except (IndexError, ValueError):
            raise ValueError('Invalid viewport coordinates was received.')

        # seems to be ok
        return ne_lat, ne_lng, sw_lat, sw_lng


    @staticmethod
    def __parse_tids_and_filters(params):
        """
        :param params: JSON object (dict in this method) with request parameters.

        :returns:
            list of object types ids received from the request.

        :raises:
            ValueError even if one tid wil not pass validation.
        """

        parsed_tids_and_filters = []
        try:
            for filters in params['filters']:
                tid = int(filters['type_sid'])
                if tid not in OBJECTS_TYPES.values():
                    raise ValueError('Invalid type id received from the client, {}'.format(tid))

                panel = filters['panel']
                parsed_tids_and_filters.append(
                    (tid, panel, filters, ) # note: tuple here
                )

        except (IndexError, ValueError):
            raise ValueError('Invalid filters parameters was received.')

        # seems to be ok
        return parsed_tids_and_filters