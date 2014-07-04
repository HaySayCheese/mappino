#coding=utf-8
import string
from django.conf import settings
from django.core.exceptions import SuspiciousOperation

from collective.exceptions import InvalidArgument, RuntimeException
from core.email_backend import email_sender
from core.publications.constants import HEAD_MODELS
from core.sms_dispatcher import notifications_sms_sender
from core.users.constants import Preferences
from mappino.wsgi import templates



def send_new_message_notification(request, tid, hash_hid, message, client_email, client_name=None):
	def send_email_notification():
		template = templates.get_template('email/notifications/incoming_message.html')
		html = template.render({
			'client_name': client_name,
		    'publication': {
			    'title': publication.body.title,
		        'url': settings.REDIRECT_DOMAIN + '/cabinet/#!/publications/published/{0}:{1}'.format(tid, hash_hid)
		    },
		    'message': message
		})
		email_sender.send_html_email(
			subject = u'Сообщение от заинтересованного клиента ({0})'.format(client_email), # tr
		    html = html,
		    addresses_list = [publication.owner.contact_email()],
		    reply_to = client_email
		)


	def send_sms_notification():
		notifications_sms_sender.incoming_message(publication.owner.mobile_phone, request)



	if not message:
		raise InvalidArgument('Message can not be empty.')

	model = HEAD_MODELS.get(tid)
	if model is None:
		raise InvalidArgument('Invalid publication tid.')

	publications = model.objects.filter(hash_id = hash_hid).only('id', 'owner', 'state_sid', 'body__title')[:1]
	if not publications:
		raise InvalidArgument('Invalid publication hid.')
	publication = publications[0]


	# security checks
	if not publication.is_published():
		raise SuspiciousOperation('Attempt to comment not published publication.')
	if not publication.body.title:
		raise SuspiciousOperation('Attempt to comment publication without title.')


	preferences = publication.owner.preferences()
	if not preferences.allow_messaging:
		raise SuspiciousOperation('Attempt to send call request to the realtor that was disabled this future.')


	# choosing delivery method for the notification
	method = preferences.send_message_notifications_to_sid
	if method == Preferences.MESSAGE_NOTIFICATIONS.email():
		send_email_notification()

	elif method == Preferences.MESSAGE_NOTIFICATIONS.sms_and_email():
		send_sms_notification()
		send_email_notification()

	else:
		raise RuntimeException('Invalid send method sid.')




def send_new_call_request_notification(request, tid, hash_hid, client_number, client_name=None):
	# todo: додати перевірку, чи недсилався недавно рієлтору запит на дзвінок на цей номер
	# можна використати інтервал в 2-3 години перед наступним повідомленням.


	def send_email_notification():
		template = templates.get_template('email/notifications/incoming_call_request.html')
		html = template.render({
			'client_name': client_name,
		    'phone_number': client_number,
		    'publication': {
			    'title': publication.body.title,
		        'url': settings.REDIRECT_DOMAIN + '/cabinet/#!/publications/published/{0}:{1}'.format(tid, hash_hid)
		    },
		})
		email_sender.send_html_email(
			subject = u'Запрос обратного звонка ({0})'.format(client_number), # tr
		    html = html,
		    addresses_list = [publication.owner.contact_email()],
		)


	def send_sms_notification():
		notifications_sms_sender.incoming_call_request(publication.owner.mobile_phone, client_number, request)



	# check client number
	if not client_number:
		raise InvalidArgument('Phone number can not be empty.')

	for symbol in client_number:
		if symbol not in string.digits + '+':
			raise InvalidArgument('Invalid phone number.')


	model = HEAD_MODELS.get(tid)
	if model is None:
		raise InvalidArgument('Invalid publication tid.')

	publications = model.objects.filter(hash_id = hash_hid).only('owner', 'state_sid', 'body__title')[:1]
	if not publications:
		raise InvalidArgument('Invalid publication hid.')
	publication = publications[0]


	# security checks
	if not publication.is_published():
		raise SuspiciousOperation('Attempt to comment not published publication.')
	if not publication.body.title:
		raise SuspiciousOperation('Attempt to comment publication without title.')


	preferences = publication.owner.preferences()
	if not preferences.allow_call_requests:
		raise SuspiciousOperation('Attempt to send call request to the realtor that was disabled this future.')


	# choosing delivery method for the notification
	method = preferences.send_call_request_notifications_to_sid
	if method == Preferences.CALL_REQUEST_NOTIFICATIONS.sms():
		send_sms_notification()

	elif method == Preferences.CALL_REQUEST_NOTIFICATIONS.email():
		send_email_notification()

	elif method == Preferences.CALL_REQUEST_NOTIFICATIONS.sms_and_email():
		send_sms_notification()
		send_email_notification()

	else:
		raise RuntimeException('Invalid send method sid.')
