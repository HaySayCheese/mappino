# coding=utf-8
from django.conf import settings

from core.users.notifications.mail_dispatcher import email_sender


class SellersMailDispatcher(object):
    @staticmethod
    def send_email_about_incoming_call_request(publication, number, name):
        email = publication.owner.contact_email()
        if not email:
            raise RuntimeError('It seems that seller does not specified contact email.')


        return email_sender.send_html_email(
            template_name = 'email/notifications/incoming_call_request.html',
            context = {
                'client_name': name,
                'phone_number': number,
                'publication': {
                    'url': settings.REDIRECT_DOMAIN_URL + '/cabinet/#!/publications/published/{0}:{1}'.format(
                         publication.tid, publication.hash_id)
                },
            },
            subject = u'Запрос обратного звонка ({0})'.format(number), # tr
            addresses_list = [email, ],
        )


    @staticmethod
    def send_message_email(publication, reply_email, name, message):
        subject = u'Сообщение от заинтересованного клиента ({0})'.format(name) \
            if name else u'Сообщение от заинтересованного клиента', # tr # note: name may be omitted


        email = publication.owner.contact_email()
        if not email:
            raise RuntimeError('It seems that seller does not specified contact email.')


        return email_sender.send_html_email(
            template_name = 'email/notifications/incoming_message.html',
            context = {
                'client_name': name,
                'publication': {
                    'url': settings.REDIRECT_DOMAIN_URL + '/cabinet/#!/publications/published/{0}:{1}'.format(
                        publication.tid, publication.hash_id)
                },
                'message': message
            },
            subject = subject,
            addresses_list = [email, ],
            reply_to=reply_email
        )