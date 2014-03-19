from collective.constants import AbstractConstant


class TicketsStates(AbstractConstant):
	def __init__(self):
		super(TicketsStates, self).__init__()
		self.set_ids({
			'open': 0,
		    'closed': 1,
		})

	def open(self):
		return self.ids['open']

	def closed(self):
		return self.ids['closed']

TICKETS_STATES = TicketsStates()


class MessagesTypes(AbstractConstant):
	def __init__(self):
		super(MessagesTypes, self).__init__()
		self.set_ids({
			'clients_message': 0,
		    'supports_message': 1,
		})

	def clients_message(self):
		return self.ids['clients_message']

	def supports_message(self):
		return self.ids['supports_message']

TICKETS_MESSAGES_TYPES = MessagesTypes()