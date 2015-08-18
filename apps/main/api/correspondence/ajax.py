#coding=utf-8
from django.core.exceptions import SuspiciousOperation
from django.views.generic import View

from collective.decorators.ajax import json_response, json_response_bad_request, json_response_not_found
from collective.exceptions import InvalidArgument, RuntimeException
from collective.methods.request_data_getters import angular_parameters
from core.notifications.mail_dispatcher.sellers import SellersMailDispatcher
from core.notifications.sms_dispatcher.sellers import SellersSMSDispatcher
from core.publications.constants import HEAD_MODELS
from core.users.constants import Preferences


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
                SellersSMSDispatcher.send_sms_about_incoming_call_request(
                    request, publication.owner.mobile_phone, params['phone_number'], params.get('name', ''))

                cls.__send_notification_about_new_call_request(
                    request, publication, params['phone_number'], params.get('name', ''))

            except ValueError:
                return cls.PostResponses.invalid_parameters()


            return cls.PostResponses.ok()


        @staticmethod
        def __send_notification_about_new_call_request(request, publication, client_number, client_name=None):
            """
            Аналізує власника оголошення publication, та обирає спосіб доставки повідомлення,
            після чого надсилає повідомлення.

            :param request:
                <передаєтьсья в нижчу логіку>

            :param publication: head-запис оголошення, власнику якого слід надіслати повідомлення.
            :param client_number: номер мобільного телефону у міжнародному форматі.
            :param client_name: контактна особа.
            """

            # todo: додати перевірку, чи не надсилався недавно рієлтору запит на дзвінок на цей номер
            # можна використати інтервал в 2-3 години перед наступним повідомленням.

            # checks
            try:
                int(client_number)
            except ValueError:
                raise InvalidArgument('Invalid phone number.')


            preferences = publication.owner.preferences
            if not preferences.allow_call_requests:
                raise SuspiciousOperation('Attempt to send call request to the realtor that was disabled this future.')


            # choosing delivery method for the notification
            # and sending the message
            method = preferences.send_call_request_notifications_to_sid
            if method == Preferences.call_requests.sms():
                SellersSMSDispatcher.send_sms_about_incoming_call_request(request, publication.owner.mobile_phone, client_number, client_name)

            elif method == Preferences.call_requests.email():
                SellersMailDispatcher.send_email_about_incoming_call_request(publication, client_number, client_name)

            elif method == Preferences.call_requests.sms_and_email():
                # if delivering through one of the methods wasn't successful —
                # delivering by other methods should not break,
                # but on the end of the method the error should be raised.

                error = None
                try:
                    SellersSMSDispatcher.send_sms_about_incoming_call_request(request, publication.owner.mobile_phone, client_number, client_name)

                except Exception as e:
                    # catch all errors here
                    error = e


                try:
                    SellersMailDispatcher.send_email_about_incoming_call_request(publication, client_number, client_name)

                except Exception as e:
                    # catch all errors here
                    error = e


                if error is not None:
                    raise error

            else:
                raise RuntimeException('Invalid send method sid.')




#
# class SendMessageFromClient(View):
#
#
#
#     post_codes = {
#         'Ok': {
#             'code': 0,
#         },
#         'invalid_hash_id': {
#             'code': 1
#         },
#         'invalid_parameters': {
#             'code': 2
#         },
#         'invalid_tid': {
#             'code': 3
#         },
#     }
#
#
#     def post(self, request, *args):
#         try:
#             tid, hash_hid = args[0].split(':')
#             if (tid is None) or (hash_hid is None):
#                 raise InvalidHttpParameter()
#
#         except (
#             IndexError, # args doesn't contains required params
#             InvalidHttpParameter, # tid or hash_id is None
#         ):
#             return HttpResponseBadRequest(
#                 json.dumps(self.post_codes['invalid_parameters']), content_type='application/json')
#
#
#         try:
#             tid = int(tid)
#             if tid not in OBJECTS_TYPES.values():
#                 raise InvalidHttpParameter()
#
#         except (
#             InvalidHttpParameter, # tid is incorrect object type
#             ValueError, # tid is not an int
#         ):
#             return HttpResponseBadRequest(
#                 json.dumps(self.post_codes['invalid_tid']), content_type='application/json')
#
#
#         try:
#             params = angular_parameters(request, ['email', 'message'])
#         except (
#             ValueError, # email or message is not specified
#         ):
#             return HttpResponseBadRequest(json.dumps(
#                 self.post_codes['invalid_parameters']), content_type='application/json')
#
#
#         model = HEAD_MODELS.get(tid)
#         try:
#             publication = model.objects.filter(hash_id = hash_hid).only('id', 'owner', 'state_sid', 'body__title')[:1][0]
#         except (
#             IndexError, # models doesn't contains record with exact hash
#         ):
#             return HttpResponse( # request semantically is correct
#                 json.dumps(self.post_codes['invalid_parameters']), content_type='application/json')
#
#
#         # security checks
#         if not publication.is_published():
#             raise SuspiciousOperation('Attempt to comment unpublished publication.')
#
#
#         try:
#             send_notification_about_new_message(
#                 request, tid, publication,
#
#                 params['message'],
#                 params['email'],
#                 params.get('name', '') # is not required
#              )
#
#         except (
#             InvalidArgument, # message is empty
#         ):
#             return HttpResponseBadRequest(
#                 json.dumps(self.post_codes['invalid_parameters']), content_type='application/json')
#
#         return HttpResponse(json.dumps(self.post_codes['Ok']), content_type="application/json")
#
#
#
# class SendCallRequestFromClient(View):
#     post_codes = {
#         'Ok': {
#             'code': 0,
#         },
#         'invalid_hash_id': {
#             'code': 1
#         },
#         'invalid_parameters': {
#             'code': 2
#         }
#     }
#
#     def post(self, request, *args):
#         try:
#             tid, hash_hid = args[0].split(':')
#             if (tid is None) or (hash_hid is None):
#                 raise InvalidHttpParameter()
#
#         except (
#             IndexError, # args doesn't contains required params
#             InvalidHttpParameter, # tid or hash_id is None
#         ):
#             return HttpResponseBadRequest(
#                 json.dumps(self.post_codes['invalid_parameters']), content_type='application/json')
#
#
#         try:
#             tid = int(tid)
#             if tid not in OBJECTS_TYPES.values():
#                 raise InvalidHttpParameter()
#
#         except (
#             InvalidHttpParameter, # tid is incorrect object type
#             ValueError, # tid is not an int
#         ):
#             return HttpResponseBadRequest(
#                 json.dumps(self.post_codes['invalid_tid']), content_type='application/json')
#
#
#         try:
#             params = angular_parameters(request, ['phone_number'])
#         except (
#             ValueError, # email or message is not specified
#         ):
#             return HttpResponseBadRequest(json.dumps(
#                 self.post_codes['invalid_parameters']), content_type='application/json')
#
#
#         model = HEAD_MODELS.get(tid)
#         try:
#             publication = model.objects.filter(hash_id = hash_hid).only('id', 'owner', 'state_sid', 'body__title')[:1][0]
#         except (
#             IndexError, # models doesn't contains record with exact hash
#         ):
#             return HttpResponse( # request semantically is correct
#                 json.dumps(self.post_codes['invalid_parameters']), content_type='application/json')
#
#
#         # security checks
#         if not publication.is_published():
#             raise SuspiciousOperation('Attempt to comment unpublished publication.')
#
#
#         try:
#             send_notification_about_new_call_request(
#                 request,
#                 tid,
#                 publication,
#                 params['phone_number'],
#                 params.get('name', '') # not required
#             )
#         except InvalidArgument:
#             return HttpResponseBadRequest(
#                 json.dumps(self.post_codes['invalid_parameters']), content_type='application/json')
#
#
#         return HttpResponse(
#             json.dumps(self.post_codes['Ok']), content_type="application/json")

#
# def send_notification_about_new_call_request(request, tid, publication, client_number, client_name=None):
#     """
#     Аналізує налаштування ріелтора, що є власником оголошення publication,
#     та обирає спосіб доставки повідомлення, після чого надсилає повідомлення.
#
#     :param request:
#         <передаєтьсья в нижчу логіку>
#
#     :param tid: id типу оголошення.
#     :param publication: head-запис оголошення, власнику якого слід надіслати повідомлення.
#     :param client_number: номер мобільного телефону у міжнародному форматі.
#     :param client_name: контактна особа.
#     """
#
#     # todo: додати перевірку, чи не надсилався недавно рієлтору запит на дзвінок на цей номер
#     # можна використати інтервал в 2-3 години перед наступним повідомленням.
#
#     # checks
#     try:
#         int(client_number)
#     except ValueError:
#         raise InvalidArgument('Invalid phone number.')
#
#
#     preferences = publication.owner.preferences()
#     if not preferences.allow_call_requests:
#         raise SuspiciousOperation('Attempt to send call request to the realtor that was disabled this future.')
#
#
#     # choosing delivery method for the notification
#     # and sending the message
#     method = preferences.send_call_request_notifications_to_sid
#     if method == Preferences.call_requests.sms():
#         CallRequestsHanlder.send_sms_notification(request, publication, client_number, client_name)
#
#     elif method == Preferences.call_requests.email():
#         CallRequestsHanlder.send_email_notification(tid, publication, client_number, client_name)
#
#     elif method == Preferences.call_requests.sms_and_email():
#         # if delivering through one of the methods wasn't successful —
#         # delivering by other methods should not break,
#         # but on the end of the method the error should be raised.
#
#         error = None
#         try:
#             if not CallRequestsHanlder.send_sms_notification(request, publication, client_number, client_name):
#                 raise RuntimeException('Message can\'t be delivered.')
#
#         except Exception as e:
#             # catch all errors here
#             error = e
#
#
#         try:
#             if not CallRequestsHanlder.send_email_notification(tid, publication, client_number, client_name):
#                 raise RuntimeException('Message can\'t be delivered.')
#
#         except Exception as e:
#             # catch all errors here
#             error = e
#
#
#         if error is not None:
#             raise error
#
#     else:
#         raise RuntimeException('Invalid send method sid.')