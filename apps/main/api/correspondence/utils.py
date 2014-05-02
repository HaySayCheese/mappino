#coding=utf-8
from django.conf import settings
from django.core.exceptions import SuspiciousOperation

from collective.exceptions import InvalidArgument
from core.email_backend import email_sender
from core.publications.constants import HEAD_MODELS
from core.sms_dispatcher import notifications_sms_sender
from mappino.wsgi import templates



def send_new_message_notification(request, tid, hid, message, client_email, client_name=None):
	if not message:
		raise InvalidArgument('Message can not be empty.')

	model = HEAD_MODELS.get(tid)
	if model is None:
		raise InvalidArgument('Invalid publication tid.')

	publications = model.objects.filter(id = hid).only('id', 'owner', 'state_sid', 'body__title')[:1]
	if not publications:
		raise InvalidArgument('Invalid publication hid.')
	publication = publications[0]


	# security checks
	if not publication.is_published():
		raise SuspiciousOperation('Attempt to comment not published publication.')

	if not publication.body.title:
		raise SuspiciousOperation('Attempt to comment publication without title.')


	# sending email
	html = templates.get_template('email/notifications/incoming_message.html').render({
		'client_name': client_name,
	    'publication': {
		    'title': publication.body.title,
	        'url': settings.REDIRECT_DOMAIN + '/cabinet/#!/publications/published/{0}:{1}'.format(tid, hid)
	    },
	    'message': message
	})
	email_sender.send_html_email(
		subject = u'Сообщение от заинтересованного клиента ({0})'.format(client_email), # tr
	    html = html,
	    addresses_list = [publication.owner.contact_email()],
	    reply_to = client_email
	)


	# sending sms notification
	notifications_sms_sender.incoming_message(publication.owner.mobile_phone, request)



def send_new_call_request_notification(self, request, tid, hid, client_number, client_name=None):
	# todo: додати перевірку, чи недсилався недавно рієлтору запит на дзвінок на цей номер
	# можна використати інтервал в 2-3 години перед наступним повідомленням.

	if not client_number:
		raise InvalidArgument('Phone number can not be empty.')

	model = HEAD_MODELS.get(tid)
	if model is None:
		raise InvalidArgument('Invalid publication tid.')

	publications = model.objects.filter(id = hid).only('id', 'owner', 'state_sid', 'body__title')[:1]
	if not publications:
		raise InvalidArgument('Invalid publication hid.')
	publication = publications[0]


	# security checks
	if not publication.is_published():
		raise SuspiciousOperation('Attempt to comment not published publication.')
	if not publication.body.title:
		raise SuspiciousOperation('Attempt to comment publication without title.')


	# sending email
	html = templates.get_template('email/notifications/incoming_call_request.html').render({
		'client_name': client_name,
	    'phone_number': client_number,
	    'publication': {
		    'title': publication.body.title,
	        'url': settings.REDIRECT_DOMAIN + '/cabinet/#!/publications/published/{0}:{1}'.format(tid, hid)
	    },
	})
	email_sender.send_html_email(
		subject = u'Запрос обратного звонка ({0})'.format(client_number), # tr
	    html = html,
	    addresses_list = [publication.owner.contact_email()],
	)


	# sending sms notification
	notifications_sms_sender.incoming_call_request(publication.owner.mobile_phone, client_number, request)