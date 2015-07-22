# coding=utf-8
import json
from django.views.generic import View

from collective.exceptions import InvalidArgument
from collective.http.responses import HttpJsonResponseBadRequest, HttpJsonResponse, HttpJsonResponseNotFound
from collective.methods.request_data_getters import angular_post_parameters
from core.claims.classes import ClaimsManager
from core.markers_handler import SegmentsIndex
from core.markers_handler.exceptions import TooBigTransaction
from core.publications import classes
from core.publications.constants import HEAD_MODELS


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
                filter_conditions = (cls.filters_parsers[tid])(filters)


                # Generating of the briefs.
                # This method will also return ids (not hash ids) of the publications from the viewport.
                # This ids will be used on next iterations to exclude duplicates.
                briefs, used_ids = SegmentsIndex.markers(
                    tid, ne_segment_x, ne_segment_y, sw_segment_x, sw_segment_y, zoom,
                    filter_conditions, excluded_ids_per_tid[tid])

                if briefs:
                    response[panel] = briefs

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


class DetailedView(View):
    formatter = classes.PublishedDataSource() # this is a description generator for the publications.

    class GetResponses(object):
        @staticmethod
        def ok(data):
            return HttpJsonResponse({
                'code': 0,
                'message': 'OK',
                'data': data,
            })

        @staticmethod
        def invalid_tid_hid():
            return HttpJsonResponseBadRequest({
                'code': 1,
                'message': 'Request contains invalid "tid" or "hid" or does not contains them at all.'
            })

        @staticmethod
        def no_such_publication():
            return HttpJsonResponseNotFound({
                'code': 1,
                'message': 'There is no publication with exact id.'
            })

        @staticmethod
        def publication_is_unpublished():
            return HttpJsonResponse({
                'code': 2,
                'message': 'This publication was unpublished.'
            })


    def __init__(self):
        super(DetailedView, self).__init__()
        self.formatter = classes.PublishedDataSource()


    def get(self, request, *args):
        tid, hash_id = int(args[0]), args[1]

        try:
            model = HEAD_MODELS[tid]
        except KeyError:
            return self.GetResponses.invalid_tid_hid()

        try:
            publication = model.objects\
                .filter(hash_id=hash_id)\
                .only('for_sale', 'for_rent', 'body', 'sale_terms', 'rent_terms')[:1][0]
        except IndexError:
            return self.GetResponses.no_such_publication()

        # check if publication is published,
        # otherwise we must not show it
        if not publication.is_published():
            return self.GetResponses.publication_is_unpublished()



        description = self.formatter.format(tid, publication)

        # todo: return favorites back

        # # check if this publication is listed in customers favorites
        # description['added_to_favorites'] = False


        # try:
        #     customer = self.get_customer_queryset(request)[0]
        #     if Favorites.exist(customer.id, tid, hash_id):
        #         description['added_to_favorites'] = True
        # except IndexError:
        #     pass


        return self.GetResponses.ok(description)


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