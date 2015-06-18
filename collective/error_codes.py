class ErrorCodes(object):
	def __init__(self):
		self.ids = {
			'ObjectDoesNotExist': 0,
		    'RecordDoesNotExist': 1,
		}

		if len(set(self.ids.values())) < len(self.ids.values()):
			raise ValueError('Duplicate id detected.')

	# system functions
	def all(self):
		return self.ids

	def values(self):
		return self.ids.values()


	def ObjectDoesNotExist(self):
		return self.ids['ObjectDoesNotExist']

	def RecordDoesNotExist(self):
		return self.ids['RecordDoesNotExist']

ERROR_CODES = ErrorCodes()