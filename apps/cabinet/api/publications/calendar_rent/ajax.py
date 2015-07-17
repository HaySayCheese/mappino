from datetime import datetime

from django.views.generic import View

from collective.http.responses import HttpJsonResponse
from core.publications.constants import OBJECTS_TYPES, HEAD_MODELS


class CalendarControlView(View):

    @classmethod
    def post(cls, request, *args):
        try:
            tid, hash_id = args[0], args[1]
            tid = int(tid)
        except (IndexError, ValueError, ):
            return cls.CommonResponses.absent_publications_id()

        if not tid in OBJECTS_TYPES.daily_rent:
            return cls.CommonResponses.invalid_tid_object()


        date_from = request.POST.get('date_from','')
        date_to = request.POST.get('date_to','')

        if not date_from or date_to:
            return cls.CommonResponses.invalid_date()

        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
        except (ValueError, ) :
            return cls.CommonResponses.invalid_date_format()

        model = HEAD_MODELS[tid]

        #Publication - my way, to named head.
        try:
            publication = model.objects.filter(hash_id = hash_id).values_list('rent_terms')[0][0]
        except (IndexError,):
            return cls.CommonResponses.invalid_hash_id()


        if publication.owner.id != request.user.id:
            return cls.CommonResponses.invalid_user()

        try:
            publication.rent_terms.add_dates_rent(tid, date_from, date_to )
        except (ValueError, ):
            return cls.CommonResponses.invalid_date()

        return cls.Post.ok()

    @classmethod
    def get(cls, request, *args):
        try:
            tid, hash_id = args[0], args[1]
            tid = int(tid)
        except (IndexError, ValueError, ):
            return cls.CommonResponses.absent_publications_id()

        if not tid in OBJECTS_TYPES.daily_rent:
            return cls.CommonResponses.invalid_tid_object()

        model = HEAD_MODELS[tid]

        try:
            publication = model.objects.filter(hash_id = hash_id).values_list('rent_terms')[0][0]
        except (IndexError,):
            return cls.CommonResponses.invalid_hash_id()

        calendar_rent_dates = publication.rent_terms.get_rent_dates()

        return cls.Get.ok(calendar_rent_dates)


    @classmethod
    def delete(cls, request, *args):

        try:
            tid, hash_id = args[0], args[1]
            tid = int(tid)
        except (IndexError, ValueError, ):
            return cls.CommonResponses.absent_publications_id()

        if not tid in OBJECTS_TYPES.daily_rent:
            return cls.CommonResponses.invalid_tid_object()

        date_from = request.POST.get('date_from','')
        date_to = request.POST.get('date_to','')

        if not date_from or date_to:
            return cls.CommonResponses.invalid_date()

        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
        except (ValueError, ) :
            return cls.CommonResponses.invalid_date_format()

        model = HEAD_MODELS[tid]

        #Publication - my way, to named head.
        try:
            publication = model.objects.filter(hash_id = hash_id).values_list('rent_terms')[0][0]
        except (IndexError,):
            return cls.CommonResponses.invalid_hash_id()


        if publication.owner.id != request.user.id:
            return cls.CommonResponses.invalid_user()

        try:
            publication.rent_terms.remove_rent_dates(tid, date_from, date_to)
        except (ValueError, ):
            return cls.CommonResponses.invalid_date_format()

        return cls.Delete.ok()




    class CommonResponses(object):

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

        @staticmethod
        def invalid_date_format():
            return  HttpJsonResponse({
                'code': 3,
                'message': "one of dates is absent or already exist in base"
            })

        @staticmethod
        def invalid_tid_object():
            return HttpJsonResponse({
                'code': 4,
                'message': " Object type doesnt supply daily rent"
            })

        @staticmethod
        def invalid_user():
            return HttpJsonResponse({
                "code": 5,
                "message": "This user has not permissions for this publications"
            })

        @staticmethod
        def invalid_hash_id():
            return HttpJsonResponse({
                "code": 6,
                "messages": "There no publication with such hash_id"
            })


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





