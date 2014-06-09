#coding=utf-8
import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest
from django.http.response import HttpResponse
from django.views.generic import View

from collective.methods.request_data_getters import POST_parameter
from core.support.models import Tickets


class IncomingAgentResponseHook(View):
	def get(self, request, *args):
		return HttpResponse()


	def post(self, request, *args):
		try:
			events = POST_parameter(request, 'mandrill_events')
		except ValueError:
			return HttpResponseBadRequest('No parameter @mandrill_events in request.')

		events = json.loads(events)
		if not events:
			return HttpResponseBadRequest('Empty @mandrill_events is not allowed.')

		for event in events:
			# Validation of Mandrill's event.
			#
			# At this point we can't return BadRequest response, because @events can contains several messages.
			# In this loop we don't know what iteration is it and what message does not pass validation.
			# If we will return BadRequest to the mandrill it will try to reproduce the request with exact messages,
			# and it can produce duplicates of responses in the user's dialog.
			if not 'msg' in event:
				# Ignore invalid message.
				continue

			subject = event['msg'].get('subject', '')
			if not subject:
				# ignore invalid message
				continue

			message = event['msg'].get('text', '')
			if not message:
				# ignore invalid message
				continue


			# Searching the ticket and adding the agent's response.
			try:
				ticket_id = (subject[7:]).split(':')[0]
				ticket_id = int(ticket_id)
			except ValueError:
				# we can not return 500 to the Mandrill, because it will retry this request again,
				# but we should notify the developers about nonexistence ticket.
				# todo: add developers notify
				continue

			try:
				ticket = Tickets.objects.get(id=ticket_id)
			except ObjectDoesNotExist:
				# we can not return 500 to the Mandrill, because it will retry this request again,
				# but we should notify the developers about nonexistence ticket.
				# todo: add developers notify
				continue

			ticket.add_support_answer(message)
		return HttpResponse()