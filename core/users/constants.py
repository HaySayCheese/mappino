from collective.constants import AbstractConstant


class CallRequestNotifications(AbstractConstant):
	def __init__(self):
		super(CallRequestNotifications, self).__init__()
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



class MessageNotificationTypes(AbstractConstant):
	def __init__(self):
		super(MessageNotificationTypes, self).__init__()
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



class Preferences(object):
	CALL_REQUEST_NOTIFICATIONS = CallRequestNotifications()
	MESSAGE_NOTIFICATIONS = CallRequestNotifications()