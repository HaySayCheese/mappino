#coding=utf-8
import copy
import json
import random
import string

from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View

from apps.views_base import AnonymousOnlyView, AuthenticatedOnlyView
from collective.http.responses import HttpJsonResponse
from collective.decorators.ajax import json_response, json_response_bad_request
from collective.methods.request_data_getters import angular_post_parameters
from core.managing.ban.classes import BanHandler
from core.notifications.sms_dispatcher.common import NotificationsSender
from core.publications.constants import OBJECTS_TYPES, HEAD_MODELS
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
                # By it's presence front-end login will display or hide the state of the login form with the token input.
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
                params = angular_post_parameters(request, ['phone_code', 'phone_number'])
                phone_number = params['phone_code'] + params['phone_number']
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
                NotificationsSender.send_login_code(request, phone_number, user.one_time_token)

            return self.PostResponses.ok()


    class SecondStep(AnonymousOnlyView):
        class PostResponses(object):
            @staticmethod
            def ok(user):
                response = HttpJsonResponse({
                    'code': 0,
                    'message': 'OK',
                    'data': LoginManager.on_login_info(user)
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
                params = angular_post_parameters(request, ['phone_code', 'phone_number', 'token'])
                phone_number = params['phone_code'] + params['phone_number']
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


            # Every SMS transaction is paid,
            # so wee need to send SMS as less as possible.
            #
            # To do sow wee will prolong users's session up to 2 years,
            # to have possibility to not to send another login sms to him as long as possible.
            request.session.set_expiry(60*60*24*365*2)
            request.session.save()


            return self.PostResponses.ok(authenticated_user)


    class OnLoginInfo(AuthenticatedOnlyView):
        class GetResponses(object):
            @staticmethod
            @json_response
            def ok(user):
                return {
                    'code': 0,
                    'message': 'OK',
                    'data': LoginManager.on_login_info(user)
                }


        def get(self, reguest):
            return self.GetResponses.ok(reguest.user)


    class Logout(AuthenticatedOnlyView):
        class PostResponses(object):
            @staticmethod
            @json_response
            def ok():
                return {
                    'code': 0,
                    'message': 'OK',
                }


        @classmethod
        def post(cls, request):
            logout(request)
            return cls.PostResponses.ok()


    @staticmethod
    def on_login_info(user):
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'avatar_url': user.avatar.url(),
        }


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