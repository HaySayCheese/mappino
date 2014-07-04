#coding=utf-8
from collective.constants import AbstractConstant


class CallRequestNotificationsTypes(AbstractConstant):
	def __init__(self):
		super(CallRequestNotificationsTypes, self).__init__()
		self.set_ids({
			'sms': 0,
		    'email': 1,
		    'sms_and_email': 2,
		})


	def sms(self):
		return self.ids['sms']


	def email(self):
		return self.ids['email']


	def sms_and_email(self):
		return self.ids['sms_and_email']



class MessageNotificationsTypes(AbstractConstant):
	def __init__(self):
		super(MessageNotificationsTypes, self).__init__()
		self.set_ids({
			# id починались з 0,
		    # але тут був старий пункт sms: 0
		    'email': 1,
		    'sms_and_email': 2,
		})


	def email(self):
		return self.ids['email']


	def sms_and_email(self):
		return self.ids['sms_and_email']



class Preferences(object):
	CALL_REQUEST_NOTIFICATIONS = CallRequestNotificationsTypes()
	MESSAGE_NOTIFICATIONS = MessageNotificationsTypes()