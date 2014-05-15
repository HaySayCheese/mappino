#coding=utf-8
import json

from apps.cabinet.api.classes import CabinetView
from django.http import HttpResponse, HttpResponseBadRequest
from collective.exceptions import InvalidArgument
from collective.methods.request_data_getters import angular_parameters
from core.support import support_agents_notifier
from core.support.models import Tickets



class Support(object):
	class Tickets(CabinetView):
		post_codes = {
			'ok': {
				'code': 0
			},
		    'invalid_parameters': {
			    'code': 1
		    },
		}


		@staticmethod
		def get(request, *args):
			"""
			Returns JSON-response with all tickets of the user.
			For the format of response see code.
			"""
			tickets = Tickets.by_owner(request.user.id)
			result = [{
				'id': t.id,
			    'state_sid': t.state_sid,
			    'created': t.created.strftime('%d.%m.%Y - %H:%M'), # todo: форматування часу
			    'last_message': t.last_message_datetime().strftime('%d.%m.%Y - %H:%M') if t.last_message_datetime() else '-', # todo: форматування часу
			    'subject': t.subject
			} for t in tickets]
			return HttpResponse(json.dumps(result), content_type="application/json")


		def post(self, request, *args):
			"""
			Creates new ticket and returns JSON-response with it's id.
			"""
			try:
				params = angular_parameters(request, ['subject', 'message'])
			except ValueError:
				return HttpResponseBadRequest(json.dumps(
					self.post_codes['invalid_parameters']), content_type='application/json')

			user = request.user
			subject = params['subject']
			message = params['message']

			try:
				ticket = Tickets.open(user)
				support_agents_notifier.send_notification(ticket, message)
			except InvalidArgument:
				return HttpResponseBadRequest(json.dumps(
					self.post_codes['invalid_parameters']), content_type='application/json')
			return HttpResponse(json.dumps(self.post_codes['ok']), content_type="application/json")


	class CloseTicket(CabinetView):
		post_codes = {
			'ok': {
				'code': 0
			},
		}

		def post(self, request, *args):
			"""
			Обробляє запит на закриття тікета
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
			ticket.close()
			return HttpResponse(json.dumps(self.post_codes['ok']), content_type="application/json")


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
			Віддає всі повідомлення одного тікета в json
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
			Обробляє запит на створення нового повідомлення в запиті до служби підтримки
			(нове повідомлення)
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

			try:
				params = angular_parameters(request, ['message'])
			except ValueError:
				return HttpResponseBadRequest(json.dumps(
					self.post_codes['invalid_parameters']), content_type='application/json')
			message = params['message']

			try:
				ticket.add_message(message)
				support_agents_notifier.send_notification(ticket, message)
			except InvalidArgument:
				return HttpResponseBadRequest(json.dumps(
					self.post_codes['invalid_parameters']), content_type='application/json')
			return HttpResponse(json.dumps(self.post_codes['ok']), content_type="application/json")