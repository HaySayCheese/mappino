#coding=utf-8
import json

from django.http import HttpResponseBadRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View

from collective.decorators.views import login_required_or_forbidden

from collective.exceptions import InvalidArgument

from collective.methods.request_data_getters import angular_parameters
from core.support import support_agents_notifier
from core.support.models import Tickets


class TicketsView(View):
	codes = {
		'ok': {
			'code': 0
		},
	    'invalid_parameters': {
		    'code': 1
	    },
	}


	@method_decorator(login_required_or_forbidden)
	def dispatch(self, *args, **kwargs):
		return super(TicketsView, self).dispatch(*args, **kwargs)


	def get(self, request, *args):
		"""
		Віддає всі звернення до служби підтримки,
		які належать користувачу, який згенерував запит.
		"""
		tickets = Tickets.by_owner(request.user.id)
		result = [{
			'id': t.id,
		    'state_sid': t.state_sid,
		    'created': t.created.strftime('%Y-%m-%dT%H:%M:%S'),
		    'subject': t.subject
		} for t in tickets]
		return HttpResponse(json.dumps(result), content_type="application/json")


	def post(self, request, *args):
		"""
		Обробляє запит на створення нового звернення в службу підтримки
		"""
		try:
			params = angular_parameters(request, ['subject', 'message'])
		except ValueError:
			return HttpResponseBadRequest(json.dumps(
				self.codes['invalid_parameters']), content_type='application/json')

		user = request.user
		subject = params['subject']
		message = params['message']

		try:
			ticket = Tickets.open(user, subject, message)
			support_agents_notifier.send_notification(ticket, message)
		except InvalidArgument:
			return HttpResponseBadRequest(json.dumps(
				self.codes['invalid_parameters']), content_type='application/json')
		return HttpResponse(json.dumps(self.codes['ok']), content_type="application/json")


class CloseTicket(View):
	codes = {
		'ok': {
			'code': 0
		},
	}

	@method_decorator(login_required_or_forbidden)
	def dispatch(self, *args, **kwargs):
		return super(CloseTicket, self).dispatch(*args, **kwargs)


	def post(self, request, *args):
		"""
		Обробляє запит на закриття тікета
		"""
		try:
			ticket_id = args[0]
		except IndexError:
			return HttpResponseBadRequest(json.dumps(
				self.codes['invalid_parameters']), content_type='application/json')

		ticket = Tickets.objects.filter(id=ticket_id, owner=request.user).only('id')[:1]
		if not ticket:
			return HttpResponseBadRequest(json.dumps(
				self.codes['invalid_ticket_id']), content_type='application/json')
		ticket = ticket[0]
		ticket.close()
		return HttpResponse(json.dumps(self.codes['ok']), content_type="application/json")


class MessagesView(View):
	codes = {
	    'invalid_parameters': {
		    'code': 1
	    },
	    'invalid_ticket_id': {
		    'code': 2
	    },
	}

	@method_decorator(login_required_or_forbidden)
	def dispatch(self, *args, **kwargs):
		return super(MessagesView, self).dispatch(*args, **kwargs)


	def get(self, request, *args):
		"""
		Віддає всі повідомлення одного тікета в json
		"""
		try:
			ticket_id = args[0]
		except IndexError:
			return HttpResponseBadRequest(json.dumps(
				self.codes['invalid_parameters']), content_type='application/json')

		ticket = Tickets.objects.filter(id=ticket_id, owner=request.user).only('id')[:1]
		if not ticket:
			return HttpResponseBadRequest(json.dumps(
				self.codes['invalid_ticket_id']), content_type='application/json')
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
				self.codes['invalid_parameters']), content_type='application/json')

		ticket = Tickets.objects.filter(id=ticket_id, owner=request.user).only('id')[:1]
		if not ticket:
			return HttpResponseBadRequest(json.dumps(
				self.codes['invalid_ticket_id']), content_type='application/json')
		ticket = ticket[0]

		try:
			params = angular_parameters(request, ['message'])
		except ValueError:
			return HttpResponseBadRequest(json.dumps(
				self.codes['invalid_parameters']), content_type='application/json')
		message = params['message']

		try:
			ticket.add_message(message)
			support_agents_notifier.send_notification(ticket, message)
		except InvalidArgument:
			return HttpResponseBadRequest(json.dumps(
				self.codes['invalid_parameters']), content_type='application/json')
		return HttpResponse(json.dumps(self.codes['ok']), content_type="application/json")