# coding=utf-8
from django.core.exceptions import ObjectDoesNotExist

from apps.views_base import ModeratorsView
from collective.decorators.ajax import json_response, json_response_bad_request
from collective.methods.request_data_getters import angular_post_parameters
from core.moderators.models import PublicationsCheckQueue
from core.publications import formatters
from core.publications.constants import HEAD_MODELS



class NextPublicationToCheckView(ModeratorsView):
    class GetResponses(object):
        @staticmethod
        @json_response
        def ok(tid, hash_id):
            return {
                'code': 0,
                'message': 'OK',
                'data': {
                    'publication': {
                        'tid': tid,
                        'hash_id': hash_id,
                    }
                }
            }


        @staticmethod
        @json_response
        def no_publications_to_check():
            return {
                'code': 0,
                'message': 'OK',
                'data': None
            }


    @classmethod
    def get(cls, request, *args):
        while True:
            check_record = PublicationsCheckQueue.next_record(request.user)
            if check_record:
                # check if publication exists
                model = HEAD_MODELS[check_record.publication_tid]
                if model.objects.filter(hash_id=check_record.publication_hash_id).count() > 0:
                    return cls.GetResponses.ok(check_record.publication_tid, check_record.publication_hash_id)

                else:
                    # In some cases publication may be already deleted from the database,
                    # but reference to it may still exists.
                    #
                    # If this method will return broken reference to the client - it will receive 404 on the next step,
                    # but client will be unavailable to skip this broken reference,
                    # because this method will continue to return this broken reference until it is in the database.
                    #
                    # So, if reference is recognized as broken - it should be deleted from the check queue,
                    # and other reference should be processed.
                    check_record.delete()

            else:
                return cls.GetResponses.no_publications_to_check()



class PublicationView(ModeratorsView):
    formatter = formatters.PublishedDataSource()


    class GetResponses(object):
        @staticmethod
        @json_response
        def ok(data):
            return {
                'code': 0,
                'message': 'OK',
                'data': data
            }


        @staticmethod
        @json_response_bad_request
        def invalid_parameters():
            return {
                'code': 1,
                'message': 'Request does not contains valid parameters or one of them is incorrect.'
            }


        @staticmethod
        @json_response
        def no_such_publication():
            return {
                'code': 2,
                'message': 'No such publications.'
            }


    @classmethod
    def get(cls, request, *args):
        try:
            tid, hash_id = args[0], args[1]
            tid = int(tid)

        except (IndexError, ValueError, KeyError):
            return cls.GetResponses.invalid_parameters()


        try:
            check_record = PublicationsCheckQueue.objects.get(publication_tid=tid, publication_hash_id=hash_id)
            publication = check_record.publication
        except ObjectDoesNotExist:
            return cls.GetResponses.no_such_publication()


        if not publication.is_published():
            return cls.GetResponses.invalid_parameters()


        data = cls.formatter.format(tid, publication)
        data['claims'] = [
            {
                'hash_id': claim.hash_id,
                'date_reported': claim.date_reported.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'closed': claim.closed,
                'email': claim.email,
                'message': claim.message,
                'moderator_name': claim.moderator.full_name() if claim.moderator else None,
                'moderator_notice': claim.moderator_notice,

            } for claim in check_record.claims()
        ]
        return cls.GetResponses.ok(data)



class PublicationAcceptRejectOrHoldView(ModeratorsView):
    class PostResponses(object):
        @staticmethod
        @json_response
        def ok():
            return {
                'code': 0,
                'message': 'OK',
            }


        @staticmethod
        @json_response_bad_request
        def invalid_parameters():
            return {
                'code': 1,
                'message': 'Requests contains invalid parameters.'
            }


    @classmethod
    def post(cls, request, *args):
        try:
            tid, hash_id = args[0], args[1]
            tid = int(tid)

        except (IndexError, ValueError, KeyError):
            return cls.PostResponses.invalid_parameters()

        try:
            record = PublicationsCheckQueue.objects.by_tid_and_hash_id(tid, hash_id)[:1][0]
        except IndexError:
            return cls.PostResponses.invalid_parameters()


        operation = args[2]
        if operation not in ['accept', 'reject', 'hold']:
            return cls.PostResponses.invalid_parameters()


        if operation == 'accept':
            record.accept(request.user)

        elif operation == 'reject':
            message = angular_post_parameters(request).get('message')
            record.reject(request.user, message)

        elif operation == 'hold':
            record.hold(request.user)


        return cls.PostResponses.ok()



# class ClaimsNotices(ModeratorsView):
#
#
#     @classmethod
#     def