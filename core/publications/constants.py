#coding=utf-8
from collective.constants import AbstractConstant


class ObjectTypes(AbstractConstant):
	def __init__(self):
		super(ObjectTypes, self).__init__()
		self.set_ids({
			# Жилая недвижимость
			'house':      0,
		    'flat':       1,
		    'apartments': 2,
			'dacha':      3,
		    'cottage':    4,
			'room':       5,

		    # Коммерческая недвижимость
		    'trade':      6,
			'office':     7,
		    'warehouse':  8,
		    'business':   9,
		    'catering':   10,

		    # Другая недвижимость
		    'garage':     11,
		    'land':       12,
		})

		self.commercial_estate = [
			self.ids['trade'],
			self.ids['office'],
			self.ids['warehouse'],
			self.ids['business'],
			self.ids['catering'],
		]


	# жилая недвижимость
	def house(self):
		return self.ids['house']

	def flat(self):
		return self.ids['flat']

	def apartments(self):
		return self.ids['apartments']

	def dacha(self):
		return self.ids['dacha']

	def cottage(self):
		return self.ids['cottage']

	def room(self):
		return self.ids['room']


	# ком. недвижимость
	def trade(self):
		return self.ids['trade']

	def office(self):
		return self.ids['office']

	def warehouse(self):
		return self.ids['warehouse']

	def business(self):
		return self.ids['business']

	def catering(self):
		return self.ids['catering']


	# другая недвижимость
	def garage(self):
		return self.ids['garage']

	def land(self):
		return self.ids['land']
OBJECTS_TYPES = ObjectTypes()



HEAD_MODELS = {
    #OBJECTS_TYPES.flat():       FlatsHeads,
    #OBJECTS_TYPES.apartments(): ApartmentsHeads,
    #OBJECTS_TYPES.house():      HousesHeads,
    #OBJECTS_TYPES.dacha():      DachasHeads,
    #OBJECTS_TYPES.cottage():    CottagesHeads,
    #OBJECTS_TYPES.room():       RoomsHeads,
    #
    #OBJECTS_TYPES.trade():      TradesHeads,
    #OBJECTS_TYPES.office():     OfficesHeads,
    #OBJECTS_TYPES.warehouse():  WarehousesHeads,
    #OBJECTS_TYPES.business():   BusinessesHeads,
    #OBJECTS_TYPES.catering():   CateringsHeads,
    #
    #OBJECTS_TYPES.garage():     GaragesHeads,
    #OBJECTS_TYPES.land():       LandsHeads,
}

