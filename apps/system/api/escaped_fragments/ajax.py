from collective.decorators.ajax import json_response, json_response_bad_request
from core.publications.constants import HEAD_MODELS
from django.views.generic import View


class GetPublications(View):

    class GetResponses(object):

        @staticmethod
        @json_response
        def ok(published_publications):
            return {
                'code': 0,
                'message': 'OK',
                'data': published_publications,
            }

        @staticmethod
        @json_response_bad_request
        def invalid_parameters():
            return {
                'code': 1,
                'message': 'Request does not contains valid parameters or one of them is incorrect.'
            }


    @classmethod
    def get(cls, request):
        hash_ids = []
        for tid_model in HEAD_MODELS.keys():
            publications_query_set = HEAD_MODELS.get(tid_model).objects.exclude(published=None)
            for published_publication in publications_query_set:
                hash_ids.append([tid_model, published_publication.hash_id])
        return cls.GetResponses.ok(hash_ids)