from collective.constants import AbstractConstant


class FlatBuildingsTypes(AbstractConstant):
	def __init__(self):
		super(FlatBuildingsTypes, self).__init__()
		self.set_ids({
			'panel': 1,
		    'brick': 2,
		    'khrushchovka': 3,
		    'brezhnevka': 4,
		    'stalinka': 5,
		    'monolith': 6,
		    'pre_revolutionary': 7,
		    'small_family': 8,
		    'individual_project': 9,
		    'custom': 0,
		    'unknown': 10,
		})

	def panel(self):
		return self.ids['panel']

	def brick(self):
		return self.ids['brick']

	def khrushchovka(self):
		return self.ids['khrushchovka']

	def brezhnevka(self):
		return self.ids['brezhnevka']

	def stalinka(self):
		return self.ids['stalinka']

	def monolith(self):
		return self.ids['monolith']

	def pre_revolutionary(self):
		return self.ids['pre_revolutionary']

	def small_family(self):
		return self.ids['small_family']

	def individual_project(self):
		return self.ids['individual_project']

	def custom(self):
		return self.ids['custom']

	def unknown(self):
		return self.ids['unknown']
FLAT_BUILDING_TYPES = FlatBuildingsTypes()


class FlatTypes(AbstractConstant):
	def __init__(self):
		super(FlatTypes, self).__init__()
		self.set_ids({
			'custom': 0,
			'small_family': 1,
		    'separate': 2,
		    'communal': 3,
		    'two_level': 4,
		    'studio': 5,
		})

	def custom(self):
		return self.ids['custom']

	def small_family(self):
		return self.ids['small_family']

	def separate(self):
		return self.ids['separate']

	def communal(self):
		return self.ids['communal']

	def two_level(self):
		return self.ids['two_level']

	def studio(self):
		return self.ids['studio']
FLAT_TYPES = FlatTypes()


class FlatRoomsPlanningTypes(AbstractConstant):
	def __init__(self):
		super(FlatRoomsPlanningTypes, self).__init__()
		self.set_ids({
			'adjacent': 0,
			'separate': 1,
		    'separate_adjacent': 2,
		    'free': 3,
		})

	def adjacent(self):
		return self.ids['adjacent']

	def separate(self):
		return self.ids['separate']

	def separate_adjacent(self):
		return self.ids['separate_adjacent']

	def free(self):
		return self.ids['free']
FLAT_ROOMS_PLANNINGS = FlatRoomsPlanningTypes()