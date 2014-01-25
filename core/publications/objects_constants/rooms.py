from collective.constants import AbstractConstant
from core.publications.objects_constants.flats import FLAT_BUILDING_TYPES


ROOMS_BUILDINGS_TYPES = FLAT_BUILDING_TYPES


class RoomsRoomsPlaningTypes(AbstractConstant):
	def __init__(self):
		super(RoomsRoomsPlaningTypes).__init__()
		self.set_ids({
			'adjacent': 0,
			'separate': 1,
		    'separate_adjacent': 2,
		})

	def adjacent(self):
		return self.ids['adjacent']

	def separate(self):
		return self.ids['separate']

	def separate_adjacent(self):
		return self.ids['separate_adjacent']
ROOMS_ROOMS_PLANING_TYPES  = RoomsRoomsPlaningTypes()


class RoomsWCLocation(AbstractConstant):
	def __init__(self):
		super(RoomsWCLocation).__init__()
		self.set_ids({
			'on_the_floor': 0,
		    'inside': 1,
		    'none': 2,
		    'unknown': 3,
		})

	def on_the_floor(self):
		return self.ids['on_the_floor']

	def inside(self):
		return self.ids['inside']

	def none(self):
		return self.ids['none']

	def unknown(self):
		return self.ids['unknown']
ROOMS_WC_LOCATION  = RoomsWCLocation()