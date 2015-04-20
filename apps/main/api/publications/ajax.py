# coding=utf-8
import json
from collective.http.responses import HttpJsonResponseBadRequest, HttpJsonResponse, HttpJsonResponseNotFound
from collective.methods.request_data_getters import angular_post_parameters
from core.claims.classes import ClaimsManager
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.generic import View

from core.publications import classes
from core.publications.constants import HEAD_MODELS



class DetailedView(View):
    codes = {
        'invalid_parameters': {
            'code': 1
        },
        'unpublished': {
        '   code': 2
        }
    }


    def __init__(self):
        super(DetailedView, self).__init__()
        self.formatter = classes.PublishedDataSource()


    def get(self, request, *args):
        try:
            tid, hash_hid = args[0].split(':')
            tid = int(tid)
        except (ValueError, IndexError):
            return HttpResponseBadRequest(
                json.dumps(self.codes['invalid_parameters']), content_type='application/json')

        try:
            model = HEAD_MODELS[tid]
            publication = model.objects.filter(hash_id=hash_hid).only(
                'for_sale', 'for_rent', 'body', 'sale_terms', 'rent_terms')[:1][0]
        except IndexError:
            return HttpResponseBadRequest(
                json.dumps(self.codes['invalid_parameters']), content_type='application/json')

        # Якщо оголошення не опубліковано — заборонити показ.
        if not publication.is_published():
            return HttpResponse(
                json.dumps(self.codes['unpublished']), content_type='application/json')

        description = self.formatter.format(tid, publication)

        photos = publication.photos()
        if photos:
            description['head']['photos'] = []
            for photo in photos:
                if photo.is_title:
                    description['head']['title_photo'] = photo.url() + photo.title_thumbnail_name()
                description['head']['photos'].append(photo.url() + photo.image_name())


        # Деякі із полів, згенерованих генератором видачі можуть бути пустими.
        # Для уникнення їх появи на фронті їх слід видалити із словника опису.
        description = dict((k, v) for k, v in description.iteritems() if (v is not None) and (v != ""))
        return HttpResponse(json.dumps(description), content_type='application/json')


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



