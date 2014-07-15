#coding=utf-8
from django.conf import settings
from django.core.exceptions import SuspiciousOperation

from collective.exceptions import InvalidArgument, RuntimeException
from core.email_backend import email_sender
from core.sms_dispatcher import notifications_sms_sender
from core.users.constants import Preferences
from core.utils.jinja2_integration import templates



class NewClients(object):
	@staticmethod
	def send_sms_notification(request, publication):
		return notifications_sms_sender.incoming_message(request, publication.owner.mobile_phone)


	@staticmethod
	def send_email_notification(tid, publication, email, name, message):
		template = templates.get_template('email/notifications/incoming_message.html')
		html = template.render({
			'client_name': name,
		    'publication': {
			    'title': publication.body.title,
		        'url': settings.REDIRECT_DOMAIN + '/cabinet/#!/publications/published/{0}:{1}'.format(
			        tid, publication.hash_id)
		    },
		    'message': message
		})

		return email_sender.send_html_email(
			subject = u'Сообщение от заинтересованного клиента ({0})'.format(name), # tr
		    html = html,
		    addresses_list = [publication.owner.contact_email()],
		    reply_to = email
		)



class CallRequests(object):
	@staticmethod
	def send_sms_notification(request, publication):
		return notifications_sms_sender.incoming_message(request, publication.owner.mobile_phone)


	@staticmethod
	def send_email_notification(tid, publication, number, name):
		template = templates.get_template('email/notifications/incoming_call_request.html')
		html = template.render({
			'client_name': name,
		    'phone_number': number,
		    'publication': {
			    'title': publication.body.title,
		        'url': settings.REDIRECT_DOMAIN + '/cabinet/#!/publications/published/{0}:{1}'.format(
			        tid, publication.hash_id)
		    },
		})
		return email_sender.send_html_email(
			subject = u'Запрос обратного звонка ({0})'.format(number), # tr
		    html = html,
		    addresses_list = [publication.owner.contact_email()],
		)


	@staticmethod
	def send_sms_notification(request, publication):
		return notifications_sms_sender.incoming_call_request(
			request, publication.owner.mobile_phone, publication.owner.mobile_phone)



def send_notification_about_new_message(request, tid, publication, message, client_email, client_name=None):
	"""
	Аналізує налаштування ріелтора, що є власником оголошення publication,
	та обирає спосіб доставки повідомлення, після чого надсилає повідомлення.

	:param request:
		<передаєтьсья в нижчу логіку>

	:param tid: id типу оголошення.
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
		raise InvalidArgument('Invalid message: {0}'.format(message))
	if not client_email:
		raise InvalidArgument('Invalid email: {0}'.format(client_email))
	if not client_name:
		raise InvalidArgument('Invalid client name: {0}'.format(client_name))


	preferences = publication.owner.preferences()
	if not preferences.allow_messaging:
		raise SuspiciousOperation('Attempt to send message to the realtor that was disabled this future.')


	# choosing delivery method for the notification
	# and sending the notification
	method = preferences.send_message_notifications_to_sid
	if method == Preferences.messaging.email():
		NewClients.send_email_notification(tid, publication, client_email, client_name, message)

	elif method == Preferences.messaging.sms_and_email():
		# if delivering by one of the methods wasn't successful —
		# delivering by other methods should not break,
		# but on the end of the method the error should be raised.

		error = None
		try:
			if not NewClients.send_sms_notification(request, publication):
				raise RuntimeException('Message can\'t be delivered.')

		except Exception as e:
			# catch all errors here
			error = e


		try:
			if not NewClients.send_email_notification(tid, publication, client_email, client_name, message):
				raise RuntimeException('Message can\'t be delivered.')

		except Exception as e:
			# catch all errors here
			error = e


		if error is not None:
			raise error

	else:
		# method is unknown
		raise RuntimeException('Invalid send method sid.')




def send_notification_about_new_call_request(request, tid, publication, client_number, client_name=None):
	"""
	Аналізує налаштування ріелтора, що є власником оголошення publication,
	та обирає спосіб доставки повідомлення, після чого надсилає повідомлення.

	:param request:
		<передаєтьсья в нижчу логіку>

	:param tid: id типу оголошення.
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


	preferences = publication.owner.preferences()
	if not preferences.allow_call_requests:
		raise SuspiciousOperation('Attempt to send call request to the realtor that was disabled this future.')


	# choosing delivery method for the notification
	# and sending the message
	method = preferences.send_call_request_notifications_to_sid
	if method == Preferences.call_requests.sms():
		CallRequests.send_sms_notification(request, publication)

	elif method == Preferences.call_requests.email():
		CallRequests.send_email_notification(tid, publication, client_number, client_name)

	elif method == Preferences.call_requests.sms_and_email():
		# if delivering through one of the methods wasn't successful —
		# delivering by other methods should not break,
		# but on the end of the method the error should be raised.

		error = None
		try:
			if not CallRequests.send_sms_notification(request, publication):
				raise RuntimeException('Message can\'t be delivered.')

		except Exception as e:
			# catch all errors here
			error = e


		try:
			if not CallRequests.send_email_notification(tid, publication, client_number, client_name):
				raise RuntimeException('Message can\'t be delivered.')

		except Exception as e:
			# catch all errors here
			error = e


		if error is not None:
			raise error

	else:
		raise RuntimeException('Invalid send method sid.')
