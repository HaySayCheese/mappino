class AbstractConstant(object):
	def __init__(self):
		self.ids = {
			'0': '',
			'1': '',
			'2': '',
			'3': '',
			'4': '',
			'5': '',
			'6': '',
			'7': '',
		}

	def set_ids(self, ids_dict):
		if len(set(ids_dict.values())) < len(ids_dict.values()):
			raise ValueError('Duplicate id detected.')
		self.ids = ids_dict

	# system functions
	def records(self):
		return self.ids

	def values(self):
		return self.ids.values()

	def keys(self):
		return self.ids.keys()