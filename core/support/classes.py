#coding=utf-8
from django.conf import settings
import mandrill
from collective.exceptions import InvalidArgument
from mappino.wsgi import templates


class SupportAgentsNotifier(object):
	def __init__(self):
		self.__connect_to_mandrill()


	def send_notification(self, ticket, message):
		if not message:
			raise InvalidArgument('Message can not be empty.')

		html = templates.get_template('email/support/new_ticket.html').render({
			'client': {
				'id': ticket.owner.id,
			    'name': ticket.owner.full_name(),
			},
		    'message': message
		})
		self.__send_email(ticket, html)


	def send_empty_answer_notification(self, ticket, html):
		html = templates.get_template('email/support/auto_responses/empty_answer.html').render({
		    'html': html
		})
		self.__send_email(ticket, html)


	def send_closed_ticket_notification(self, ticket):
		html = templates.get_template('email/support/auto_responses/closed_ticket.html').render()
		self.__send_email(ticket, html)


	def send_nonexistent_ticket_notification(self, ticket):
		html = templates.get_template('email/support/auto_responses/nonexistent_ticket.html').render()
		self.__send_email(ticket, html)


	def __send_email(self, ticket, html):
		def send():
			result = self.mandrill_client.messages.send(message=message, async=True)
			return result[0]['status'] == 'sent'

		message = {
			'from_email': 'support-dispatcher@mappino.com',
			'from_name': 'support-request',
			'to': [{
				'type': 'to',
				'email': settings.SUPPORT_EMAIL,
			}],
		    'subject': u'Ticket {0}: {1}'.format(ticket.id, ticket.subject),
			'html': html,
			'headers': {
				'Reply-To': settings.SUPPORT_EMAIL, # todo: add web hook here
			    'X-Ticket-Id': unicode(ticket.id),
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