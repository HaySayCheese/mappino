#coding=utf-8
from copy import deepcopy
import json

from apps.cabinet.api.classes import CabinetView
from django.http import HttpResponse, HttpResponseBadRequest
from collective.exceptions import RuntimeException, EmptyArgument
from collective.methods.request_data_getters import angular_parameters
from core.support import support_agents_notifier
from core.support.models import Tickets


class Support(object):
	class Tickets(CabinetView):
		post_codes = {
			'ok': {
				'code': 0
			},
		}


		@staticmethod
		def get(request, *args):
			"""
			Returns JSON-response with all tickets of the user. For the format of response see code.
			"""

			tickets = Tickets.by_owner(request.user.id)
			result = [{
				'id': t.id,
			    'state_sid': t.state_sid,
			    'created': t.created.strftime('%Y-%m-%dT%H:%M:00Z'),
			    'last_message': t.last_message_datetime().strftime('%Y-%m-%dT%H:%M:00Z')
			                        if t.last_message_datetime() else '-',
			    'subject': t.subject
			} for t in tickets]
			return HttpResponse(json.dumps(result), content_type="application/json")


		def post(self, request, *args):
			"""
			Creates new ticket and returns JSON-response with it's id.
			"""
			ticket = Tickets.open(request.user)
			response = deepcopy(self.post_codes['ok'])
			response['id'] = ticket.id
			return HttpResponse(json.dumps(response), content_type='application/json')


	class CloseTicket(CabinetView):
		post_codes = {
			'ok': {
				'code': 0
			},
		}

		def post(self, request, *args):
			"""
			Closes the ticket with id from the url-params.

			Params:
				ticket_id: (url, pos=0) - id of the ticket.
			"""
			try:
				ticket_id = int(args[0])
			except IndexError:
				return HttpResponseBadRequest()


			ticket = Tickets.objects.filter(id=ticket_id, owner=request.user).only('id')[:1]
			if not ticket:
				return HttpResponseBadRequest('No ticket with such id.')

			ticket = ticket[0]
			ticket.close()
			return HttpResponse(json.dumps(
				self.post_codes['ok']), content_type="application/json")


	class Messages(CabinetView):
		post_codes = {
		    'invalid_parameters': {
			    'code': 1
		    },
		    'invalid_ticket_id': {
			    'code': 2
		    },
		}


		def get(self, request, *args):
			"""
			Returns JSON-response with all messages of ticket ith id from url.
			For the response format see the code.

			Params:
				ticket_id (url, pos=0)
			"""
			try:
				ticket_id = args[0]
			except IndexError:
				return HttpResponseBadRequest(json.dumps(
					self.post_codes['invalid_parameters']), content_type='application/json')

			ticket = Tickets.objects.filter(id=ticket_id, owner=request.user).only('id')[:1]
			if not ticket:
				return HttpResponseBadRequest(json.dumps(
					self.post_codes['invalid_ticket_id']), content_type='application/json')
			ticket = ticket[0]

			result = [{
				'id': m.id,
			    'type_sid': m.type_sid,
			    'created': m.created.strftime('%Y-%m-%dT%H:%M:%S'),
			    'text': m.text,
			} for m in ticket.messages()]
			return HttpResponse(json.dumps(result), content_type="application/json")


		def post(self, request, *args):
			"""
			Params:
				ticket_id - (url, pos=0)
				message - message in plaintext that will be added to the ticket.
				subject - (optional) - subject that will be set tot the ticket.

			Updates ticket with @message and @subject (if present).
			If @subject is present and ticket does not have subject already -
			the subject will be set to the ticket, else the response with error code will be returned.
			"""
			try:
				ticket_id = int(args[0])
			except IndexError:
				return HttpResponseBadRequest()

			ticket = Tickets.objects.filter(id=ticket_id, owner=request.user).only('id')[:1]
			if not ticket:
				return HttpResponseBadRequest('No ticket with such id.')
			ticket = ticket[0]

			try:
				params = angular_parameters(request)
			except ValueError:
				return HttpResponseBadRequest(json.dumps(
					self.post_codes['invalid_parameters']), content_type='application/json')


			subject = params.get('subject')
			if subject:
				try:
					ticket.set_subject(subject)
				except EmptyArgument:
					return HttpResponse(json.dumps(
						self.post_codes['invalid_parameters']), content_type='application/json')


			message = params.get('message')
			if not message:
				return HttpResponseBadRequest('@message can\'t be empty, it is required.')

			try:
				ticket.add_message(message)
			except EmptyArgument:
				return HttpResponseBadRequest(json.dumps(
					self.post_codes['invalid_parameters']), content_type='application/json')


			support_agents_notifier.send_notification(ticket, message)
			return HttpResponse(json.dumps(self.post_codes['ok']), content_type="application/json")