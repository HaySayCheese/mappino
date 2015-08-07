# coding=utf-8
from django.http.response import Http404
from django.views.generic import View
from collective.decorators.ajax import json_response
from collective.methods.request_data_getters import angular_parameters
from core.claims.models import PublicationsClaims
from core.publications.constants import HEAD_MODELS


class ClaimsView(View):
    class PostResponses(object):
        @staticmethod
        @json_response
        def ok():
            return {
                'code': 0,
                'message': 'OK',
            }


        @staticmethod
        @json_response
        def invalid_params():
            return {
                'code': 1,
                'message': 'Request contains invalid parameters.',
            }


        @staticmethod
        @json_response
        def publication_does_not_exists():
            return {
                'code': 2,
                'message': 'Publication does not exists.',
            }


    @classmethod
    def post(cls, request, *args):
        # there is no need to catch exceptions
        #
        tid = int(args[0])
        hash_id = args[1]

        try:
            params = angular_parameters(request, ['claim_tid', 'message', 'email'])

            claim_tid = int(params['claim_tid'])
            if claim_tid == PublicationsClaims.Types.other:
                message = params['message']
            else:
                message = params.get('message')

            email = params['email']

        except (ValueError, IndexError):
            return cls.PostResponses.invalid_params()


        # check if publication exists and is published
        try:
            model = HEAD_MODELS[tid]
            publication = model.objects.filter(hash_id=hash_id).only('id', 'hash_id')[:1][0]
            if not publication.is_published():
                raise Http404()

        except KeyError:
            return cls.PostResponses.invalid_params()

        except (IndexError, Http404):
            return cls.PostResponses.publication_does_not_exists()


        try:
            PublicationsClaims.new(
                publication.tid, publication.hash_id, claim_tid, email, message)

        except PublicationsClaims.InvalidClaimTypeId:
            return cls.PostResponses.invalid_params()


        # seems to be ok
        return cls.PostResponses.ok()