# coding=utf-8
from django.core.exceptions import SuspiciousOperation
from core.notifications.mail_dispatcher.sellers import SellersMailDispatcher
from core.notifications.sms_dispatcher.sellers import SellersSMSDispatcher
from core.users.constants import Preferences


class SellersNotificationsManager(object):
    @classmethod
    def notify_about_incoming_call_request(cls, request, publication, client_number, client_name=None):
        """
        Аналізує власника оголошення publication, та обирає спосіб доставки повідомлення,
        після чого надсилає повідомлення.

        :param request:
            <передаєтьсья в нижчу логіку>

        :param tid: id типу оголошення.
        :param publication: head-запис оголошення, власнику якого слід надіслати повідомлення.
        :param client_number: номер мобільного телефону у міжнародному форматі.
        :param client_name: контактна особа.
        """
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
                SellersMailDispatcher.send_email_about_incoming_call_request(tid, publication, client_number, client_name)
            except Exception as e:
                # catch all errors here
                error = e


            if error is not None:
                raise error

        else:
            raise ValueError('Invalid send method sid')


    @classmethod
    def notify_about_publication_blocked_by_moderator(cls, user):
        SellersSMSDispatcher.send_sms_about_publication_blocked_by_moderator(user.mobile)
