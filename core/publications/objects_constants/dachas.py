#coding=utf-8
from collective.constants import AbstractConstant


class DachaWC(AbstractConstant):
	def __init__(self):
		super(DachaWC, self).__init__()
		self.set_ids({
			'present': 0,
			'absent': 1,
			'unknown': 2,
		})

	def present(self):
		return self.ids['present']

	def absent(self):
		return self.ids['absent']

	def unknown(self):
		return self.ids['unknown']
DACHA_WC = DachaWC()


class WCLocation(AbstractConstant):
	def __init__(self):
		super(WCLocation, self).__init__()
		self.set_ids({
			'outside': 0,
			'inside': 1,
			'inside_and_outside':   2,
			'unknown':   3,
		})

	def inside(self):
		return self.ids['inside']

	def outside(self):
		return self.ids['outside']

	def inside_and_outside(self):
		return self.ids['inside_and_outside']

	def unknown(self):
		return self.ids['unknown']
DACHA_WC_LOCATIONS = WCLocation()