#coding=utf-8
from django.core.exceptions import SuspiciousOperation
from django.views.generic import View

from collective.decorators.ajax import json_response, json_response_bad_request, json_response_not_found
from collective.methods.request_data_getters import angular_parameters
from core.notifications.mail_dispatcher.sellers import SellersMailDispatcher
from core.notifications.sms_dispatcher.exceptions import ResourceThrottled
from core.notifications.sms_dispatcher.sellers import SellersSMSDispatcher
from core.publications.constants import HEAD_MODELS
from core.users.constants import Preferences
from core.notifications.sms_dispatcher.checkers import MessageChecker, CallRequestChecker


class ClientNotificationsHandler(object):
    class MessagesHandler(View):
        class PostResponses(object):

            @staticmethod
            @json_response
            def ok():
                return {
                    'code': 0,
                    'message': 'OK',
                }


            @staticmethod
            @json_response_bad_request
            def invalid_tid():
                return {
                    'code': 1,
                    'message': 'Request contains invalid tid.',
                }


            @staticmethod
            @json_response_bad_request
            def invalid_hash_id():
                return {
                    'code': 2,
                    'message': 'Request contains invalid hash id.',
                }


            @staticmethod
            @json_response_bad_request
            def invalid_parameters():
                return {
                    'code': 3,
                    'message': 'Request contains invalid parameters.',
                }


            @staticmethod
            @json_response_not_found
            def no_such_publication():
                return {
                    'code': 4,
                    'message': 'There is no publication with such id.',
                }


            @staticmethod
            @json_response
            def request_throttled():
                return {
                    'code': 200,
                    'message': 'Request was throttled.'
                }


        @classmethod
        def post(cls, request, *args):
            try:
                tid, hash_hid = int(args[0]), args[1]
                model = HEAD_MODELS[tid]
            except (ValueError, IndexError, KeyError):
                return cls.PostResponses.invalid_parameters()


            try:
                params = angular_parameters(request, ['email', 'message'])
            except (ValueError, ):
                return cls.PostResponses.invalid_parameters()


            try: # todo: test if no params
                publication = model.queryset_by_hash_id(hash_hid)\
                    .only('id', 'owner', 'state_sid', 'body__title')\
                    [:1][0]
            except (IndexError, ):
                return cls.PostResponses.no_such_publication()


            # security checks
            if not publication.is_published():
                raise SuspiciousOperation('Attempt to comment unpublished publication.')


            try:
                cls.__send_notification_about_new_message(
                    request, publication, params['message'], params['email'], params.get('name', '') # is not required
                )

            except ValueError:
                return cls.PostResponses.invalid_parameters()

            except ResourceThrottled:
                return cls.PostResponses.request_throttled()


            return cls.PostResponses.ok()


        @staticmethod
        def __send_notification_about_new_message(request, publication, message, client_email, client_name=None):
            """
            Аналізує налаштування ріелтора, що є власником оголошення publication,
            та обирає спосіб доставки повідомлення, після чого надсилає повідомлення.

            :param request:
                <передаєтьсья в нижчу логіку>

            :param publication: head-запис оголошення, власнику якого слід надіслати повідомлення.
            :param message: повідомлення, яке слід надіслати.
                WARN: повідомлення message буде надіслано лише за допомогою ел. пошти.
                В SMS воно надіслане не буде, а натомість буде надіслано стандартний текст з проханням перевірити пошту.

            :param client_email: ел. адреса людини, яка залишає повідомлення.
                На дану адресу будуть напрявлятись відповіді рієлтора.

            :param client_name: контактна особа.
            """

            # checks
            if not message:
                raise ValueError('Invalid message: {0}'.format(message))
            if not client_email:
                raise ValueError('Invalid email: {0}'.format(client_email))

            # note: client name may be omitted.


            preferences = publication.owner.preferences
            if not preferences.allow_messaging:
                raise SuspiciousOperation('Attempt to send message to the realtor that was disabled this future.')


            # choosing delivery method for the notification
            # and sending the notification
            method = preferences.send_message_notifications_to_sid
            if method == Preferences.messaging.email():
                SellersMailDispatcher.send_message_email(publication, client_email, client_name, message)

            elif method == Preferences.messaging.sms_and_email():
                # if delivering by one of the methods wasn't successful —
                # delivering by other methods should not break,
                # but on the end of the method the error should be raised.

                error = None
                try:
                    MessageChecker.check_for_throttling(request, publication.owner.mobile_phone)
                    if not SellersSMSDispatcher.send_sms_about_incoming_email(request, publication.owner.mobile_phone):
                        raise RuntimeError('Email can not be sent.')


                except Exception as e:
                    # catch all errors here
                    error = e


                try:
                    if not SellersMailDispatcher.send_message_email(publication, client_email, client_name, message):
                        raise RuntimeError('Email can not be sent.')

                except Exception as e:
                    # catch all errors here
                    error = e


                if error is not None:
                    raise error

            else:
                # method is unknown
                raise RuntimeError('Invalid send method sid.')


    class CallRequestsHandler(View):
        class PostResponses(object):

            @staticmethod
            @json_response
            def ok():
                return {
                    'code': 0,
                    'message': 'OK',
                }


            @staticmethod
            @json_response_bad_request
            def invalid_tid():
                return {
                    'code': 1,
                    'message': 'Request contains invalid tid.',
                }


            @staticmethod
            @json_response_bad_request
            def invalid_hash_id():
                return {
                    'code': 2,
                    'message': 'Request contains invalid hash id.',
                }


            @staticmethod
            @json_response_bad_request
            def invalid_parameters():
                return {
                    'code': 3,
                    'message': 'Request contains invalid parameters.',
                }


            @staticmethod
            @json_response_not_found
            def no_such_publication():
                return {
                    'code': 4,
                    'message': 'There is no publication with such id.',
                }


            @staticmethod
            @json_response
            def request_throttled():
                return {
                    'code': 200,
                    'message': 'Request was throttled.'
                }


        @classmethod
        def post(cls, request, *args):
            try:
                tid, hash_hid = int(args[0]), args[1]
                model = HEAD_MODELS[tid]
            except (ValueError, IndexError, KeyError):
                return cls.PostResponses.invalid_parameters()


            try:
                params = angular_parameters(request, ['phone_number']) # note: name may be omitted
            except (ValueError, ):
                return cls.PostResponses.invalid_parameters()


            try: # todo: test if no params
                publication = model.queryset_by_hash_id(hash_hid)\
                    .only('id', 'owner', 'state_sid', 'body__title')\
                    [:1][0]
            except (IndexError, ):
                return cls.PostResponses.no_such_publication()


            # security checks
            if not publication.is_published():
                raise SuspiciousOperation('Attempt to comment unpublished publication.')


            try:
                CallRequestChecker.check_for_throttling(
                    request, publication.owner.mobile_phone, params['phone_number'])
            except ResourceThrottled:
                return cls.PostResponses.request_throttled()

            try:
                SellersSMSDispatcher.send_sms_about_incoming_call_request(
                    request, publication.owner.mobile_phone, params['phone_number'], params.get('name', ''))
            except ValueError:
                return cls.PostResponses.invalid_parameters()


            return cls.PostResponses.ok()