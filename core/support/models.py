#coding=utf-8
from django.core.exceptions import SuspiciousOperation

from django.db import models, transaction

from core.support.constants import TICKETS_STATES, TICKETS_MESSAGES_TYPES
from core.users.models import Users


class Tickets(models.Model):
	class ClosedTicket(Exception): pass
	class Meta:
		db_table = "support_tickets"

	owner = models.ForeignKey(Users)
	state_sid = models.SmallIntegerField(default=TICKETS_STATES.open())
	created = models.DateTimeField(auto_now_add=True)
	subject = models.TextField()


	@classmethod
	def by_owner(cls, user_id):
		return cls.objects.filter(owner_id=user_id).defer('owner')


	@classmethod
	def open(cls, owner, subject, message):
		with transaction.atomic():
			new_ticket = cls.objects.create(owner=owner, subject=subject)
			new_ticket.add_message(message)
		return new_ticket


	def close(self):
		self.state_sid = TICKETS_STATES.closed()
		self.save()


	def add_message(self, text):
		if self.state_sid != TICKETS_STATES.open():
			raise SuspiciousOperation('Attempt to add message into closed ticket.')

		Messages.objects.create(
			ticket = self,
			type = TICKETS_MESSAGES_TYPES.clients_message(),
			text = text
		)


	def add_support_answer(self, text):
		if self.state_sid != TICKETS_STATES.open():
			raise self.ClosedTicket()

		Messages.objects.create(
			ticket = self,
			type = TICKETS_MESSAGES_TYPES.supports_message(),
			text = text
		)


	def messages(self):
		return Messages.objects.filter(ticket=self).defer('ticket')


class Messages(models.Model):
	class Meta:
		db_table = "support_messages"

	ticket = models.ForeignKey(Tickets)
	type = models.SmallIntegerField()
	created = models.DateTimeField(auto_now_add=True)
	text = models.TextField()

