#coding=utf-8
import copy
import json

from django.http import HttpResponseBadRequest, HttpResponse
from django.views.generic import View
from collective.decorators.ajax import json_response, json_response_bad_request

from collective.exceptions import InvalidHttpParameter
from core.publications.constants import OBJECTS_TYPES, HEAD_MODELS



class Contacts(View):
    class GetResponses(object):
        @staticmethod
        @json_response
        def ok(user):
            contacts = {}

            if user.first_name:
                contacts['first_name'] = user.first_name

            if user.last_name:
                contacts['last_name'] = user.last_name

            if user.avatar.url():
                contacts['avatar_url'] = user.avatar.url()

            preferences = user.preferences
            if preferences.mobile_phone_may_be_shown():
                if user.mobile_phone:
                    contacts['mobile_phone'] = user.mobile_phone

            if preferences.add_mobile_phone_may_be_shown():
                if user.add_mobile_phone:
                    contacts['add_mobile_phone'] = user.add_mobile_phone

            if preferences.landline_phone_may_be_shown():
                if user.landline_phone:
                    contacts['landline_phone'] = user.landline_phone

            if preferences.add_landline_phone_may_be_shown():
                if user.add_landline_phone:
                    contacts['add_landline_phone'] = user.add_landline_phone

            if preferences.skype_may_be_shown():
                if user.skype:
                    contacts['skype'] = user.skype

            if preferences.email_may_be_shown():
                if user.work_email:
                    contacts['email'] = user.work_email
                elif user.email:
                    contacts['email'] = user.email

            return {
                'code': 0,
                'data': contacts
            }


        @staticmethod
        @json_response_bad_request
        def invalid_parameters():
            return {
                'code': 1,
                'message': 'request contains invalid parameters.'
            },


    @classmethod
    def get(cls, request, *args):
        try:
            tid, hash_hid = int(args[0]), args[1]
            model = HEAD_MODELS[tid]
        except (IndexError, ValueError, KeyError):
            return cls.GetResponses.invalid_parameters()


        try:
            publication = model.queryset_by_hash_id(hash_hid).only('id', 'owner')[:1][0]
        except IndexError:
            return cls.GetResponses.invalid_parameters()


        return cls.GetResponses.ok(publication.owner)