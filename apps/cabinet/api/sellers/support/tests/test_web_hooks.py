# import json
# from apps.cabinet.api.support.ajax import Tickets
# from core.support import constants
# from core.support.models import Messages
# from core.users.models import Users
# from django.test import Client
# from django.utils.unittest.case import TestCase
#
#
# class IncomingAgentAnswerTest(TestCase):
# 	@classmethod
# 	def setUpClass(cls):
# 		cls.client = Client()
# 		cls.user = Users.objects.create_user('mail@mail.com', '+380954699151', 'password')
# 		cls.user.is_active = True # by default accounts are disabled
# 		cls.user.save()
# 		cls.client.login(username='+380954699151', password='password')
#
#
# 	@classmethod
# 	def tearDownClass(cls):
# 		Users.objects.all().delete()
#
#
# 	def tearDown(self):
# 		Messages.objects.all().delete()
# 		Tickets.objects.all().delete()
#
#
# 	def test_empty_request(self):
# 		r = self.client.post('/web-hooks/support/agents-answers/')
# 		self.assertEqual(r.status_code, 400)
#
# 		r = self.client.post('/web-hooks/support/agents-answers/', {'mandrill_events': {}})
# 		self.assertEqual(r.status_code, 400)
#
# 		r = self.client.post('/web-hooks/support/agents-answers/', {'mandrill_events': []})
# 		self.assertEqual(r.status_code, 400)
#
#
# 	def test_empty_subject(self):
# 		r = self.client.post('/web-hooks/support/agents-answers/', {
# 			'mandrill_events': json.dumps([
# 				{
# 					'msg': {
# 						'subject': ''
# 					}
# 				},
# 			])
# 		})
#
# 		# Since one request from Mandrill may contains several messages
# 		# it is terrible idea to return response with 500 to it,
# 		# because Mandrill will retry the request with the exact messages
# 		# and it potentially can produce duplicates in users dialog.
# 		self.assertEqual(r.status_code, 200)
#
# 		self.assertEqual(Tickets.objects.all().count(), 0)
#
#
# 	def test_normal(self):
# 		ticket = Tickets.open(self.user)
#
# 		r = self.client.post('/web-hooks/support/agents-answers/', {
# 			'mandrill_events': json.dumps([
# 				{'msg': {
# 					'subject': 'Ticket {0}: test subject'.format(ticket.id),
# 				    'text': 'test message'
# 				}},
# 			])
# 		})
#
#
# 		self.assertEqual(r.status_code, 200)
# 		self.assertEqual(ticket.messages().count(), 1)
# 		self.assertEqual(Tickets.objects.all().count(), 1)
#
# 		message = ticket.messages()[0]
# 		self.assertEqual(message.type_sid, constants.TICKETS_MESSAGES_TYPES.supports_message())