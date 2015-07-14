from datetime import datetime

from django.core.exceptions import RentTypeError
from django.views.generic import View

from collective.http.responses import HttpJsonResponse
from core.publications.constants import OBJECTS_TYPES, HEAD_MODELS


class CalendarControlView(View):

    #FirstStep
    @classmethod
    def post(cls, request, *args):
        try:
            # params = angular_parameters(request, ['id'])
            # tid, hash_id = params['id'].split(':')
            tid, hash_id = args[0], args[1]
            tid = int(tid)
        except Exception as e:
            return cls.Post.absent_publications_id()

        if not tid in OBJECTS_TYPES.daily_rent:
            # error
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

        # if publication.owner.id != request.user.id:
        #     raise PermissionDenied()

        try:
            publication.rent_terms.add_dates_rent(tid, hash_id, date_from, date_to )
        except (ValueError, ):
            pass
        except Exception as e:
            pass


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


