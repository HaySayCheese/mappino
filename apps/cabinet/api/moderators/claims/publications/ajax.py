# coding=utf-8
from django.core.exceptions import ObjectDoesNotExist

from apps.views_base import ModeratorsView
from collective.decorators.ajax import json_response, json_response_bad_request
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
            return cls.GetResponses.invalid_parameters()


        if not publication.is_published():
            return cls.GetResponses.invalid_parameters()


        data = cls.formatter.format(tid, publication)
        data['claims'] = [
            {
                'hash_id': claim.hash_id,
                'date_reported': claim.date_reported.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'closed': claim.closed,
                'email': claim.mesage,
                'moderator_hash_id': claim.moderator.hash_id,
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


        operation = args[0]
        if operation not in ['accept', 'reject', 'hold']:
            return cls.PostResponses.invalid_parameters()


        if operation == 'accept':
            record.accept()

        elif operation == 'reject':
            record.reject()

        elif operation == 'hold':
            record.hold()

        else:
            return cls.PostResponses.ok()



# class PublicationsClaimsView(ModeratorsView):
#     class GetResponses(object):
#         @staticmethod
#         @json_response
#         def ok(claims):
#             def key(x):
#                 return '{tid}:{hash_id}'.format(tid=x.publication_tid, hash_id=x.publication_hash_id)
#
#
#             data = {}
#             for publication_id, claims_of_publication in itertools.groupby(claims, key):
#                 data[publication_id] = [
#                     {
#                         'hash_id': c.hash_id,
#                         'state_sid': c.state_sid,
#                         'date_reported': c.date_reported.strftime('%Y-%m-%dT%H:%M:%SZ'),
#
#                         'email': c.email,
#                         'message': c.message,
#                         'publication_tid': c.publication_tid,
#                         'publication_hash_id': c.publication_hash_id,
#
#                         'moderator': {
#                             'hash_id': c.moderator.hash_id,
#                             'first_name': c.moderator.first_name,
#                             'last_name': c.moderator.last_name,
#                         }
#                     }
#
#                     for c in claims_of_publication
#                 ]
#
#             return {
#                 'code': 0,
#                 'message': 'OK',
#                 'data': data
#             }
#
#
#         @staticmethod
#         @json_response_bad_request
#         def invalid_parameters():
#             return {
#                 'code': 0,
#                 'message': 'Request contains invalid parameters.'
#             }
#
#
#     @classmethod
#     def get(cls, request, *args):
#         try:
#             offset = int(request.GET.get('offset', '0'))
#             count = int(request.GET.get('count', '20'))
#
#             if count > 100:
#                 raise SuspiciousOperation()
#
#         except ValueError:
#             return cls.GetResponses.invalid_parameters()
#
#
#         if args[0] == 'opened': # operation
#             claims = cls.__get_opened_claims(request.user, offset, count)
#         else:
#             claims = cls.__get_archived_claims(request.user, offset, count)
#
#
#         return cls.GetResponses.ok(claims)
#
#
#
#     @classmethod
#     def __get_opened_claims(cls, moderator, offset=0, count=20):
#         base_pubs_query = PublicationsClaims.objects\
#             .filter(state_sid=PublicationsClaims.States.new)\
#             .distinct()\
#             .order_by('date_reported')\
#             .prefetch_related('moderator')\
#             .values_list('publication_tid', 'publication_hash_id')
#
#
#         owned_pubs_ids = base_pubs_query.filter(moderator_id=moderator.id)[offset:count]
#         if owned_pubs_ids:
#             # if "owned_pubs_ids" will contains no one element -
#             # then will be generated empty filter, and, as a result -
#             # query will return all the records from the table without filtering at all.
#             owned_claims_filter = Q()
#             for tid, hash_id in owned_pubs_ids:
#                 owned_claims_filter |= Q(publication_tid=tid, publication_hash_id=hash_id)
#
#             owned_claims = PublicationsClaims.objects.filter(owned_claims_filter)
#
#         else:
#             owned_claims = PublicationsClaims.objects.none()
#
#
#         owned_claims_count = len(owned_claims)
#         if owned_claims_count >= count:
#             return itertools.chain(owned_claims, PublicationsClaims.objects.none())
#
#
#         # There are not enough claims was selected for reaching needed "count".
#         # Selecting several more publications that are not owned by the moderator.
#         pubs_ids = base_pubs_query[offset:count-owned_claims_count]
#         if pubs_ids:
#             # if "pubs_ids" will contains no one element -
#             # then will be generated empty filter, and, as a result -
#             # query will return all the records from the table without filtering at all.
#             claims_filter = Q()
#             for tid, hash_id in pubs_ids:
#                 claims_filter |= Q(publication_tid=tid, publication_hash_id=hash_id)
#
#             # assign selected claims to current moderator
#             PublicationsClaims.objects.filter(claims_filter).update(moderator=moderator)
#
#
#             claims = PublicationsClaims.objects.filter(claims_filter)
#
#         else:
#             claims = PublicationsClaims.objects.none()
#
#         return itertools.chain(owned_claims, claims)
#
#
#     @classmethod
#     def __get_archived_claims(cls, moderator, offset=0, count=20):
#         pubs_ids = PublicationsClaims.objects\
#             .filter(state_sid=PublicationsClaims.States.processed)\
#             .distinct()\
#             .order_by('date_reported')\
#             .prefetch_related('moderator')\
#             .values_list('publication_tid', 'publication_hash_id')\
#             [offset:count]
#
#         if pubs_ids:
#             # if "pubs_ids" will contains no one element -
#             # then will be generated empty filter, and, as a result -
#             # query will return all the records from the table without filtering at all.
#             claims_filter = Q()
#             for tid, hash_id in pubs_ids:
#                 claims_filter |= Q(publication_tid=tid, publication_hash_id=hash_id)
#
#             # assign selected claims to current moderator
#             PublicationsClaims.objects.filter(claims_filter).update(moderator=moderator)
#
#
#             claims = PublicationsClaims.objects.filter(claims_filter)
#
#         else:
#             claims = PublicationsClaims.objects.none()
#
#         return itertools.chain(claims, PublicationsClaims.objects.none())