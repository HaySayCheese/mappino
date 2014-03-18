#coding=utf-8
import mandrill

from django.core.exceptions import SuspiciousOperation
from django.conf import settings

from collective.exceptions import InvalidArgument
from core.publications.constants import HEAD_MODELS, OBJECT_STATES
from core.sms_dispatcher import notifications_sms_sender
from mappino.wsgi import templates


class NotificationsDispatcher(object):
	def __init__(self):
		self.__connect_to_mandrill()


	def send_new_message_notification(self, request, pub_tid, pub_hid, message, client_email, client_name=None):
		if not message:
			raise InvalidArgument('Message can not be empty.')

		model = HEAD_MODELS.get(pub_tid)
		if model is None:
			raise InvalidArgument('Invalid publication tid.')

		publication = model.objects.filter(id = pub_hid).only('id', 'owner', 'state_sid', 'body__title')[:1]
		if not publication:
			raise InvalidArgument('Invalid publication hid.')
		publication = publication[0]

		# security checks
		if not publication.state_sid == OBJECT_STATES.published():
			raise SuspiciousOperation('Attempt to comment not published publication.')
		if not publication.body.title:
			raise SuspiciousOperation('Attempt to comment publication without title.')

		html = templates.get_template('email/notifications/incoming_message.html').render({
			'domain': settings.REDIRECT_DOMAIN,
			'client_name': client_name,
		    'publication': {
			    'tid': pub_tid,
			    'hid': pub_hid,
			    'title': publication.body.title,
		    },
		    'message': message
		})
		message = {
			'from_email': 'mail-dispatcher@mappino.com',
			'from_name': 'mappino',
			'to': [{
				'type': 'to',
				'email': publication.owner.email,
			}],
		    'subject': u'Сообщение от заинтересованного клиента (' + client_email + ')', # tr
			'html': html,
			'headers': {
				'Reply-To': client_email,
			},
		}
		self.__send_email(message)

		# Надішлем рієлтору щасливу sms
		notifications_sms_sender.incoming_message(publication.owner.mobile_phone(), request)


	def send_new_call_request_notification(self, request, pub_tid, pub_hid, client_number, client_name=None):
		if not client_number:
			raise InvalidArgument('Phone number can not be empty.')

		model = HEAD_MODELS.get(pub_tid)
		if model is None:
			raise InvalidArgument('Invalid publication tid.')

		publication = model.objects.filter(id = pub_hid).only('id', 'owner', 'state_sid', 'body__title')[:1]
		if not publication:
			raise InvalidArgument('Invalid publication hid.')
		publication = publication[0]

		# security checks
		if not publication.state_sid == OBJECT_STATES.published():
			raise SuspiciousOperation('Attempt to comment not published publication.')
		if not publication.body.title:
			raise SuspiciousOperation('Attempt to comment publication without title.')

		html = templates.get_template('email/notifications/incoming_call_request.html').render({
			'domain': settings.REDIRECT_DOMAIN,
			'client_name': client_name,
		    'phone_number': client_number,
		    'publication': {
			    'tid': pub_tid,
			    'hid': pub_hid,
			    'title': publication.body.title,
		    },
		})
		message = {
			'from_email': 'mail-dispatcher@mappino.com',
			'from_name': 'mappino',
			'to': [{
				'type': 'to',
				'email': publication.owner.email,
			}],
		    'subject': u'Запрос обратного звонка ('+ unicode(client_number) + ')', # tr
			'html': html,
		}
		self.__send_email(message)

		# Надішлем рієлтору щасливу sms
		notifications_sms_sender.incoming_call_request(publication.owner.mobile_phone(), client_number, request)


	def __send_email(self, message):
		def send():
			result = self.mandrill_client.messages.send(message=message, async=True)
			return result[0]['status'] == 'sent'

		try:
			return send()
		except (mandrill.Error, IndexError):
			# При виникненні помилки - спробувати повторно з’єднатись з mandrill і надіслати заново.
			self.__connect_to_mandrill()
			return send()


	def __connect_to_mandrill(self):
		self.mandrill_client = mandrill.Mandrill(settings.MANDRILL_API_KEY)