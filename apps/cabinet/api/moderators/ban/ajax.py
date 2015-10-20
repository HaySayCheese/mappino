from apps.views_base import ModeratorsView
from collective.decorators.ajax import json_response, json_response_not_found
from core.managing.ban.classes import BanHandler
from collective.methods.request_data_getters import angular_post_parameters

from core.managing.ban.models import BannedPhoneNumbers, SuspiciousPhoneNumbers
from core.users.models import Users


class BanUser(ModeratorsView):
    class PostResponses(object):
        @staticmethod
        @json_response
        def ok():
            return {
                'code': 0,
                'message': 'OK'
            }

        @classmethod
        @json_response_not_found
        def number_already_exist(cls):
            return {
                'code': 2,
                'message': 'Number already banned'
            }

    @classmethod
    def post(cls, request):

        phone_number = angular_post_parameters(request).get('phone_number', '')

        user = Users.objects.filter(mobile_phone=phone_number)[0]

        if BanHandler.check_user(user):
            return cls.PostResponses.number_already_exist()

        if not BanHandler.ban_user(user):
            return cls.PostResponses.number_already_exist()

        else:
            return cls.PostResponses.ok()


class AddSuspiciousUser(ModeratorsView):
    class PostResponses(object):
        @staticmethod
        @json_response
        def ok():
            return {
                'code': 0,
                'message': 'OK'
            }

        @classmethod
        @json_response_not_found
        def number_already_exist(cls):
            return {
                'code': 2,
                'message': 'Number already suspicious'
            }

    @classmethod
    def post(cls, request):

        phone_number = angular_post_parameters(request).get('phone_number', '')

        user = Users.objects.filter(mobile_phone=phone_number)[0]

        if BanHandler.check_suspicious_user(user):
            return cls.PostResponses.number_already_exist()

        if not BanHandler.add_suspicious_user(user):
            return cls.PostResponses.number_already_exist()

        else:
            return cls.PostResponses.ok()