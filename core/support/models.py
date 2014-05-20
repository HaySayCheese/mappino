#coding=utf-8
from collective.exceptions import EmptyArgument

from django.db import models

from core.support.constants import TICKETS_STATES, TICKETS_MESSAGES_TYPES
from core.users.models import Users


class Tickets(models.Model):
	# exceptions
	class ClosedTicket(Exception):
		pass

	owner = models.ForeignKey(Users)
	state_sid = models.SmallIntegerField(default=TICKETS_STATES.open())
	created = models.DateTimeField(auto_now_add=True)
	subject = models.TextField(null=True)

	class Meta:
		db_table = "support_tickets"


	@classmethod
	def by_owner(cls, user_id):
		return cls.objects.filter(owner_id=user_id).defer('owner')


	@classmethod
	def open(cls, owner):
		"""
		Opens new ticket with owner @owner.
		By default the subject of ticket is blank and no one message will be added.

		Params:
			owner - user to which the ticket will be assigned.
		"""
		return cls.objects.create(owner=owner)


	def close(self):
		self.state_sid = TICKETS_STATES.closed()
		self.save()


	def set_subject(self, subject):
		"""
		If subject if ticket is blank - it wil lbe updated with @subject,
		else RuntimeException will  be thrown.

		Params:
			subject - the new subject of a ticket.
		"""
		if not subject:
			raise EmptyArgument('@subject')

		self.subject = subject
		self.save()


	def add_message(self, message):
		"""
		Adds @message to the ticket if it is opened, else - raises an ClosedTicket exception.
		This method should be used to add message from users.

		params:
			@text (required) - message that should be added to the ticket.
		"""
		if not message:
			raise EmptyArgument('@message')

		if self.state_sid != TICKETS_STATES.open():
			raise self.ClosedTicket()


		Messages.objects.create(
			ticket = self,
			type_sid = TICKETS_MESSAGES_TYPES.clients_message(),
			text = message
		)


	def add_support_answer(self, message):
		"""
		Adds @message to the ticket if it is opened, else - raises an ClosedTicket exception.
		This method should be used to add message from support agents.

		params:
			@text: (required) - message that should be added to the ticket.
		"""
		if not message:
			raise EmptyArgument('@message')

		if self.state_sid != TICKETS_STATES.open():
			raise self.ClosedTicket()


		Messages.objects.create(
			ticket = self,
			type_sid = TICKETS_MESSAGES_TYPES.supports_message(),
			text = message
		)


	def messages(self):
		"""
		Returns QuerySet with all messages in ticket sorted by creation date in reverse order.
		If no messages in ticket - the result queryset will be empty.
		"""
		return Messages.objects.filter(ticket=self).defer('ticket').order_by('-created')


	def last_message_datetime(self):
		"""
		Returns datetime of last added message.
		If no messages in ticket - returns None.
		"""
		try:
			return self.messages().order_by('-created').only('created')[:1][0].created
		except IndexError:
			return None


class Messages(models.Model):
	ticket = models.ForeignKey(Tickets)
	type_sid = models.SmallIntegerField()
	created = models.DateTimeField(auto_now_add=True)
	text = models.TextField()

	class Meta:
		db_table = "support_messages"

