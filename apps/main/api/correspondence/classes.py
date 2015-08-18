# coding=utf-8
from django.conf import settings

from core.notifications.mail_dispatcher import email_sender
from core.utils.jinja2_integration import templates


# class MessagesHandler(object):
#     @staticmethod
#     def send_email(tid, publication, email, name, message):
#         template = templates.get_template('email/notifications/incoming_message.html')
#         html = template.render({
#             'client_name': name,
#             'publication': {
#                 'title': publication.body.title,
#                 'url': settings.REDIRECT_DOMAIN_URL + '/cabinet/#!/publications/published/{0}:{1}'.format(
#                     tid, publication.hash_id)
#             },
#             'message': message
#         })
#
#         return email_sender.send_html_email(
#             subject = u'Сообщение от заинтересованного клиента ({0})'.format(name)
#                 if name else u'Сообщение от заинтересованного клиента', # tr # note: name may be omitted
#
#             html = html,
#             addresses_list = [publication.owner.contact_email()],
#             reply_to = email
#         )
#
#
# class CallRequestsHandler(object):
#     @staticmethod
#     def send_email_notification(tid, publication, number, name):
#         template = templates.get_template('email/notifications/incoming_call_request.html')
#         html = template.render({
#             'client_name': name,
#             'phone_number': number,
#             'publication': {
#                 'title': publication.body.title,
#                 'url': settings.REDIRECT_DOMAIN_URL + '/cabinet/#!/publications/published/{0}:{1}'.format(
#                     tid, publication.hash_id)
#             },
#         })
#         return email_sender.send_html_email(
#             subject = u'Запрос обратного звонка ({0})'.format(number), # tr
#             html = html,
#             addresses_list = [publication.owner.contact_email()],
#         )