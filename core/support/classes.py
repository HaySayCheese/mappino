#coding=utf-8
from django.conf import settings
import mandrill
from collective.exceptions import InvalidArgument, RuntimeException
from mappino.wsgi import templates


class SupportAgentsNotifier(object):
	def __init__(self):
		self.__connect_to_mandrill()


	def send_notification(self, ticket, message, user_name):
		"""
		Надішле повідомлення, що надійшло від рієлтора на ящик підтримки.
		"""
		if not message:
			raise InvalidArgument('Message can not be empty.')

		html = templates.get_template('email/support/new_ticket.html').render({
			'client': {
				'id': ticket.owner.id,
			    'name': ticket.owner.full_name(),
			},
		    'message': message,
		})
		if not self.__send_email(ticket, html, user_name):
			raise RuntimeException('Emails was not sent.')


	def send_empty_answer_notification(self, ticket, html):
		"""
		Надішле повідомлення агенту підтримки про те,
		що його попереднє повідомлення було відхилено системою обробки через відсутність тексту,
		або неможливість його розпізнання.
		"""
		html = templates.get_template('email/support/auto_responses/empty_answer.html').render({
		    'html': html
		})
		if not self.__send_email(ticket, html):
			raise RuntimeException('Emails was not sent.')


	def send_closed_ticket_notification(self, ticket):
		"""
		Надішле повідомлення агенту підтримки про те,
		що його попереднє повідомлення було відхилено системою обробки через те,
		що клієнт закрив тікет.
		"""
		html = templates.get_template('email/support/auto_responses/closed_ticket.html').render()
		if not self.__send_email(ticket, html):
			raise RuntimeException('Emails was not sent.')


	def send_nonexistent_ticket_notification(self, ticket):
		"""
		Надішле повідомлення агенту підтримки про те,
		що його попереднє повідомлення було відхилено системою обробки через відсутність тікета.
		(наприклад, якшо тікет був фізично видалений)
		"""
		html = templates.get_template('email/support/auto_responses/nonexistent_ticket.html').render()
		if not self.__send_email(ticket, html):
			raise RuntimeException('Emails was not sent.')



	def __send_email(self, ticket, html, user_name=None):
		def send():
			result = self.mandrill_client.messages.send(message=message, async=False)
			return result[0]['status'] == 'sent'

		if user_name is None:
			user_name = ''

		message = {
			'from_email': u'support@mandrill-3702849048.mappino.com',
			'from_name': u'{user_name}'.format(user_name = user_name),
			'to': [{
				'type': u'to',
				'email': settings.SUPPORT_EMAIL,
			}],
		    'subject': u'Ticket {0}: {1}'.format(ticket.id, ticket.subject),
			'html': html,
			'headers': {
				'Reply-To': u'support@mandrill-3702849048.mappino.com', # todo: add web hook here
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