from django.http.response import HttpResponseBadRequest
from django.views.generic.base import View
from collective.http.responses import HttpJsonResponse, HttpJsonResponseBadRequest
from collective.methods.request_data_getters import angular_parameters
from core.publications.abstract_models import AbstractHeadModel
from core.publications.constants import HEAD_MODELS


class PublishedPublicationControllerView(View):


    @classmethod
    def post(cls, request, is_adequacy, message):
        """
        :param request:
        :param is_adequacy: True or False.
            If False publication will be  unpublished,
            If True publication will be set as moderated by added date_moderated

        :param message: If publication is not adequacy, this message will contain a reason
        """
        try:
            params = angular_parameters(request, ['id'])
            tid, hash_id = params['id'].split(':')
            tid = int(tid)
        except ValueError:
            return cls.absent_publications_id()

        if is_adequacy:
            model = HEAD_MODELS[tid]
            try:
                head = model.objects.filter(hash_id=hash_id).only('id', 'owner')[0]
            except IndexError:
                return HttpResponseBadRequest(json.dumps(
                    cls.put_codes['invalid_hid']), content_type='application/json')

            # check owner
            if head.owner.id != request.user.id:
                raise PermissionDenied()

            # seems to be ok
            head.unpublish()
            return HttpResponse(json.dumps(
                self.put_codes['OK']), content_type='application/json')

        else:
            PublicationsToCheck.mapped_publication_as_moderated(tid, hash_id)

        return

    @classmethod
    def get(cls, request):
        return


    class Post(object):
        @staticmethod
        def ok():

            return HttpJsonResponse({
                'code': 0,
                'message': "OK"
            })

    class Get(object):
        @staticmethod
        def ok(publication_ids):
            return HttpJsonResponse({
                'code': 0,
                'message': "OK",
                'data': {
                    'publication_ids': publication_ids,
                }
            })

    @staticmethod
    def absent_publications_id():
        return HttpJsonResponseBadRequest({
            'code': 1,
            'message': '"tid" or "hash_id" for publication is absent.'
        })