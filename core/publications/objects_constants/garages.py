#coding=utf-8
from collective.constants import AbstractConstant


class DriveWays(AbstractConstant):
	def __init__(self):
		super(DriveWays, self).__init__()
		self.set_ids({
			'asphalt': 0,
		    'ground': 1,
			'unknown': 2,
		})


	def asphalt(self):
		return self.ids['asphalt']

	def ground(self):
		return self.ids['ground']

	def unknown(self):
		return self.ids['unknown']
GARAGE_DRIVE_WAYS = DriveWays()