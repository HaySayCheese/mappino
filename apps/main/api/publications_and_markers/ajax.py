# coding=utf-8
import json

from django.views.generic import View

from apps.main.api.publications_and_markers.utils import *
from collective.decorators.ajax import json_response, json_response_bad_request, json_response_not_found
from collective.exceptions import InvalidArgument
from collective.http.responses import HttpJsonResponseBadRequest, HttpJsonResponse, HttpJsonResponseNotFound
from collective.methods.request_data_getters import angular_post_parameters
from core.claims.classes import ClaimsManager
from core.markers_index import SegmentsIndex
from core.markers_index.exceptions import TooBigTransaction
from core.publications import formatters
from core.publications.constants import HEAD_MODELS, OBJECTS_TYPES


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

    filters_parsers = {
        OBJECTS_TYPES.flat(): parse_flats_filters,
        OBJECTS_TYPES.house(): parse_houses_filters,
        OBJECTS_TYPES.room(): parse_rooms_filters,

        OBJECTS_TYPES.land(): parse_lands_filters,
        OBJECTS_TYPES.garage(): parse_garages_filters,

        OBJECTS_TYPES.office(): parse_offices_filters,
        OBJECTS_TYPES.trade(): parse_trades_filters,
        OBJECTS_TYPES.warehouse(): parse_warehouses_filters,
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
    def __markers_briefs(cls, params):
        """
        :returns:
            HttpJsonResponse with briefs for every received object type and viewport coords (if request was handled OK), or
            HttpJsonResponse with error code (if request was not handled properly).
        """
        try:
            ne_lat, \
            ne_lng, \
            sw_lat, \
            sw_lng = cls.parse_viewport_coordinates(params)
        except ValueError:
            return HttpJsonResponseBadRequest(cls.get_codes['invalid_coordinates'])


        try:
            tids_panels_and_filters = cls.parse_tids_panels_and_filters(params)
        except ValueError:
            return HttpJsonResponseBadRequest(cls.get_codes['invalid_tids'])


        # by default, markers are shown on a 14 zoom level.
        # at this point zoom parameter received from the client will be ignored.
        zoom = 14

        # all markers should be displayed on a same viewport coordinates,
        # so we can calculate and prepare it only once per all requested object types.
        ne_segment_x, \
        ne_segment_y, \
        sw_segment_x, \
        sw_segment_y = SegmentsIndex.normalize_viewport_coordinates(ne_lat, ne_lng, sw_lat, sw_lng, zoom)

        # we need to prevent duplicates in output,
        # so we should exclude already used markers from every next iteration.
        # ids of different object types may be the same
        # (tables are different and sequences for ids are different too),
        # so we need to handle ids per tid.
        excluded_ids_per_tid = {
            tid: [] for tid, _, _ in tids_panels_and_filters
        }


        response = {}
        try:
            for tid, panel, filters in tids_panels_and_filters:
                # Generating of the filters objects.
                # This object is used to perform filtering based on parameters
                # that was specified on front-end.

                try:
                    filter_conditions = (cls.filters_parsers[tid])(filters)
                except OperationSIDParseError:
                    # In some cases operation type of some panels may be omitted by the front-end.
                    # (for example, if realty type was selected moment ago and no operation type was selected)
                    # In this case this panel should be ignored, but the rest panels should be processed.
                    continue


                # Generating of the briefs.
                # This method will also return ids (not hash ids) of the publications from the viewport.
                # This ids will be used on next iterations to exclude duplicates.
                briefs, used_ids = SegmentsIndex.markers(
                    tid, ne_segment_x, ne_segment_y, sw_segment_x, sw_segment_y, zoom,
                    filter_conditions, excluded_ids_per_tid[tid])

                if briefs:
                    response[panel] = briefs
                else:
                    response[panel] = {}

                # on the next iteration we need to receive only ids
                # that was not received on previous iterations
                # (prevent duplication)
                excluded_ids_per_tid[tid] += used_ids


        except TooBigTransaction:
            return HttpJsonResponseBadRequest(cls.get_codes['too_big_query'])
        except InvalidArgument:
            return HttpJsonResponseBadRequest(cls.get_codes['invalid_coordinates'])


        # seems to be ok
        return HttpJsonResponse(response)


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
            sw_lng = cls.parse_viewport_coordinates(params)
        except ValueError:
            return HttpJsonResponseBadRequest(cls.get_codes['invalid_coordinates'])


        try:
            tids_panels_and_filters = cls.parse_tids_panels_and_filters(params)
        except ValueError:
            return HttpJsonResponseBadRequest(cls.get_codes['invalid_tids'])


        try:
            zoom = int(params['zoom'])
        except (IndexError, ValueError):
            return HttpJsonResponseBadRequest(cls.get_codes['invalid_request'])


        # all markers should be displayed on a same viewport coordinates,
        # so we can calculate and prepare it only once per all requested object types.
        ne_segment_x, \
        ne_segment_y, \
        sw_segment_x, \
        sw_segment_y = SegmentsIndex.normalize_viewport_coordinates(ne_lat, ne_lng, sw_lat, sw_lng, zoom)


        # we need to prevent duplicates in output,
        # so we should exclude already used markers from every next iteration.
        # ids of different object types may be the same
        # (tables are different and sequences for ids are different too),
        # so we need to handle ids per tid.
        excluded_ids_per_tid = {
            tid: [] for tid, _, _ in tids_panels_and_filters
        }


        response = {}
        try:
            # Generating unique set of markers counters for all panels.
            # All the markers ids will be intersected to prevent counters duplication on front-end.
            for tid, panel, filters in tids_panels_and_filters:

                # Generating of the filters objects.
                # This object is used to perform filtering based on parameters
                # that was specified on front-end.
                filter_conditions = (cls.filters_parsers[tid])(filters)

                # Segments generation.
                # This method will also return ids (not hash ids) of the publications from the viewport.
                # This ids will be used on next iterations to exclude duplicates.
                segments, used_ids = SegmentsIndex.estimate_count(
                    tid, ne_segment_x, ne_segment_y, sw_segment_x, sw_segment_y, zoom,
                    filter_conditions, excluded_ids_per_tid[tid])

                if segments:
                    response[panel] = segments
                else:
                    response[panel] = {}

                # on the next iteration we need to receive only ids
                # that was not received on previous iterations
                # (prevent duplication)
                excluded_ids_per_tid[tid] += used_ids


        except TooBigTransaction:
            return HttpJsonResponseBadRequest(cls.get_codes['too_big_query'])
        except InvalidArgument:
            return HttpJsonResponseBadRequest(cls.get_codes['invalid_coordinates'])


        # seems to be ok
        return HttpJsonResponse(response)


    @staticmethod
    def parse_viewport_coordinates(params):
        """
        Parses viewport coordinates from the "params".

        :param params: object with all the request parameters.
        :type params: dict

        :returns:
            ne_lat, ne_lng, sw_lat, sw_lng in tuple.

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
    def parse_tids_panels_and_filters(params):
        """
        :type params: dict
        :param params: JSON object with request parameters.

        :returns:
            list of object types ids received from the request.

        :raises:
            ValueError even if one tid wil not pass validation.
        """

        parsed_tids_and_filters = []
        try:
            for filters in params['filters']:
                tid = int(filters['t_sid'])
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


class DetailedView(View):
    formatter = formatters.PublishedDataSource() # this is a description generator for the publications.

    class GetResponses(object):
        @staticmethod
        @json_response
        def ok(data):
            return {
                'code': 0,
                'message': 'OK',
                'data': data,
            }

        @staticmethod
        @json_response_bad_request
        def invalid_tid_hid():
            return {
                'code': 1,
                'message': 'Request contains invalid "tid" or "hid" or does not contains them at all.'
            }

        @staticmethod
        @json_response_not_found
        def no_such_publication():
            return {
                'code': 2,
                'message': 'There is no publication with exact id.'
            }

        @staticmethod
        @json_response
        def publication_is_unpublished():
            return {
                'code': 3,
                'message': 'This publication was unpublished.'
            }


    @classmethod
    def get(cls, request, *args):
        try:
            tid, hash_id = int(args[0]), args[1]
            model = HEAD_MODELS[tid]
        except (KeyError, ValueError):
            return cls.GetResponses.invalid_tid_hid()


        try:
            publication = model.queryset_by_hash_id(hash_id)\
                .only('for_sale', 'for_rent')\
                .prefetch_related('body')\
                .prefetch_related('sale_terms')\
                .prefetch_related('rent_terms')\
                [:1][0]
        except IndexError:
            return cls.GetResponses.no_such_publication()


        if not publication.is_published():
            return cls.GetResponses.publication_is_unpublished()


        data = cls.formatter.format(tid, publication)

        # todo: return favorites back
        return cls.GetResponses.ok(data)


class Claims(object):
    class List(View):
        class PostResponses(object):
            @staticmethod
            def ok():
                return HttpJsonResponse({
                    'code': 0,
                    'message': 'OK. Claim was accepted successfully.'
                })


            @staticmethod
            def empty_request():
                return HttpJsonResponseBadRequest({
                    'code': 1,
                    'message': 'Request does not contains any parameter. '
                               'It should provide "publication_tid", "publication_hid", '
                               '"claim_tid", "email" and "message".'
                })


            @staticmethod
            def invalid_publication_tid():
                return HttpJsonResponseBadRequest({
                    'code': 2,
                    'message': 'Request doesn\'t contains parameter "publication_tid", '
                               'or it is invalid. '
                })


            @staticmethod
            def invalid_publication_hid():
                return HttpJsonResponseBadRequest({
                    'code': 3,
                    'message': 'Request doesn\'t contains parameter "publication_hid", '
                               'or it is invalid. '
                })


            @staticmethod
            def invalid_claim_tid():
                return HttpJsonResponseBadRequest({
                    'code': 4,
                    'message': 'Request doesn\'t contains parameter "claim_tid", '
                               'or it is invalid. '
                })


            @staticmethod
            def invalid_user_email():
                return HttpJsonResponseBadRequest({
                    'code': 5,
                    'message': 'Request doesn\'t contains parameter "email", '
                               'or it is invalid. '
                })


            @staticmethod
            def publication_does_not_exists():
                return HttpJsonResponseNotFound({
                    'code': 6,
                    'message': 'Publication with received params does not exists.'
                })


        @classmethod
        def post(cls, request, *args):
            if not args:
                return cls.PostResponses.empty_request()

            try:
                publication_tid = int(args[0])
            except (IndexError, ValueError, ):
                return cls.PostResponses.invalid_publication_tid()

            try:
                publication_hid = args[1]
            except (IndexError, ):
                return cls.PostResponses.invalid_publication_hid()

            post_params = angular_post_parameters(request)
            try:
                claim_tid = int(post_params['claim_tid'])
            except (KeyError, ValueError):
                return cls.PostResponses.invalid_claim_tid()

            try:
                user_email = post_params['email']
            except (KeyError, ValueError):
                return cls.PostResponses.invalid_user_email()

            # optional params
            custom_message = post_params.get('message')


            try:
                ClaimsManager.claim(publication_tid, publication_hid, user_email, claim_tid, custom_message)
                return cls.PostResponses.ok()

            except ClaimsManager.InvalidPublicationTypeId:
                return cls.PostResponses.invalid_publication_tid()

            except ClaimsManager.InvalidUserEmail:
                return cls.PostResponses.invalid_user_email()

            except ClaimsManager.InvalidClaimTypeId:
                return cls.PostResponses.invalid_claim_tid()

            except ClaimsManager.PublicationDoesNotExists:
                return cls.PostResponses.publication_does_not_exists()