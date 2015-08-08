# coding=utf-8
from django.core.exceptions import ObjectDoesNotExist
from apps.views_base import ModeratorsView
from collective.decorators.ajax import json_response, json_response_bad_request
from collective.methods.request_data_getters import angular_post_parameters
from core.moderators.models import PublicationsCheckQueue
from core.publications import formatters
from core.publications.constants import HEAD_MODELS


class NextPublicationView(ModeratorsView):
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


    @classmethod
    def get(cls, request):
        while True:
            record = PublicationsCheckQueue.get_next_record()
            if record is None:
                return cls.GetResponses.ok({}) # there are no publications to check


            try:
                model = HEAD_MODELS[record.publication_tid]
                publication = model.by_hash_id(
                    record.publication_hash_id, select_body=True, select_sale=True, select_rent=True)

            except ObjectDoesNotExist:
                record.delete()
                continue


            if not publication.is_published():
                record.delete()
                continue


            data = cls.formatter.format(record.publication_tid, publication)
            data['publication'] = {
                'tid': publication.tid,
                'hash_id': publication.hash_id,
            }
            return cls.GetResponses.ok(data)


        # todo: перевірити чи в привильному порядку віддаються оголошення


class PublicationAcceptOrRejectView(ModeratorsView):
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
            publication_id = angular_post_parameters(request, ['publication_id'])['publication_id']
            tid, hash_id = publication_id.split(':')
            tid = int(tid)

        except (ValueError, KeyError):
            return cls.PostResponses.invalid_parameters()


        try:
            record = PublicationsCheckQueue\
                .queryset_by_publication(tid, hash_id)\
                .only('publication_tid', 'publication_hash_id')\
                [0]
        except IndexError:
            return cls.PostResponses.invalid_parameters()


        operation = args[0]
        if operation not in ['accept', 'reject']:
            return cls.PostResponses.invalid_parameters()


        if operation == 'accept':
            record.accept()

        elif operation == 'reject':
            record.reject()


        return cls.PostResponses.ok()
