#coding=utf-8
from django.conf import settings
import mandrill

from collective.exceptions import InvalidArgument, RuntimeException



class EmailDispatcher(object):
    def __init__(self):
        self.__connect_to_mandrill()


    def send_html_email(self, subject, html, addresses_list,
                        from_email='mail-dispatcher@mappino.com', from_name='mappino', reply_to=None):

        if not html:
            raise InvalidArgument('"html" can\'t be empty or None.')
        if not addresses_list:
            raise InvalidArgument('"addresses_list" can\'t be empty or None.')
        if not from_email:
            raise InvalidArgument('"from_email" can\'t be empty or None.')
        if not from_name:
            raise InvalidArgument('"from_name" can\'t be empty or None.')
        if subject is None:
            subject = u''

        message = {
        'from_email': from_email,
        'from_name': from_name,
        'to': [{
               'type': 'to',
               'email': address,
               } for address in addresses_list],
        'subject': subject,
        'html': html,
        }
        if reply_to is not None:
            message['headers'] = {
            'Reply-To': reply_to
            }

        if not self.__send_email(message):
            raise RuntimeException('Email can\'t be sent.')

        return True


    def __send_email(self, message):
        def send():
            result = self.mandrill_client.messages.send(message=message, async=True)
            return result[0]['status'] == 'sent'


        try:
            return send()
        except (mandrill.Error, IndexError):
            # if error occurred - lets try one more attempt
            self.__connect_to_mandrill()
            return send()


    def __connect_to_mandrill(self):
        self.mandrill_client = mandrill.Mandrill(settings.MANDRILL_API_KEY)