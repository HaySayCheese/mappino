# coding=utf-8
import mandrill

from django.conf import settings

from collective.exceptions import InvalidArgument, RuntimeException
from core.utils.jinja2_integration import templates


class EmailDispatcher(object):
    def __init__(self):
        self.__connect_to_mandrill()


    @staticmethod
    def __render_template(template_name, context):
        return templates.get_template(template_name).render(context)


    def send_html_email(self, template_name, context, subject, addresses_list,
                        from_email='mail-dispatcher@mappino.com', from_name='mappino', reply_to=None):

        html = self.__render_template(template_name, context)
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
            if not send():
                raise Exception() # lets try one more attempt
            else:
                return True

        except (mandrill.Error, IndexError):
            # if exception occurred - lets try one more attempt
            self.__connect_to_mandrill()
            return send()


    def __connect_to_mandrill(self):
        self.mandrill_client = mandrill.Mandrill(settings.MANDRILL_API_KEY)