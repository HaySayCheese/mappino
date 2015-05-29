# coding=utf-8
import phonenumbers

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from apps.classes import CabinetView
from core.users.exceptions import AvatarExceptions
from collective.exceptions import RuntimeException
from collective.http.responses import HttpJsonResponse
from collective.methods.request_data_getters import angular_post_parameters
from core.users.constants import Preferences
from core.users.models import Users


class AccountView(CabinetView):
    class GetResponses(object):
        @staticmethod
        def ok(user):
            preferences = user.preferences

            # Дані з фронтенду приходять у міжнародному форматі.
            # Віддати їх треба в національному форматі щоб помістити дані в маску вводу.
            mobile_phone_number = ''
            if user.mobile_phone:
                mobile_phone_number = phonenumbers.format_number(
                    phonenumbers.parse(user.mobile_phone),
                    phonenumbers.PhoneNumberFormat.NATIONAL).replace(' ', '')[1:] # зайві пробіли і початкові нулі видаляються

            add_mobile_phone_number = ''
            if user.add_mobile_phone:
                add_mobile_phone_number = phonenumbers.format_number(
                    phonenumbers.parse(user.add_mobile_phone),
                    phonenumbers.PhoneNumberFormat.NATIONAL).replace(' ', '')[1:] # зайві пробіли і поч. 0 видаляються

            # Стаціонарні і робочі телефони ніяк не валідуються
            landline_phone_number = user.landline_phone if user.landline_phone else ''
            add_landline_phone_number = user.add_landline_phone if user.add_landline_phone else ''

            return HttpJsonResponse({
                'code': 0,
                'message': 'OK',
                'data': {
                    'account': {
                        'name': user.first_name,
                        'surname': user.last_name,
                        'email': user.email,
                        'work_email': user.work_email or '',
                        'skype': user.skype or '',
                        'avatar': user.avatar.url() or '',

                        'mobile_phone': mobile_phone_number,
                        'add_mobile_phone': add_mobile_phone_number,
                        'landline_phone': landline_phone_number,
                        'add_landline_phone': add_landline_phone_number,
                    },
                    'preferences': {
                        # bool values
                        'allow_call_requests': preferences.allow_call_requests,
                        'allow_messaging': preferences.allow_messaging,
                        'hide_email': preferences.hide_email,
                        'hide_mobile_phone_number': preferences.hide_mobile_phone_number,
                        'hide_add_mobile_phone_number': preferences.hide_add_mobile_phone_number,
                        'hide_landline_phone_number': preferences.hide_landline_phone,
                        'hide_add_landline_phone_number': preferences.hide_add_landline_phone,
                        'hide_skype': preferences.hide_skype,

                        # sids
                        'send_call_request_notifications_to_sid': preferences.send_call_request_notifications_to_sid,
                        'send_message_notifications_to_sid': preferences.send_message_notifications_to_sid,
                    }
                }
            })


    class PostResponses(object):
        @staticmethod
        def ok():
            return HttpJsonResponse({
                'code': 0,
                'message': 'OK',
            })


        @staticmethod
        def value_required():
            return HttpJsonResponse({
                'code': 1,
                'message': 'Value is required.'
            })


        @staticmethod
        def invalid_value():
            return HttpJsonResponse({
                'code': 2,
                'message': 'Value is invalid.'
            })


        @staticmethod
        def invalid_email():
            return HttpJsonResponse({
                'code': 10,
                'message': 'Email is invalid.'
            })


        @staticmethod
        def duplicated_email():
            return HttpJsonResponse({
                'code': 11,
                'message': 'Email is duplicated.'
            })


        @staticmethod
        def duplicated_email():
            return HttpJsonResponse({
                'code': 11,
                'message': 'Email is duplicated.'
            })


        @staticmethod
        def invalid_phone():
            return HttpJsonResponse({
                'code': 20,
                'message': 'Invalid phone.'
            })


        @staticmethod
        def duplicated_phone():
            return HttpJsonResponse({
                'code': 21,
                'message': 'Duplicated phone.'
            })


        @staticmethod
        def invalid_parameters():
            return HttpJsonResponse({
                'code': 100,
                'message': 'Request does not contains parameters or one of them is invalid.'
            })


    def __init__(self):
        super(AccountView, self).__init__()
        self.update_methods = {
            'name': self.__update_first_name,
            'surname': self.__update_last_name,
            'email': self.__update_email,
            'work_email': self.__update_work_email,
            'mobile_phone': self.__update_mobile_phone_number,
            'add_mobile_phone': self.__update_add_mobile_phone_number,
            'landline_phone': self.__update_landline_phone_number,
            'add_landline_phone': self.__update_add_landline_phone_number,
            'skype': self.__update_skype,

    
            'allow_call_requests': self.__update_allow_call_request,
            'send_call_request_notifications_to_sid': self.__update_send_call_request_notifications_to_sid,

            'allow_messaging': self.__update_allow_messaging,
            'send_message_notifications_to_sid': self.__update_send_message_notifications_to_sid,

            'hide_email': self.__update_hide_email,
            'hide_mobile_phone_number': self.__update_hide_mobile_phone,
            'hide_add_mobile_phone_number': self.__update_hide_add_mobile_phone,
            'hide_landline_phone_number': self.__update_hide_landline_phone,
            'hide_add_landline_phone_number': self.__update_hide_add_landline_phone,
            'hide_skype': self.__update_hide_skype,
        }


    @classmethod
    def get(cls, request):
        return cls.GetResponses.ok(request.user)


    def post(self, request):
        try:
            params = angular_post_parameters(request)
            field = params['f']
            value = params.get('v', '') # value can be empty
        except (ValueError, KeyError):
            return self.PostResponses.invalid_parameters()


        try:
            update_method = self.update_methods.get(field)
            return update_method(request.user, value)

        except KeyError:
            return self.PostResponses.invalid_parameters()



    def __update_first_name(self, user, name):
        if not name:
            return self.PostResponses.value_required()

        if not user.first_name == name:
            user.first_name = name
            user.save()

        return self.PostResponses.ok()


    def __update_last_name(self, user, name):
        if not name:
            return self.PostResponses.value_required()

        if not user.last_name == name:
            user.last_name = name
            user.save()

        return self.PostResponses.ok()


    def __update_email(self, user, email):
        if not email:
            return self.PostResponses.value_required()

        if user.email == email:
            # no validation and DB write
            return self.PostResponses.ok()

        try:
            validate_email(email)
        except ValidationError:
            return self.PostResponses.invalid_email()


        # check for duplicates
        if not Users.email_is_free(email):
            return self.PostResponses.duplicated_email()


        # todo: add email normalization here
        user.email = email
        user.save()
        return self.PostResponses.ok()


    def __update_work_email(self, user, email):
        if not email:
            # work email may be empty
            if user.work_email:
                user.work_email = ''
                user.save()

            return self.PostResponses.ok()

        if user.work_email == email:
            # no validation and DB write
            return self.PostResponses.ok()

        try:
            validate_email(email)
        except ValidationError:
            return self.PostResponses.invalid_email()

        # check for duplicates
        if not Users.email_is_free(email):
            return self.PostResponses.duplicated_email()

        # todo: add email normalization here
        user.work_email = email
        user.save()
        return self.PostResponses.ok()


    def __update_mobile_phone_number(self, user, phone):
        if not phone:
            return self.PostResponses.value_required()

        try:
            phone = phonenumbers.parse(phone)
            if not phonenumbers.is_valid_number(phone):
                raise ValidationError('Invalid number.')

        except (phonenumbers.NumberParseException, ValidationError):
            return self.PostResponses.invalid_phone()

        phone = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164)
        if user.mobile_phone == phone:
            # already the same
            return self.PostResponses.ok()

        # check for duplicates
        if not user.mobile_phone_number_is_free(phone):
            return self.PostResponses.duplicated_phone()

        if not user.mobile_phone == phone:
            user.mobile_phone = phone
            user.save()

        return self.PostResponses.ok()


    def __update_add_mobile_phone_number(self, user, phone):
        if not phone:
            # add mobile phone may be empty
            if user.add_mobile_phone:
                user.add_mobile_phone = ''
                user.save()

            return self.PostResponses.ok()


        try:
            phone = phonenumbers.parse(phone)
            if not phonenumbers.is_valid_number(phone):
                raise ValidationError('Invalid number.')

        except (phonenumbers.NumberParseException, ValidationError):
            return self.PostResponses.invalid_phone()


        phone = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164)
        if user.add_mobile_phone == phone:
            # already the same
            return self.PostResponses.ok()

        # check for duplicates
        if user.mobile_phone == phone or not user.mobile_phone_number_is_free(phone):
            return self.PostResponses.duplicated_phone()

        if not user.add_landline_phone == phone:
            user.add_mobile_phone = phone
            user.save()

        return self.PostResponses.ok()


    def __update_landline_phone_number(self, user, phone):
        if not phone:
            # landline phone may be empty
            if user.landline_phone:
                user.landline_phone = ''
                user.save()

            return self.PostResponses.ok()

        # check for duplicates
        if user.add_landline_phone or not user.mobile_phone_number_is_free(phone):
            return self.PostResponses.duplicated_phone()

        if not user.landline_phone == phone:
            user.landline_phone = phone
            user.save()

        return self.PostResponses.ok()


    def __update_add_landline_phone_number(self, user, phone):
        if not phone:
            # add landline phone may be empty
            if user.add_landline_phone:
                user.add_landline_phone = ''
                user.save()

            return self.PostResponses.ok()

        # check for duplicates
        if user.landline_phone == phone or not user.mobile_phone_number_is_free(phone):
            return self.PostResponses.duplicated_phone()

        if not user.add_landline_phone == phone:
            user.add_landline_phone = phone
            user.save()

        return self.PostResponses.ok()


    def __update_skype(self, user, login):
        if not user.skype == login:
            user.skype = login
            user.save()

        return self.PostResponses.ok()


    def __update_allow_call_request(self, user, allow):
        if allow not in (True, False):
            return self.PostResponses.invalid_value()

        preferences = user.preferences()
        if not preferences.allow_call_requests == allow:
            preferences.allow_call_requests = allow
            preferences.save()

        return self.PostResponses.ok()


    def __update_send_call_request_notifications_to_sid(self, user, sid):
        sid = int(sid)
        if sid not in Preferences.call_requests.values():
            return self.PostResponses.invalid_value()

        preferences = user.preferences()
        if not preferences.send_call_request_notifications_to_sid == sid:
            preferences.send_call_request_notifications_to_sid = sid
            preferences.save()

        return self.PostResponses.ok()


    def __update_allow_messaging(self, user, allow):
        if allow not in (True, False):
            return self.PostResponses.invalid_value()

        preferences = user.preferences()
        if not preferences.allow_messaging == allow:
            preferences.allow_messaging = allow
            preferences.save()

        return self.PostResponses.ok()


    def __update_send_message_notifications_to_sid(self, user, sid):
        sid = int(sid)
        if sid not in Preferences.messaging.values():
            return self.PostResponses.invalid_value()

        preferences = user.preferences()
        if not preferences.send_message_notifications_to_sid == sid:
            preferences.send_message_notifications_to_sid = sid
            preferences.save()

        return self.PostResponses.ok()


    def __update_hide_email(self, user, hide):
        if hide not in (True, False):
            return self.PostResponses.invalid_value()

        preferences = user.preferences()
        if not preferences.hide_email == hide:
            preferences.hide_email = hide
            preferences.save()

        return self.PostResponses.ok()


    def __update_hide_mobile_phone(self, user, hide):
        if hide not in (True, False):
            return self.PostResponses.invalid_value()

        preferences = user.preferences()
        if not preferences.hide_mobile_phone_number == hide:
            preferences.hide_mobile_phone_number = hide
            preferences.save()

        return self.PostResponses.ok()


    def __update_hide_add_mobile_phone(self, user, hide):
        if hide not in (True, False):
            return self.PostResponses.invalid_value()

        preferences = user.preferences()
        if not preferences.hide_add_mobile_phone_number == hide:
            preferences.hide_add_mobile_phone_number = hide
            preferences.save()

        return self.PostResponses.ok()


    def __update_hide_landline_phone(self, user, hide):
        if hide not in (True, False):
            return self.PostResponses.invalid_value()

        preferences = user.preferences()
        if not preferences.hide_landline_phone == hide:
            preferences.hide_landline_phone = hide
            preferences.save()

        return self.PostResponses.ok()


    def __update_hide_add_landline_phone(self, user, hide):
        if hide not in (True, False):
            return self.PostResponses.invalid_value()

        preferences = user.preferences()
        if not preferences.hide_add_landline_phone == hide:
            preferences.hide_add_landline_phone = hide
            preferences.save()

        return self.PostResponses.ok()


    def __update_hide_skype(self, user, hide):
        if hide not in (True, False):
            return self.PostResponses.invalid_value()

        preferences = user.preferences()
        if not preferences.hide_skype == hide:
            preferences.hide_skype = hide
            preferences.save()

        return self.PostResponses.ok()



class AvatarUpdate(CabinetView):
    class PostResponses(object):
        @staticmethod
        def ok(url):
            return HttpJsonResponse({
                'code': 0,
                'message': 'OK',
                'data': {
                    'url': url,
                }
            })

        @staticmethod
        def invalid_parameters():
            return HttpJsonResponse({
                'code': 1,
                'message': 'Image is too large.',
            })

        @staticmethod
        def too_large():
            return HttpJsonResponse({
                'code': 2,
                'message': 'Image is too large.',
            })

        @staticmethod
        def too_small():
            return HttpJsonResponse({
                'code': 3,
                'message': 'Image is too small.',
            })

        @staticmethod
        def unsupported_type():
            return HttpJsonResponse({
                'code': 4,
                'message': 'Image has unsupported type.',
            })

        @staticmethod
        def unknown_error():
            return HttpJsonResponse({
                'code': 100,
                'message': 'Unknown error.',
            })


    def post(self, request):
        # check if request is not empty
        image = request.FILES.get('file')
        if image is None:
            return self.PostResponses.invalid_parameters()

        try:
            request.user.avatar.update(image)

        except AvatarExceptions.ImageIsTooLarge:
            return self.PostResponses.too_large()

        except AvatarExceptions.ImageIsTooSmall:
            return self.PostResponses.too_small()

        except AvatarExceptions.UnsupportedImageType:
            return self.PostResponses.unsupported_type()

        except RuntimeException:
            return self.PostResponses.invalid_parameters()

        # seems to be ok
        return self.PostResponses.ok(request.user.avatar.url())