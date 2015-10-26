from apps.views_base import ManagersView
from collective.decorators.ajax import json_response, json_response_not_found
from collective.methods.request_data_getters import angular_post_parameters

from core.users.models import Users


class AllUsers(ManagersView):
    class GetResponses(object):
        @staticmethod
        @json_response
        def ok(users):

            return {
                'code': 0,
                'message': 'OK',
                'data': [{
                'first_name': user.first_name,
                'last_name': user.last_name,
                'avatar_url': user.avatar.url(),

                'mobile_phone': user.mobile_phone,
                'add_mobile_phone': user.add_mobile_phone,

                'landline_phone': user.landline_phone,
                'add_landline_phone': user.add_landline_phone,

                'skype': user.skype,

                # note: work email wil lbe shown if main email address should be hidden
                'email': user.email ,


                } for user in users]
            }


    @classmethod
    def get(cls, request):

        users = Users.objects.all()

        return cls.GetResponses.ok(users)
