#coding=utf-8
from collective.constants import AbstractConstant
from core.publications.objects_constants.rooms import ROOMS_WC_LOCATION


class TradeBuildingTypes(AbstractConstant):
	def __init__(self):
		super(TradeBuildingTypes).__init__()
		self.set_ids({
			'residential': 0, # житлова будівля
		    'entertainment': 1,
		    'business': 3,
		    'administrative': 4,
		    'separate': 5,
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