#coding=utf-8
import json

from django.http.response import HttpResponse
from django.views.generic import View

from core.support import support_agents_notifier
from core.support.models import Tickets


class IncomingAnswerWebHook(View):
	@staticmethod
	def post(request, *args):
		"""
		Обробляє вхідні запити від Mandrill з відповідями служби підтримки.
		Формат повідомлення:
		http://help.mandrill.com/entries/22092308-What-is-the-format-of-inbound-email-webhooks-
		"""
		# todo: check me after deploy
		events = json.loads(request.POST['mandrill_events'])
		for event in events:
			message = event['msg']
			ticket_id = int(message['headers']['X-Ticket-Id'])

			ticket = Tickets.objects.filter(id=ticket_id).only('id')[:1]
			if not ticket:
				support_agents_notifier.send_nonexistent_ticket_notification(ticket)
				continue
			ticket = ticket[0]

			text = message['text']
			if not text:
				support_agents_notifier.send_empty_answer_notification(ticket, message['html'])
				continue

			try:
				ticket.add_support_answer(text)
			except Tickets.ClosedTicket:
				support_agents_notifier.send_closed_ticket_notification(ticket)
				continue

		return HttpResponse()