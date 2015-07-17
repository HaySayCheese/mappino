from datetime import datetime

from django.core.exceptions import RentTypeError, PermissionDenied
from django.views.generic import View

from collective.http.responses import HttpJsonResponse
from core.publications.constants import OBJECTS_TYPES, HEAD_MODELS


class CalendarControlView(View):

    @classmethod
    def post(cls, request, *args):
        try:
            tid, hash_id = args[0], args[1]
            tid = int(tid)
        except (IndexError, TypeError, ):
            return cls.Post.absent_publications_id()

        if not tid in OBJECTS_TYPES.daily_rent:

            raise RentTypeError('This type of objects doest supply daily rent')

        try:
            date_from = request.POST.get('date_from')
            date_to = request.POST.get('date_to')
        except:
             return cls.Post.invalid_date()


        date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
        date_to = datetime.strptime(date_to, '%Y-%m-%d').date()

        model = HEAD_MODELS[tid]

        #Publication - my way, to named head.
        publication = model.objects.get(hash_id = hash_id)

        if publication.owner.id != request.user.id:
            raise PermissionDenied()

        try:
            publication.rent_terms.add_dates_rent(tid, date_from, date_to )
        except (ValueError, ):
            return cls.Post.invalid_date()

        return cls.Post.ok()

    @classmethod
    def get(cls, request, *args):
        try:
            tid, hash_id = args[0], args[1]
            tid = int(tid)
        except (IndexError, TypeError, ):
            return cls.Post.absent_publications_id()

        if not tid in OBJECTS_TYPES.daily_rent:
            # error
            raise RentTypeError('This type of objects doest supply daily rent')

        model = HEAD_MODELS[tid]
        publication = model.objects.get(hash_id = hash_id)


        try:
            calendar_rent_dates = publication.rent_terms.get_rent_dates()
        except (ValueError, ):
            return cls.Post.invalid_date()


        return cls.Get.ok(calendar_rent_dates)


    @classmethod
    def delete(cls, request, *args):
        try:
            tid, hash_id = args[0], args[1]
            tid = int(tid)
        except (IndexError, TypeError, ):
            return cls.Post.absent_publications_id()

        if not tid in OBJECTS_TYPES.daily_rent:
            # error
            raise RentTypeError('This type of objects doest supply daily rent')

        try:
            date_from = request.GET.get('date_from')
            date_to = request.GET.get('date_to')
        except:
             return cls.Post.invalid_date()


        date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
        date_to = datetime.strptime(date_to, '%Y-%m-%d').date()

        model = HEAD_MODELS[tid]

        #Publication - my way, to named head.
        publication = model.objects.get(hash_id = hash_id)

        if publication.owner.id != request.user.id:
            raise PermissionDenied()

        try:
            publication.rent_terms.remove_rent_dates(tid, date_from, date_to)
        except (ValueError, ):
            return cls.Post.invalid_date()


        return cls.Delete.ok()

    class Delete(object):
        @staticmethod
        def ok():
            return HttpJsonResponse({
                'code': 0,
                'message': 'OK'
            })


    class Get(object):
        @staticmethod
        def ok(calendar_rent_dates):
            return HttpJsonResponse({
                'code': 0,
                'message': 'OK',
                'data': calendar_rent_dates
            })


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
                'message': "one of dates is absent or already exist in base"
            })




