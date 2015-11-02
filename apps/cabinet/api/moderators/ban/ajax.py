from apps.views_base import ModeratorsView
from collective.decorators.ajax import json_response, json_response_not_found, json_response_bad_request
from core.managing.ban.classes import BanHandler
from collective.methods.request_data_getters import angular_post_parameters

from core.managing.ban.models import BannedPhoneNumbers, SuspiciousPhoneNumbers
from core.publications.constants import OBJECTS_TYPES, HEAD_MODELS
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
        @json_response_bad_request
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
            for tid in OBJECTS_TYPES.values():
                query = HEAD_MODELS[tid].by_user_id(user.id).only('id')
                for publication in query:
                    head = HEAD_MODELS[tid].queryset_by_hash_id(publication.hash_id).only('id', 'owner')[0]
                    head.unpublish()
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
        @json_response_bad_request
        def user_already_suspicious(cls):
            return {
                'code': 2,
                'message': 'User already suspicious'
            }

    @classmethod
    def post(cls, request):

        phone_number = angular_post_parameters(request).get('phone_number', '')

        user = Users.objects.filter(mobile_phone=phone_number)[0]

        if BanHandler.check_suspicious_user(user):
            return cls.PostResponses.user_already_suspicious()

        if not BanHandler.add_suspicious_user(user):
            return cls.PostResponses.user_already_suspicious()

        else:
            return cls.PostResponses.ok()


class RemoveSuspiciousUser(ModeratorsView):

    class PostResponses(object):
        @staticmethod
        @json_response
        def ok():
            return {
                'code': 0,
                'message': 'OK'
            }

        @classmethod
        @json_response_bad_request
        def user_not_suspicious(cls):
            return {
                'code': 2,
                'message': 'User is not suspicious'
            }

    @classmethod
    def post(cls, request):

        phone_number = angular_post_parameters(request).get('phone_number', '')

        user = Users.objects.filter(mobile_phone=phone_number)[0]

        if not BanHandler.check_suspicious_user(user):
            return cls.PostResponses.user_not_suspicious()

        if not BanHandler.liberate_user(user):
            return cls.PostResponses.user_not_suspicious()

        else:
            return cls.PostResponses.ok()