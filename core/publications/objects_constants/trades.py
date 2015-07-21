#coding=utf-8
from collective.constants import AbstractConstant


class TradeBuildingTypes(AbstractConstant):
	def __init__(self):
		super(TradeBuildingTypes, self).__init__()
		self.set_ids({
			'residential': 0, # житлова будівля
		    'entertainment': 1,
		    'business': 2,
		    'administrative': 3,
		    'separate': 4,
		})

	def residential(self):
		return self.ids['residential']

	def entertainment(self):
		return self.ids['entertainment']

	def business(self):
		return self.ids['business']

	def administrative(self):
		return self.ids['administrative']

	def separate(self):
		return self.ids['separate']
TRADE_BUILDING_TYPES = TradeBuildingTypes()