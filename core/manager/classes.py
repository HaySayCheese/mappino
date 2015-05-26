#coding=utf-8
from django.conf import settings
import mandrill
from collective.exceptions import  RuntimeException
from core.utils.jinja2_integration import templates



class ManagersNotifier(object):
    def __init__(self):
        self.__connect_to_mandrill()

    def send_photographer_request_notification(self, phone_number):
        """
        :param phone_number: User number, that needs photographers
        """
        html = templates.get_template('email/managers/new_photographer_request.html').render({
            'phone_number' : phone_number
        })
        if not self.__send_email(html, phone_number):
            raise RuntimeException('Email was not sent.')

    def __send_email(self, html, phone_number):
        def send():
            try:
                result = self.mandrill_client.messages.send(message=message, async=False)
            except Exception as e:
                pass
            return result[0]['status'] == 'sent'

        message = {
            'from_email': u'No-reply@mandrill-3702849048.mappino.com',
            'to': [{
                'type': u'to',
                'email': settings.MANAGER_EMAIL,
            }],
            'html': html,
            'headers': {
                'Reply-To': u'No-reply@mandrill-3702849048.mappino.com', # todo: add web hook here
            },
        }
        try:
            return send()
        except (mandrill.Error, IndexError):
            # При виникненні помилки - спробувати повторно з’єднатись з mandrill і надіслати заново.
            self.__connect_to_mandrill()
            return send()

    def __connect_to_mandrill(self):
        self.mandrill_client = mandrill.Mandrill(settings.MANDRILL_API_KEY)