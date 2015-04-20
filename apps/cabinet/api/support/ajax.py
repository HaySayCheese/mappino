#coding=utf-8
from django.db.models import Q

from apps.classes import CabinetView
from collective.http.responses import *
from collective.exceptions import EmptyArgument
from collective.methods.request_data_getters import angular_parameters
from core.support import support_agents_notifier
from core.support.models import Tickets, Messages


class Support(object):
    class Tickets(CabinetView):
        class Get(object):
            @staticmethod
            def ok(tickets):
                # warn: response code is omitted here and can't be added, because of list format!
                # todo: add response code and message here

                return HttpJsonResponse([
                    {
                        'id': ticket.id,
                        'state_sid': ticket.state_sid,
                        'created': ticket.created.strftime('%Y-%m-%dT%H:%M:00Z'),
                        'last_message': ticket.last_message_datetime().strftime('%Y-%m-%dT%H:%M:00Z')
                                            if ticket.last_message_datetime() else '-',
                        'subject': ticket.subject

                    } for ticket in tickets
                ])


        class Post(object):
            @staticmethod
            def ok(ticket_id):
                return HttpJsonResponse({
                    'code': 0,
                    'id': ticket_id,
                })


        #
        # view methods
        #
        def get(self, request, *args):
            """
            Returns JSON-response with all the tickets of the user.
            For the response format see code.
            """

            # note: owner check is made
            tickets = Tickets.by_owner(request.user.id)
            return self.Get.ok(tickets)


        def post(self, request, *args):
            """
            Creates new ticket and returns JSON-response with it's id.
            If user has one empty ticket (without subject and without messages) - returns it as new ticket.
            """

            # If user already has one empty ticket -
            # lets force him to use it, instead of creating new one.
            empty_tickets = Tickets.objects.filter(
                 Q(
                     # owner check
                     owner=request.user.id
                 ),
                 Q(
                     # contains no subject
                     Q(subject__isnull=True) or Q(subject='')
                 ),
                ~Q(
                    # contains no one message
                    id__in=Messages.objects.values_list('ticket_id')
                 )
            ).only('id')[:1]

            if empty_tickets:
                ticket = empty_tickets[0]
                return self.Post.ok(ticket.id)

            else:
                ticket = Tickets.open(request.user)
                return self.Post.ok(ticket.id)


    class CloseTicket(CabinetView):
        class Post(object):
            @staticmethod
            def ok():
                return HttpJsonResponse({
                    'code': 0,
                })

            @staticmethod
            def invalid_ticket_id():
                return HttpJsonResponseBadRequest({
                    'code': 1,
                    'message': 'Request does not contains required param "ticket_id", or it is invalid.',
                })

            @staticmethod
            def no_such_ticket():
                return HttpJsonResponseNotFound({
                    'code': 2,
                    'message': 'There is no such ticket with exact id.',
                })



        def post(self, request, *args):
            """
            Closes the ticket with id from the url-params.
            Params:
                ticket_id (url, pos=0): id of the ticket.
            """
            try:
                ticket_id = int(args[0])
            except IndexError:
                return self.Post.invalid_ticket_id()


            # note: owner check is done
            ticket = Tickets.objects.filter(id=ticket_id, owner=request.user).only('id')[:1]
            if not ticket:
                return self.Post.no_such_ticket()


            ticket = ticket[0]
            ticket.close()
            return self.Post.ok()


    class Messages(CabinetView):
        class Get(object):
            @staticmethod
            def ok(ticket, user):
                return HttpJsonResponse({
                    'code': 0,
                    'message': 'OK',

                    # todo: move this data into subobjact
                    'subject': ticket.subject,
                    'user_avatar': user.avatar().url(),
#                   'admin_avatar': '', # todo: add admin avatar url here.
                    'messages': [{
                        'type_sid': m.type_sid,
                        'created': m.created.strftime('%Y-%m-%dT%H:%M:00Z'),
                        'text': m.text,
                    } for m in ticket.messages()]
                })


            @staticmethod
            def no_param_ticket_id():
                return HttpJsonResponseBadRequest({
                    'code': 1,
                    'message': 'Request does not contains required positional parameter "ticket_id".'
                })


            @staticmethod
            def no_such_ticket():
                return HttpJsonResponseNotFound({
                    'code': 2,
                    'message': 'There is not such ticket wth exact id.'
                })


        class Post(object):
            @staticmethod
            def ok():
                return HttpJsonResponse({
                    'code': 0,
                    'message': 'OK',
                })


            @staticmethod
            def no_param_ticket_id():
                return HttpJsonResponseBadRequest({
                    'code': 1,
                    'message': 'Request does not contains required positional parameter "ticket_id".'
                })


            @staticmethod
            def no_such_ticket():
                return HttpJsonResponseNotFound({
                    'code': 2,
                    'message': 'There is not such ticket wth exact id.'
                })


            @staticmethod
            def invalid_request(): # it's to lazy now to implement error per method
                return HttpJsonResponseBadRequest({
                    'code': 3,
                    'message': 'Request does not contains required parameter, or contains invalid data.'
                })


        def get(self, request, *args):
            """
            Returns JSON-response with all messages of ticket ith id from url.
            For the response format see the code.

            Params:
                ticket_id (url, pos=0): id of the ticket.
            """
            try:
                ticket_id = args[0]
            except IndexError:
                return self.Get.no_param_ticket_id()


            # note: owner check is done
            tickets = Tickets.objects.filter(id=ticket_id, owner=request.user).only('id')[:1]
            if not tickets:
                return self.Get.no_such_ticket()


            ticket = tickets[0]
            return self.Get.ok(ticket, request.user)


        def post(self, request, *args):
            """
            Params:
                ticket_id - (url, pos=0)
                message - message in plaintext that will be added to the ticket.
                subject - (optional) - subject that will be set tot the ticket.

            Updates ticket with "message" and "subject" (if present).
            If "subject" is present and ticket does not have subject already -
            the "subject" will be set to the ticket, else the response with error code will be returned.
            """
            try:
                ticket_id = int(args[0])
            except IndexError:
                return self.Post.no_param_ticket_id()

            try:
                params = angular_parameters(request)
            except ValueError:
                return self.Post.invalid_request()


            # note: owner check is done
            tickets = Tickets.objects.filter(id=ticket_id, owner=request.user).only('id')[:1]
            if not tickets:
                return self.Post.no_such_ticket()
            else:
                ticket = tickets[0]


            subject = params.get('subject', '')
            if subject:
                try:
                    ticket.set_subject(subject)
                except EmptyArgument:
                    return self.Post.invalid_request()


            message = params.get('message')
            if not message:
                return self.Post.invalid_request()

            try:
                ticket.add_message(message)
            except EmptyArgument:
                return self.Post.invalid_request()

            # sending notification to the support about new ticket.
            # separate method is used to have possibility to implement
            # notifications balancing between support agents
            support_agents_notifier.send_notification(ticket, message, request.user.full_name())

            return self.Post.ok()

