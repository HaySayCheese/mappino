from datetime import datetime

from django.core.exceptions import PermissionDenied, RentTypeError
from django.views.generic import View

from collective.http.responses import HttpJsonResponse
from collective.methods.request_data_getters import angular_parameters
from core.publications.constants import OBJECTS_TYPES, HEAD_MODELS


class CalendarControlView(View):

    #FirstStep
    @classmethod
    def post(cls, request, *args):
        try:
            params = angular_parameters(request, ['id'])
            tid, hash_id = params['id'].split(':')
            tid = int(tid)
        except ValueError:
            return cls.Post.absent_publications_id()

        if not tid in OBJECTS_TYPES.daily_rent:
            # error
            raise RentTypeError('This type of objects doest supply daily rent')

        try:
            date_from = request.GET.get('date_from')
            date_to = request.GET.get('date_to')
        except:
             return cls.Post.invalid_date()

        date_from = datetime.strptime(date_from, '%Y-%m-%d')
        date_to = datetime.strptime(date_to, '%Y-%m-%d')
        model = HEAD_MODELS[tid]


        #Publication - my way, to named head.
        publication = model.by_id(tid, hash_id)

        if publication.owner.id != request.user.id:
            raise PermissionDenied()

        publication.rent_terms.add_dates_rent(hash_id, date_from, date_to )


        return cls.Post.ok()

    class Post(object):

        @staticmethod
        def ok():
            return HttpJsonResponse({
                'code' : 0,
                'message': "OK"
            })

        @staticmethod
        def absent_publications_id():
            return HttpJsonResponse({
                'code': 1,
                'message': "Tid or Hid id is absent"
            })

        @staticmethod
        def invalid_date():
            return  HttpJsonResponse({
                'code': 2,
                'message': "some of date is absent"
            })


