#coding=utf-8
import copy
import json

import phonenumbers
from phonenumbers import NumberParseException

from django.http.response import HttpResponseRedirect
from django.http import HttpResponseBadRequest, HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from django.views.generic import View

from apps.classes import AnonymousOnlyView, AuthenticatedOnlyView
from apps.common.api.accounts.utils import MobilePhoneChecker
from collective.methods.request_data_getters import angular_post_parameters
from collective.http.responses import HttpJsonResponse
from core.email_backend import email_sender
from core.publications.constants import OBJECTS_TYPES, HEAD_MODELS
from core.users import tasks
from core.users.models import Users, AccessRestoreTokens
from core.utils.jinja2_integration import templates
from core.ban.classes import BanHandler


class RegistrationManager(object):
    class EmailValidation(View):
        post_codes = {
            'OK': {
                'code': 0
            },
            'invalid': {
                'code': 1
            },
            'already_in_use': {
                'code': 2
            }
        }

        def post(self, request, *args):
            if request.user.is_authenticated():
                return HttpResponseBadRequest('Anonymous users only.')


            try:
                email = angular_post_parameters(request, ['email'])['email']
            except (ValueError, IndexError):
                return HttpResponseBadRequest('Empty or absent parameter "email".')

            # is email valid?
            try:
                validate_email(email)
            except ValidationError:
                return HttpResponse(json.dumps(self.post_codes['invalid']), content_type='application/json')

            # is email in use?
            if not Users.email_is_free(email):
                return HttpResponse(json.dumps(self.post_codes['already_in_use']), content_type='application/json')

            # seems to be ok
            return HttpResponse(json.dumps(self.post_codes['OK']), content_type='application/json')



    class MobilePhoneValidation(AnonymousOnlyView):
        post_codes = {
            # todo: refactor this
            # todo: add messages to this responses

            'OK': {
                'code': 0
            },
            'invalid': {
                'code': 1
            },
            'only_ua':{
                'code': 2,
            },
             'already_in_use': {
                'code': 3
            },
            'banned': {
                'code': 4,
            }
        }

        ua_phone_codes = [
            '91', # Тримоб
            '99', # MTC
            '95', # MTC
            '66', # MTC
            '50', # MTC
            '39', # Київстар
            '68', # Київстар
            '98', # Київстар
            '97', # Київстар
            '96', # Київстар
            '67', # Київстар
            '94', # Інтертелеком
            '92', # PEOPLEnet
            '93', # life :)
            '63', # life :)
        ]


        def post(self, request, *args):
            try:
                number = angular_post_parameters(request, ['number'])['number']
            except (ValueError, IndexError):
                return HttpResponseBadRequest('Empty or absent parameter "number".')

            # is number correct?
            try:
                number = phonenumbers.parse(number, 'UA')
            except NumberParseException:
                return HttpResponse(json.dumps(self.post_codes['invalid']), content_type='application/json')

            if not phonenumbers.is_valid_number(number):
                return HttpResponse(json.dumps(self.post_codes['only_ua']), content_type='application/json')

            # is number in use?
            number = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)
            if not Users.mobile_phone_number_is_free(number):
                return HttpResponse(json.dumps(self.post_codes['already_in_use']), content_type='application/json')

            # is number banned?
            if BanHandler.contains_number(number):
                return HttpResponse(json.dumps(self.post_codes['banned']), content_type='application/json')

            # seems to be ok
            return HttpResponse(json.dumps(self.post_codes['OK']), content_type='application/json')



    class Registration(AnonymousOnlyView):
        post_codes = {
            'OK': {
                'code': 0,
            },
            'first_name_empty': {
                'code': 1,
            },
            'last_name_empty': {
                'code': 2,
            },
            'phone_empty': {
                'code': 3,
            },
            'email_empty': {
                'code': 4,
            },
            'password_empty': {
                'code': 5,
            },
            'password_repeat_empty': {
                'code': 6,
            },
            'passwords_not_match': {
                'code': 7,
            },
            'phone_banned': {
                'code': 8,
            },

            # --
            'invalid_code_check': {
                'code': 100,
            },

            # --
            'in_check_queue': {
                # користувач з такими даними вже зареєстрований
                # і знаходиться на етапі перевірки коду моб. телефону.
                'code': 200,
            }
        }


        def post(self, request, *args):
            if MobilePhoneChecker.check_is_started(request):
                try:
                    code = angular_post_parameters(request, ['code'])['code']
                except ValueError:
                    return HttpResponseBadRequest('Empty or absent parameter "code".')

                response = HttpResponse()
                ok, check_results = MobilePhoneChecker.check_code(code, request, response)
                if not ok:
                    # WARNING: deep copy is needed here
                    body = copy.deepcopy(self.post_codes['invalid_code_check'])
                    response.write(json.dumps(body))
                    return response


                # seems to be ok
                uid = check_results['id']
                user = Users.objects.filter(id=uid).only('id')[:1][0]
                user.is_active = True
                user.save()
                return LoginManager.Login.login_user_without_password(user, request, response)


            else:
                try:
                    check_results = angular_post_parameters(request,
                            ['name', 'surname', 'phone-number', 'email', 'password', 'password-repeat'])
                except ValueError as e:
                    return HttpResponseBadRequest(e.message)


                first_name = check_results.get('name', '')
                if not first_name:
                    return HttpResponseBadRequest(
                        json.dumps(self.post_codes['first_name_empty']), content_type='application/json')

                last_name = check_results.get('surname', '')
                if not last_name:
                    return HttpResponseBadRequest(
                        json.dumps(self.post_codes['last_name_empty']), content_type='application/json')

                phone_number = check_results.get('phone-number', '')
                if not phone_number:
                    return HttpResponseBadRequest(
                        json.dumps(self.post_codes['phone_empty']), content_type='application/json')

                # check if number was banned
                if BanHandler.contains_number(
                        phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)):
                    return HttpResponseBadRequest(
                        json.dumps(self.post_codes['phone_banned']), content_type='application/json')

                email = check_results.get('email', '')
                if not email:
                    return HttpResponseBadRequest(
                        json.dumps(self.post_codes['email_empty']), content_type='application/json')

                password = check_results.get('password', '')
                if not password:
                    return HttpResponseBadRequest(
                        json.dumps(self.post_codes['password_empty']), content_type='application/json')

                password_repeat = check_results.get('password-repeat', '')
                if not password_repeat:
                    return HttpResponseBadRequest(
                        json.dumps(self.post_codes['password_repeat_empty']), content_type='application/json')


                # passwords match check
                if password != password_repeat:
                    return HttpResponseBadRequest(
                        json.dumps(self.post_codes['passwords_not_match']), content_type='application/json')


                # ...
                # todo: request check here
                # ...

                try:
                    # Дана функція зажди повертає результат ОК,
                    # незалежно від того чи була насправді відіслана sms.
                    # Це зроблено для того, щоб зловмисники у випадку атаки
                    # не мали змоги слідкувати за тим чи надсилаються sms.
                    response = HttpResponse(json.dumps(self.post_codes['OK']), content_type='application/json')

                    # creating of disabled account.
                    with transaction.atomic():
                        user = Users.objects.create_user(email, phone_number, password)
                        user.first_name = first_name
                        user.last_name = last_name
                        user.save()

                        tasks.remove_inactive_account.apply_async(
                            [user.id, ], countdown=MobilePhoneChecker._transaction_ttl)
                        MobilePhoneChecker.begin_check(user.id, phone_number, request, response)

                    # seems to be ok.
                    return response

                except MobilePhoneChecker.AlreadyInQueue:
                    # Користувач з такими реєстраційними даними вже присутній
                    # і знаходиться на етапі перевірки коду з СМС
                    return HttpResponse(self.post_codes['in_check_queue'], content_type='application/json')



    class CancelRegistration(AnonymousOnlyView):
        post_codes = {
            'OK': {
                'code': 0
            }
        }


        def post(self, request, *args):
            response = HttpJsonResponse(self.post_codes['OK'])

            # In case when user decided to cancel his registration
            # (for example if he doesn't received sms from us)
            # we need to remove his data from our database too.
            # to do this wee ned his id.
            user_id = MobilePhoneChecker.cancel_check(request, response)
            Users.objects.filter(id=user_id).delete()

            return response



    class ResendCheckSMS(AnonymousOnlyView):
        post_codes = {
            'OK': {
                'code': 0
            }
        }


        def post(self, request, *args):
            # Дана функція зажди повертає результат ОК,
            # незалежно від того чи була насправді відіслана sms.
            # Це зроблено для того, щоб зловмисники у випадку атаки
            # не мали змоги слідкувати за тим чи надсилаються sms.
            response = HttpResponse(json.dumps(self.post_codes['OK']), content_type='application/json')
            try:
                MobilePhoneChecker.resend_sms(request)
            except Exception:
                pass
            return response



class LoginManager(object):
    class Login(AnonymousOnlyView):
        class PostResponses(object):
            @staticmethod
            def ok():
                return HttpJsonResponse({
                    'code': 0,
                    'message': 'OK',
                })




        post_codes = {
            'OK': {
                'code': 0,
            },
            'username_empty': {
                'code': 1,
            },
            'password_empty': {
                'code': 2,
            },
            'invalid_attempt': {
                'code': 3,
            },
            'account_disabled': {
                'code': 4,
            }
        }


        def post(self, request, *args):
            try:
                d = angular_post_parameters(request, ['username', 'password'])
            except ValueError:
                return HttpResponseBadRequest('Empty or absent parameter "username" or "password"')


            username = d.get('username', '')
            if not username:
                return HttpResponseBadRequest(
                    json.dumps(self.post_codes['username_empty']), content_type='application/json')

            password = d.get('password', '')
            if not username:
                return HttpResponseBadRequest(
                    json.dumps(self.post_codes['password_empty']), content_type='application/json')


            try:
                phone_number = phonenumbers.parse(username, 'UA')
                if phonenumbers.is_valid_number(phone_number):
                    username = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)

                # check if phone number was not banned
                if BanHandler.contains_number(phone_number):
                    return HttpResponse(
                        json.dumps(self.post_codes['account_disabled']), content_type='application/json')


                user = Users.objects.filter(mobile_phone=username).only('id')[:1]
                if user:
                    user = user[0]

            except NumberParseException:
                user = None


            if not user:
                # attempt with email
                user = Users.by_email(username)
                if user is None:
                    return HttpResponse(
                        json.dumps(self.post_codes['invalid_attempt']), content_type='application/json')


            user = authenticate(username=user.mobile_phone, password=password)
            if user is not None:
                if user.is_active:
                    # seems to be ok
                    response = HttpResponse(content_type='application/json')
                    return self.login_user_without_password(user, request, response)

                else:
                    return HttpResponse(
                        json.dumps(self.post_codes['account_disabled']), content_type='application/json')

            return HttpResponse(
                json.dumps(self.post_codes['invalid_attempt']), content_type='application/json')


        @classmethod
        def login_user_without_password(cls, user, request, response):
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            # WARNING: deep copy is needed here
            body = copy.deepcopy(cls.post_codes['OK'])
            body['user'] = LoginManager.on_login_data(user)
            response.write(json.dumps(body))
            return response



    class Logout(AuthenticatedOnlyView):
        post_codes = {
            'OK': {
                'code': 0,
            },
        }


        def post(self, request, *args):
            logout(request)
            return HttpResponse(json.dumps(self.post_codes['OK']), content_type='application/json')



    class OnLogin(AuthenticatedOnlyView):
        post_codes = {
            'OK': {
                'code': 0,
            },
        }


        def get(self, request, *args):
            body = copy.deepcopy(self.post_codes['OK']) # note: deep copy is needed here
            body['user'] = LoginManager.on_login_data(request.user)
            return HttpResponse(json.dumps(body), content_type='application/json')



    @staticmethod
    def on_login_data(user):
        return {
            'name': user.first_name,
            'surname': user.last_name,
        }



class AccessRestoreManager(object):
    class BeginRestore(AnonymousOnlyView):
        post_codes = {
            'OK': {
                'code': 0,
            },
            'invalid_username': {
                'code': 1,
            },
            'invalid_attempt': {
                'code': 2,
            },
        }


        def post(self, request, *args):
            try:
                username = angular_post_parameters(request, ['username'])['username']
            except ValueError:
                return HttpResponseBadRequest(
                    self.post_codes['invalid_username'], content_type='application/json')


            user = None
            try:
                # attempt with phone number
                phone_number = phonenumbers.parse(username, 'UA')
                if phonenumbers.is_valid_number(phone_number):
                    phone_number = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)

                users = Users.objects.filter(mobile_phone=phone_number).only('id')[:1]
                if users:
                    user = users[0]

            except NumberParseException:
                # attempt with email
                users = Users.objects.filter(email=username).only('id')[:1]
                if users:
                    user = users[0]

            if user is None:
                return HttpResponse(json.dumps(self.post_codes['invalid_attempt']), content_type='application/json')


            record = AccessRestoreTokens.new(user)
            html = templates.get_template('email/access_restore/new_token.html').render({
                'token_url': '{domain}{url}?token={token_id}'.format(
                    domain = settings.REDIRECT_DOMAIN_URL,
                    url = '/accounts/access-restore/redirect/',
                    token_id = record.token
                )
            })
            email_sender.send_html_email(
                subject=u'Восстановление пароля', # tr
                html=html,
                addresses_list=[record.user.email],
            )

            return HttpResponse(json.dumps(self.post_codes['OK']), content_type='application/json')


    class RedirectFromEmail(AnonymousOnlyView):
        """
        На деяких поштових клієнтах посилання виду "#!..." заміняються на "#%21...",
        тому посилання на відновлення паролю не працює з цих поштовиків.

        Даний клас забезпечує коректний HTTP-редірект на ajax-діалог на фронті.
        Посилання на дану в’юху кидається в листі на віднолення паролю.
        """
        def get(self, request):
            token = request.GET.get('token')
            if not token:
                return HttpResponseBadRequest('Invalid request token.')


            url = '{domain}{url}?token={token_id}'.format(
                domain = settings.REDIRECT_DOMAIN_URL,
                url = '#!/account/restore-access',
                token_id = token
            )
            return HttpResponseRedirect(url, content='Перенаправление...')


    class Check(AnonymousOnlyView):
        post_codes = {
            'OK': {
                'code': 0,
            },
            'invalid_token': {
                'code': 1,
            },
            'invalid_password_or_repeat': {
                'code': 2,
            },
            'passwords_not_match': {
                'code': 3,
            }
        }


        def post(self, request, *args):
            try:
                token = angular_post_parameters(request, ['token'])['token']
                if not token:
                    raise ValueError('Token can\'t be empty.')
            except (IndexError, ValueError):
                return HttpResponse(json.dumps(
                    self.post_codes['invalid_token']), content_type='application/json')


            token_record_query = AccessRestoreTokens.objects.filter(token=token)[:1]
            if not token_record_query:
                return HttpResponse(json.dumps(
                    self.post_codes['invalid_token']), content_type='application/json')
            token = token_record_query[0]


            try:
                params = angular_post_parameters(request, ['password', 'password-repeat'])
            except ValueError:
                return HttpResponse(json.dumps(
                    self.post_codes['invalid_password_or_repeat']), content_type='application/json')


            if params['password'] != params['password-repeat']:
                return HttpResponse(
                    json.dumps(self.post_codes['passwords_not_match']),
                    content_type='application/json')

            with transaction.atomic():
                token.user.set_password(params['password'])
                token.user.save()
                token.delete()

            response = HttpResponse(content_type='application/json')
            LoginManager.Login.login_user_without_password(token.user, request, response)
            return response


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