#coding=utf-8
from django.db import transaction
import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest
from django.http.response import HttpResponse
from django.views.generic import View
from collective.exceptions import RuntimeException

from collective.methods.request_data_getters import POST_parameter
from core.support.models import Tickets


class IncomingAgentResponseHook(View):
	def get(self, request, *args):
		"""
		Mandrill check's the the web hook before applying it,
		so we need to return code 200 to it.
		"""
		return HttpResponse()


	def post(self, request, *args):
		try:
			events = POST_parameter(request, 'mandrill_events')
		except ValueError:
			return HttpResponseBadRequest('No parameter @mandrill_events in request.')

		events = json.loads(events)
		if not events:
			return HttpResponseBadRequest('Empty @mandrill_events is not allowed.')


		with transaction.atomic():
			for event in events:
				# subject
				subject = event['msg'].get('subject', '')
				if not subject:
					raise ValueError('Empty subject.')

				if 'Re: ' in subject:
					subject = subject[4:]


				# message = event['msg'].get('text', '')
				message = event['msg'].get('html', '')
				if not message:
					raise ValueError('Empty message.')


				# removing the extra text
				message = message[:message.index('<div class="gmail_quote">')]

				extra = message[message.index('<div class="gmail_extra">'):]
				extra = extra.replace('<br>','')
				extra = extra.replace('\r','')
				extra = extra.replace('\n','')
				extra = extra.replace('<br clear="all">','<br/>')
				message = message[:message.index('<div class="gmail_extra">')] + extra


				# Searching the ticket and adding the agent's response.
				try:
					ticket_id = (subject[7:]).split(':')[0]
					ticket_id = int(ticket_id)
				except ValueError:
					raise RuntimeException('Invalid subject: {0}'.format(subject))

				try:
					ticket = Tickets.objects.get(id=ticket_id)
				except ObjectDoesNotExist:
					raise RuntimeException('Invalid ticket')

				ticket.add_support_answer(message)
		return HttpResponse()