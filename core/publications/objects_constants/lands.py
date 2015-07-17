#coding=utf-8
from collective.constants import AbstractConstant


class DriveWays(AbstractConstant):
	def __init__(self):
		super(DriveWays, self).__init__()
		self.set_ids({
			'asphalt': 0,
		    'ground': 1,
		    'none': 2,
			'unknown': 3,
		})

	def asphalt(self):
		return self.ids['asphalt']

	def ground(self):
		return self.ids['ground']

	def none(self):
		return self.ids['none']

	def unknown(self):
		return self.ids['unknown']
LAND_DRIVEWAYS = DriveWays()