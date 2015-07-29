#coding=utf-8
from django.views.generic import View

from collective.decorators.ajax import json_response, json_response_bad_request
from core.publications.constants import HEAD_MODELS


class Contacts(View):
    class GetResponses(object):
        @staticmethod
        @json_response
        def ok(user):
            preferences = user.preferences
            contacts = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'avatar_url': user.avatar.url(),

                'mobile_phone': user.mobile_phone if preferences.mobile_phone_may_be_shown() else None,
                'add_mobile_phone': user.add_mobile_phone if preferences.add_mobile_phone_may_be_shown() else None,

                'landline_phone': user.landline_phone if preferences.landline_phone_may_be_shown() else None,
                'add_landline_phone': user.add_landline_phone if preferences.add_landline_phone_may_be_shown() else None,

                'skype': user.skype if preferences.skype_may_be_shown() else None,

                # note: work email wil lbe shown if main email address should be hidden
                'email': user.email if preferences.email_may_be_shown() else user.work_email,


                # preferences
                'allow_call_requests': preferences.allow_call_requests,
                'allow_messaging': preferences.allow_messaging,
            }

            # Not all fields may be present.
            # User may omit some of them,
            # so wee need to remove empty entries here
            contacts = {
                k: v for k, v in contacts.items() if v
            }

            return {
                'code': 0,
                'message': 'OK',
                'data': contacts
            }


        @staticmethod
        @json_response_bad_request
        def invalid_parameters():
            return {
                'code': 1,
                'message': 'Request contains invalid parameters.'
            },


    @classmethod
    def get(cls, request, *args):
        try:
            tid, hash_hid = int(args[0]), args[1]
            model = HEAD_MODELS[tid]
        except (ValueError, IndexError, KeyError):
            return cls.GetResponses.invalid_parameters()


        try:
            publication = model.queryset_by_hash_id(hash_hid)\
                .only('id')\
                .prefetch_related('owner')\
                [:1][0]
        except IndexError:
            return cls.GetResponses.invalid_parameters()


        return cls.GetResponses.ok(publication.owner)