#coding=utf-8
import copy
import json
import random
import string
from collective.http.responses import HttpJsonResponse

from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponse
from django.contrib.auth import authenticate, login
from django.views.generic import View

from apps.classes import AnonymousOnlyView
from collective.decorators.ajax import json_response, json_response_bad_request
from collective.methods.request_data_getters import angular_post_parameters
from core.ban.classes import BanHandler
from core.publications.constants import OBJECTS_TYPES, HEAD_MODELS
from core.sms_dispatcher import login_codes_sms_sender
from core.users.models import Users


class LoginManager(object):
    class FirstStep(AnonymousOnlyView):
        class PostResponses(object):
            @staticmethod
            def ok():
                response = HttpJsonResponse({
                    'code': 0,
                    'message': 'OK',
                })

                # This cookie is needed fot the front-end.
                # By it's presence front-end login will display or hide
                # state of the login form with the token input
                response.set_signed_cookie('mcheck', ''.join([random.choice(string.ascii_letters) for _ in range(7)]), max_age=60*5)
                return response


            @staticmethod
            @json_response_bad_request
            def invalid_phone_number():
                return {
                    'code': 1,
                    'message': 'Parameter "phone_number" is invalid or absent.'
                }


            @staticmethod
            @json_response
            def account_disabled():
                return {
                    'code': 2,
                    'message': 'Account associated with this phone number was deactivated.'
                }


        def post(self, request):
            try:
                phone_number = angular_post_parameters(request, ['phone_number'])['phone_number']
                phone_number = Users.objects.parse_phone_number(phone_number)
            except (ValueError, KeyError):
                return self.PostResponses.invalid_phone_number()


            # check if phone number was not banned
            if BanHandler.contains_number(phone_number):
                return self.PostResponses.account_disabled()


            user = Users.by_one_of_the_mobile_phones(phone_number)
            if user is None:
                # is no user such mobile phone - we need to create new empty user
                user = Users.objects.create_user(phone_number)


            user.update_one_time_token()

            if not settings.DEBUG:
                login_codes_sms_sender.send(phone_number, user.one_time_token, request)

            return self.PostResponses.ok()


    class SecondStep(AnonymousOnlyView):
        class PostResponses(object):
            @staticmethod
            def ok(user):
                response = HttpJsonResponse({
                    'code': 0,
                    'message': 'OK',
                    'data': {
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'avatar_url': user.avatar.url(),
                    }
                })

                response.delete_cookie('mcheck')
                return response

            @staticmethod
            @json_response_bad_request
            def invalid_phone_number():
                return {
                    'code': 1,
                    'message': 'Parameter "phone_number" is invalid or absent.'
                }


            @staticmethod
            @json_response
            def account_disabled():
                return {
                    'code': 2,
                    'message': 'Account associated with this phone number was deactivated.'
                }


            @staticmethod
            @json_response
            def invalid_attempt():
                return {
                    'code': 3,
                    'message': 'Code is invalid.'
                }



        def post(self, request):
            try:
                params = angular_post_parameters(request, ['phone_number', 'token'])
                phone_number = params['phone_number']
                phone_number = Users.objects.parse_phone_number(phone_number)

                token = params['token']
            except (ValueError, KeyError):
                return self.PostResponses.invalid_phone_number()


            # check if phone number was not banned
            if BanHandler.contains_number(phone_number):
                return self.PostResponses.account_disabled()


            authenticated_user = authenticate(mobile_phone=phone_number, one_time_token=token)
            if authenticated_user is None:
                return self.PostResponses.invalid_attempt()


            # to authenticate user without password we need a little trick
            authenticated_user.backend = 'core.users.authentication_backends.SMSAuthenticationBackend'
            login(request, authenticated_user)

            return self.PostResponses.ok(authenticated_user)


class Contacts(View):
    """
    Implements operations for getting contacts of realtors on main pages of the site.
    """
    get_codes = {
        'OK': {
            'code': 0,
            'contacts': None, # WARN: owner's contacts here
        },
        'invalid_parameters': {
            'code': 1
        },
        'invalid_tid': {
            'code': 2
        },
        'invalid_hid': {
            'code': 3
        },
    }


    def get(self, request, *args):
        """
        Returns contacts of the owner of the publication accordingly to his preferences.
        """
        try:
            tid, hid = args[0].split(':')
            tid = int(tid)
            hid = int(hid)
        except (ValueError, IndexError):
            return HttpResponseBadRequest(
                json.dumps(self.get_codes['invalid_parameters']), content_type='application/json')


        if tid not in OBJECTS_TYPES.values():
            return HttpResponseBadRequest(
                json.dumps(self.get_codes['invalid_tid']), content_type='application/json')


        model = HEAD_MODELS[tid]
        try:
            publication = model.objects.filter(id=hid).only('id', 'owner')[:1][0]
        except IndexError:
            return HttpResponseBadRequest(
                json.dumps(self.get_codes['invalid_hid']), content_type='application/json')


        data = copy.deepcopy(self.get_codes['OK']) # WARN: deep copy here
        data['contacts'] = publication.owner.contacts_dict()
        return HttpResponse(json.dumps(data), content_type='application/json')