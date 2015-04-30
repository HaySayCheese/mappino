# coding=utf-8
from django.views.generic import View

from collective.http.responses import HttpJsonResponseBadRequest, HttpJsonResponse, HttpJsonResponseNotFound
from collective.methods.request_data_getters import angular_post_parameters
from core.claims.classes import ClaimsManager
from core.publications import classes
from core.publications.constants import HEAD_MODELS


class DetailedView(View):
    # this is a description generator for the publications.
    formatter = classes.PublishedDataSource()

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
