# coding=utf-8
import phonenumbers

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from apps.views_base import CabinetView
from collective.decorators.ajax import json_response
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
            if user.mobile_phone:
                mobile_phone =  phonenumbers.parse(user.mobile_phone)
                mobile_phone_code = str(mobile_phone.country_code)
                mobile_phone_number = phonenumbers\
                    .format_number(mobile_phone, phonenumbers.PhoneNumberFormat.NATIONAL)\
                    .replace(' ', '')[1:] # зайві пробіли і початкові нулі видаляються

            else:
                mobile_phone_code = None
                mobile_phone_number = None


            if user.add_mobile_phone:
                add_mobile_phone =  phonenumbers.parse(user.add_mobile_phone)
                add_mobile_phone_code = str(add_mobile_phone.country_code)
                add_mobile_phone_number = phonenumbers\
                    .format_number(add_mobile_phone, phonenumbers.PhoneNumberFormat.NATIONAL)\
                    .replace(' ', '')[1:] # зайві пробіли і початкові нулі видаляються

            else:
                if mobile_phone_code:
                    add_mobile_phone_code = mobile_phone_code
                else:
                    add_mobile_phone_code = None
                add_mobile_phone_number = None


            # Стаціонарні і робочі телефони ніяк не валідуються
            landline_phone_number = user.landline_phone if user.landline_phone else ''
            add_landline_phone_number = user.add_landline_phone if user.add_landline_phone else ''



            if user.is_moderator:
                return HttpJsonResponse({
                    'code': 0,
                    'message': 'OK',
                    'data': {
                        'account': {
                            'first_name': user.first_name or None,
                            'last_name': user.last_name or None,
                            'email': user.email or None,
                            'work_email': user.work_email or '',
                            'skype': user.skype or '',
                            'avatar_url': user.avatar.url() or '',

                            'mobile_code': '+{0}'.format(mobile_phone_code) if mobile_phone_code else None,
                            'mobile_phone': mobile_phone_number or None,
                            'add_mobile_code': '+{0}'.format(add_mobile_phone_code) if add_mobile_phone_code else None,
                            'add_mobile_phone': add_mobile_phone_number or None,

                            'landline_phone': landline_phone_number or None,
                            'add_landline_phone': add_landline_phone_number or None,
                        },
                    }
                })

            else:
                return HttpJsonResponse({
                    'code': 0,
                    'message': 'OK',
                    'data': {
                        'account': {
                            'first_name': user.first_name or None,
                            'last_name': user.last_name or None,
                            'email': user.email or None,
                            'work_email': user.work_email or None,
                            'skype': user.skype or None,
                            'avatar_url': user.avatar.url() or None,

                            'mobile_code': '+{0}'.format(mobile_phone_code) if mobile_phone_code else None,
                            'mobile_phone': mobile_phone_number or None,
                            'add_mobile_code': '+{0}'.format(add_mobile_phone_code) if add_mobile_phone_code else None,
                            'add_mobile_phone': add_mobile_phone_number or None,

                            'landline_phone': landline_phone_number or None,
                            'add_landline_phone': add_landline_phone_number or None,
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
                            'send_call_request_notifications_to_sid': str(preferences.send_call_request_notifications_to_sid),
                            'send_message_notifications_to_sid': str(preferences.send_message_notifications_to_sid),
                        }
                    }
                })


    class PostResponses(object):
        @staticmethod
        @json_response
        def ok(value=None):
            return {
                'code': 0,
                'message': 'OK',
                'data': {
                    'value': value
                }
            }


        @staticmethod
        @json_response
        def value_required():
            return {
                'code': 1,
                'message': 'Value is required.'
            }


        @staticmethod
        @json_response
        def invalid_value():
            return {
                'code': 2,
                'message': 'Value is invalid.'
            }


        @staticmethod
        @json_response
        def duplicated_value():
            return {
                'code': 3,
                'message': 'Value is duplicated.'
            }


        @staticmethod
        @json_response
        def invalid_parameters():
            return {
                'code': 100,
                'message': 'Request does not contains parameters or one of them is invalid.'
            }


    def __init__(self):
        super(AccountView, self).__init__()
        self.update_methods = {
            'first_name': self.__update_first_name,
            'last_name': self.__update_last_name,
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
            field, value = params.iteritems().next()
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
            user.first_name = name.capitalize()
            user.save()

        return self.PostResponses.ok(user.first_name)


    def __update_last_name(self, user, name):
        if not name:
            return self.PostResponses.value_required()

        if not user.last_name == name:
            user.last_name = name.capitalize()
            user.save()

        return self.PostResponses.ok(user.last_name)


    def __update_email(self, user, email):
        if not email:
            return self.PostResponses.value_required()

        if user.email == email:
            # no validation and DB write
            return self.PostResponses.ok()

        try:
            validate_email(email)
        except ValidationError:
            return self.PostResponses.invalid_value()


        # check for duplicates
        if not Users.email_is_free(email):
            return self.PostResponses.duplicated_value()


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
            return self.PostResponses.invalid_value()

        # check for duplicates
        if not Users.email_is_free(email):
            return self.PostResponses.duplicated_value()

        # todo: add email normalization here
        user.work_email = email
        user.save()
        return self.PostResponses.ok()


    def __update_mobile_phone_number(self, user, phone):
        return self.PostResponses.ok()

        # note: mobile phone temporary can not be changed.

        # if not phone:
        #     return self.PostResponses.value_required()
        #
        #
        # try:
        #     phone = Users.objects.parse_phone_number(phone)
        # except ValueError:
        #     return self.PostResponses.invalid_value()
        #
        #
        # if user.mobile_phone == phone:
        #     # already the same
        #     return self.PostResponses.ok()
        #
        # # check for duplicates
        # if not user.mobile_phone_number_is_free(phone):
        #     return self.PostResponses.duplicated_value()
        #
        # if not user.mobile_phone == phone:
        #     user.mobile_phone = phone
        #     user.save()
        #
        # return self.PostResponses.ok()


    def __update_add_mobile_phone_number(self, user, phone):
        if not phone:
            # add mobile phone may be empty
            if user.add_mobile_phone:
                user.add_mobile_phone = ''
                user.save()

            return self.PostResponses.ok()


        try:
            phone =Users.objects.parse_phone_number(phone)
        except ValueError:
            return self.PostResponses.invalid_value()


        if user.add_mobile_phone == phone:
            # already the same
            return self.PostResponses.ok()

        # check for duplicates
        if user.mobile_phone == phone or not user.mobile_phone_number_is_free(phone):
            return self.PostResponses.duplicated_value()

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

        # note: several users may have common landline phone,
        # so wee need to check for duplication only with other landline_phone
        if user.add_landline_phone == phone:
            return self.PostResponses.duplicated_value()

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

        # note: several users may have common landline phone,
        # so wee need to check for duplication only with other landline_phone
        if user.landline_phone == phone:
            return self.PostResponses.duplicated_value()

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

        preferences = user.preferences
        if not preferences.allow_call_requests == allow:
            preferences.allow_call_requests = allow
            preferences.save()

        return self.PostResponses.ok()


    def __update_send_call_request_notifications_to_sid(self, user, sid):
        sid = int(sid)
        if sid not in Preferences.call_requests.values():
            return self.PostResponses.invalid_value()

        preferences = user.preferences
        if not preferences.send_call_request_notifications_to_sid == sid:
            preferences.send_call_request_notifications_to_sid = sid
            preferences.save()

        return self.PostResponses.ok()


    def __update_allow_messaging(self, user, allow):
        if allow not in (True, False):
            return self.PostResponses.invalid_value()

        preferences = user.preferences
        if not preferences.allow_messaging == allow:
            preferences.allow_messaging = allow
            preferences.save()

        return self.PostResponses.ok()


    def __update_send_message_notifications_to_sid(self, user, sid):
        sid = int(sid)
        if sid not in Preferences.messaging.values():
            return self.PostResponses.invalid_value()

        preferences = user.preferences
        if not preferences.send_message_notifications_to_sid == sid:
            preferences.send_message_notifications_to_sid = sid
            preferences.save()

        return self.PostResponses.ok()


    def __update_hide_email(self, user, hide):
        if hide not in (True, False):
            return self.PostResponses.invalid_value()

        preferences = user.preferences
        if not preferences.hide_email == hide:
            preferences.hide_email = hide
            preferences.save()

        return self.PostResponses.ok()


    def __update_hide_mobile_phone(self, user, hide):
        if hide not in (True, False):
            return self.PostResponses.invalid_value()

        preferences = user.preferences
        if not preferences.hide_mobile_phone_number == hide:
            preferences.hide_mobile_phone_number = hide
            preferences.save()

        return self.PostResponses.ok()


    def __update_hide_add_mobile_phone(self, user, hide):
        if hide not in (True, False):
            return self.PostResponses.invalid_value()

        preferences = user.preferences
        if not preferences.hide_add_mobile_phone_number == hide:
            preferences.hide_add_mobile_phone_number = hide
            preferences.save()

        return self.PostResponses.ok()


    def __update_hide_landline_phone(self, user, hide):
        if hide not in (True, False):
            return self.PostResponses.invalid_value()

        preferences = user.preferences
        if not preferences.hide_landline_phone == hide:
            preferences.hide_landline_phone = hide
            preferences.save()

        return self.PostResponses.ok()


    def __update_hide_add_landline_phone(self, user, hide):
        if hide not in (True, False):
            return self.PostResponses.invalid_value()

        preferences = user.preferences
        if not preferences.hide_add_landline_phone == hide:
            preferences.hide_add_landline_phone = hide
            preferences.save()

        return self.PostResponses.ok()


    def __update_hide_skype(self, user, hide):
        if hide not in (True, False):
            return self.PostResponses.invalid_value()

        preferences = user.preferences
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


    class DeleteCodes(object):
        @staticmethod
        @json_response
        def ok():
            return {
                'code': 0,
                'message': 'OK',
            }


    @classmethod
    def post(cls, request):
        # check if request is not empty
        image = request.FILES.get('file')
        if image is None:
            return cls.PostResponses.invalid_parameters()

        try:
            request.user.avatar.update(image)

        except AvatarExceptions.ImageIsTooLarge:
            return cls.PostResponses.too_large()

        except AvatarExceptions.ImageIsTooSmall:
            return cls.PostResponses.too_small()

        except AvatarExceptions.UnsupportedImageType:
            return cls.PostResponses.unsupported_type()

        except RuntimeException:
            return cls.PostResponses.invalid_parameters()

        # seems to be ok
        return cls.PostResponses.ok(request.user.avatar.url())


    @classmethod
    def delete(cls, request):
        request.user.avatar.remove()
        return cls.DeleteCodes.ok()