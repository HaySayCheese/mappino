#coding=utf-8
from django.db import models

from core.publications.abstract_models import LivingHeadModel, BodyModel, LivingRentTermsModel, CommercialRentTermsModel, PhotosModel, SaleTermsModel, CommercialHeadModel, AbstractModel
from core.publications.constants import MARKET_TYPES, OBJECT_CONDITIONS, FLOOR_TYPES, HEATING_TYPES, INDIVIDUAL_HEATING_TYPES, CURRENCIES, \
	OBJECTS_TYPES
from core.publications.exceptions import EmptyFloor, EmptyTotalArea, EmptyLivingArea, EmptyRoomsCount, EmptyFloorsCount, \
	EmptyHallsArea, EmptyHallsCount, EmptyCabinetsCount
from core.publications.objects_constants.apartments import APARTMENTS_BUILDINGS_TYPES, APARTMENTS_FLAT_TYPES, APARTMENTS_ROOMS_PLANNING_TYPES
from core.publications.objects_constants.cottages import COTTAGE_RENT_TYPES, COTTAGE_SALE_TYPES
from core.publications.objects_constants.dachas import DACHA_WC_LOCATIONS, DACHA_WC
from core.publications.objects_constants.flats import FLAT_BUILDING_TYPES, FLAT_TYPES, FLAT_ROOMS_PLANNINGS
from core.publications.objects_constants.garages import GARAGE_DRIVE_WAYS
from core.publications.objects_constants.houses import HOUSE_RENT_TYPES, HOUSE_SALE_TYPES
from core.publications.objects_constants.lands import LAND_DRIVEWAYS
from core.publications.objects_constants.rooms import ROOMS_BUILDINGS_TYPES, ROOMS_ROOMS_PLANNING_TYPES, ROOMS_WC_LOCATION
from core.publications.objects_constants.trades import TRADE_BUILDING_TYPES


class FlatsPhotos(PhotosModel):
	class Meta:
		db_table = 'img_flats_photos'

	destination_dir_name = 'flats/'
	hid = models.ForeignKey('FlatsHeads', db_index=True)


class FlatsSaleTerms(SaleTermsModel):
	class Meta:
		db_table = 'o_flats_sale_terms'


class FlatsRentTerms(LivingRentTermsModel):
	class Meta:
		db_table = 'o_flats_rent_terms'


class FlatsBodies(BodyModel):
	class Meta:
		db_table = 'o_flats_bodies'

	substitutions = {
		'market_type': {
			MARKET_TYPES.new_building(): u'новостройка',
			MARKET_TYPES.secondary_market(): u'вторичный рынок',
		},
		'building_type': {
			FLAT_BUILDING_TYPES.panel(): u'панель',
			FLAT_BUILDING_TYPES.brick(): u'кирпич',
			FLAT_BUILDING_TYPES.khrushchovka(): u'хрущевка',
			FLAT_BUILDING_TYPES.brezhnevka(): u'брежневка',
			FLAT_BUILDING_TYPES.stalinka(): u'сталинка',
			FLAT_BUILDING_TYPES.monolith(): u'монолит',
			FLAT_BUILDING_TYPES.pre_revolutionary(): u'дореволюционный',
			FLAT_BUILDING_TYPES.small_family(): u'малосемейка',
			FLAT_BUILDING_TYPES.individual_project(): u'индивидуальный проект',
		},
		'flat_type': {
			FLAT_TYPES.small_family(): u'малосемейка',
			FLAT_TYPES.separate(): u'отдельная',
			FLAT_TYPES.communal(): u'коммунальная',
			FLAT_TYPES.two_level(): u'двухуровневая',
			FLAT_TYPES.studio(): u'студия',
		},
		'rooms_planning': {
			FLAT_ROOMS_PLANNINGS.adjacent(): u'смежная',
			FLAT_ROOMS_PLANNINGS.separate(): u'раздельная',
			FLAT_ROOMS_PLANNINGS.separate_adjacent(): u'раздельно-смежная',
			FLAT_ROOMS_PLANNINGS.free(): u'свободная',
		},
		'condition': {
			OBJECT_CONDITIONS.cosmetic_repair(): u'косметический ремонт',
			OBJECT_CONDITIONS.living(): u'жилое / советское',
			OBJECT_CONDITIONS.euro_repair(): u'евроремонт',
			OBJECT_CONDITIONS.design_repair(): u'дизайнерский ремонт',
			OBJECT_CONDITIONS.cosmetic_repair_needed(): u'требуется косметический ремонт',
			OBJECT_CONDITIONS.unfinished_repair(): u'неоконченный ремонт',
			OBJECT_CONDITIONS.for_finishing(): u'под чистовую отделку',
		},
		'floor_types': {
			FLOOR_TYPES.mansard(): u'мансардное помещение',
			FLOOR_TYPES.ground(): u'цокольное помещение'
		},
	}


	market_type_sid = models.SmallIntegerField(default=MARKET_TYPES.secondary_market()) # Тип ринку

	building_type_sid = models.SmallIntegerField(default=FLAT_BUILDING_TYPES.brick())
	custom_building_type = models.TextField(null=True)
	build_year = models.PositiveSmallIntegerField(null=True)
	flat_type_sid = models.SmallIntegerField(default=FLAT_TYPES.separate()) # тип квартири
	custom_flat_type = models.TextField(null=True)
	rooms_planning_sid = models.SmallIntegerField(default=FLAT_ROOMS_PLANNINGS.separate()) # планування кімнат
	condition_sid = models.SmallIntegerField(default=OBJECT_CONDITIONS.living()) # загальний стан

	floor = models.SmallIntegerField(null=True) # номер поверху
	floor_type_sid = models.SmallIntegerField(default=FLOOR_TYPES.floor()) # тип поверху: мансарда, цоколь, звичайний поверх і т.д
	floors_count = models.SmallIntegerField(null=True)
	ceiling_height = models.FloatField(null=True) # висота стелі

	total_area = models.FloatField(null=True)
	living_area = models.FloatField(null=True)
	kitchen_area = models.FloatField(null=True)

	rooms_count = models.PositiveSmallIntegerField(null=True)
	bedrooms_count = models.PositiveSmallIntegerField(null=True)
	vcs_count = models.SmallIntegerField(null=True)
	balconies_count = models.SmallIntegerField(null=True)
	loggias_count = models.SmallIntegerField(null=True)


	# Опалення
	heating_type_sid = models.SmallIntegerField(default=HEATING_TYPES.central())
	custom_heating_type = models.TextField(null=True) # якщо нічого не вказано в heating_type_sid
	# якщо вибрано ідивідуальний тип опалення в heating_type_sid
	ind_heating_type_sid = models.SmallIntegerField(default=INDIVIDUAL_HEATING_TYPES.gas())
	custom_ind_heating_type = models.TextField(null=True) # якщо нічого не вказано в ind_heating_type_sid

	# Інші зручності
	electricity = models.BooleanField(default=False)
	gas = models.BooleanField(default=False)
	hot_water = models.BooleanField(default=False)
	cold_water = models.BooleanField(default=False)

	security_alarm = models.BooleanField(default=False)
	fire_alarm = models.BooleanField(default=False)
	lift = models.BooleanField(default=False)
	add_facilities = models.TextField(null=True) # дод. відомості про зручності

	# Комунікації
	phone = models.BooleanField(default=False)
	internet = models.BooleanField(default=False)
	mobile_coverage = models.BooleanField(default=False) # покриття моб. операторами
	cable_tv = models.BooleanField(default=False) # кабельне / супутникове тб

	# Дод. будівлі
	garage = models.BooleanField(default=False) # гараж / паркомісце
	playground = models.BooleanField(default=False)
	add_buildings = models.TextField(null=True)

	# Поряд знаходиться
	kindergarten = models.BooleanField(default=False)
	school = models.BooleanField(default=False)
	market = models.BooleanField(default=False)
	transport_stop = models.BooleanField(default=False)
	entertainment = models.BooleanField(default=False) # розважальні установи
	sport_center = models.BooleanField(default=False)
	park = models.BooleanField(default=False)
	add_showplaces = models.TextField(null=True)

	#-- validation
	def check_extended_fields(self):
		if self.floor is None:
			raise EmptyFloor('Floor is None.')
		if self.total_area is None:
			raise EmptyTotalArea('Total area is None.')
		if self.living_area is None:
			raise EmptyLivingArea('Living area is None.')
		if self.rooms_count is None:
			raise EmptyRoomsCount('Rooms count is None.')


	#-- output
	def print_title(self):
		if self.title is None:
			return u''

		# if without_trailing_dot:
		# 	if self.title[-1] == u'.':
		# 		return self.title[:-1]
		# else:
		# 	if self.title[-1] != u'.':
		# 		return self.title + u'.'
		return self.title



	def print_description(self):
		if not self.description:
			return u''
		return self.description


	def print_market_type(self):
		return self.substitutions['market_type'][self.market_type_sid]


	def print_building_type(self):
		building_type = self.substitutions['building_type'].get(self.building_type_sid)
		if not building_type:
			return building_type

		if self.building_type_sid == FLAT_BUILDING_TYPES.custom() and self.custom_building_type:
			return self.custom_building_type
		return u''


	def print_build_year(self):
		if not self.build_year:
			return u''
		return unicode(self.build_year) + u' г.'


	def print_flat_type(self):
		flat_type = self.substitutions['flat_type'].get(self.flat_type_sid)
		if not flat_type:
			return flat_type

		if self.flat_type_sid == FLAT_TYPES.custom() and self.custom_flat_type:
			return self.custom_flat_type
		return u''


	def print_rooms_planning(self):
		return self.substitutions['rooms_planning'][self.rooms_planning_sid]


	def print_condition(self):
		return self.substitutions['condition'][self.condition_sid]


	def print_floor(self):
		# Поле "этаж" пропущено в floor_types умисно, щоб воно зайвий раз не потрапляло у видачу.
		floor_type = self.substitutions['floor_types'].get(self.floor_type_sid, u'')
		if floor_type:
			return floor_type
		return unicode(self.floor)


	def print_floors_count(self):
		if not self.floors_count:
			return u''
		return unicode(self.floors_count)


	def print_total_area(self):
		if not self.total_area:
			return u''
		return "{:.2f}".format(self.total_area).rstrip('0').rstrip('.')  + u'м²'


	def print_living_area(self):
		if not self.living_area:
			return u''
		return "{:.2f}".format(self.living_area).rstrip('0').rstrip('.')  + u'м²'


	def print_kitchen_area(self):
		if not self.kitchen_area:
			return u''
		return "{:.2f}".format(self.kitchen_area).rstrip('0').rstrip('.')  + u'м²'


	def print_rooms_count(self):
		if self.rooms_planning_sid == FLAT_ROOMS_PLANNINGS.free() or not self.rooms_count:
			return u''
		return unicode(self.rooms_count)


	def print_bedrooms_count(self):
		if not self.bedrooms_count:
			return u''
		return unicode(self.bedrooms_count)


	def print_vcs_count(self):
		if not self.vcs_count:
			return u''
		return unicode(self.vcs_count)


	def print_balconies_count(self):
		if not self.balconies_count:
			return u''
		return unicode(self.balconies_count)


	def print_loggias_count(self):
		if not self.loggias_count:
			return u''
		return unicode(self.loggias_count)


	def print_ceiling_height(self):
		if self.ceiling_height is None:
			return u''
		return unicode(self.ceiling_height) + u' м'


	def print_facilities(self):
		facilities = u''

		# Опалення (пункт "невідомо" не виводиться)
		if self.heating_type_sid == HEATING_TYPES.none():
			facilities += u'отопление отсутствует'
		elif self.heating_type_sid == HEATING_TYPES.central():
			facilities += u'центральное отопление'
		elif self.heating_type_sid == HEATING_TYPES.individual():
			facilities += u'индивидуальное отопление'
			if self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.electricity():
				facilities += u' (электричество)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.gas():
				facilities += u' (газ)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.firewood():
				facilities += u' (дрова)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.other():
				if self.custom_ind_heating_type is not None:
					facilities += u' ('+self.custom_ind_heating_type + u')'
		elif self.heating_type_sid == HEATING_TYPES.other():
			facilities += u'отопление — ' + self.custom_heating_type

		if self.electricity:
			facilities += u', электричество'
		if self.gas:
			facilities += u', газ'
		if self.hot_water:
			facilities += u', гарячая вода'
		if self.cold_water:
			facilities += u', холодная вода'

		if self.security_alarm and self.fire_alarm:
			facilities += u', охранная и пожарная сигнализации'
		else:
			if self.security_alarm:
				facilities += u', охранная сигнализация'
			if self.fire_alarm:
				facilities += u', пожарная сигнализация'
		if self.lift:
			facilities += u', лифт'

		if self.add_facilities:
			facilities = facilities + '. ' + self.add_facilities

		if facilities[:2] == u', ':
			facilities = facilities[2:]
		return facilities if facilities else u''


	def print_communications(self):
		communications = u''
		if self.phone:
			communications += u', телефон'
		if self.internet:
			communications += u', интернет'
		if self.mobile_coverage:
			communications += u', покрытие мобильными операторами'
		if self.cable_tv:
			communications += u', кабельное телевидение'

		if communications:
			return communications[2:]
		return u''


	def print_provided_add_buildings(self):
		buildings = u''
		if self.garage:
			buildings += u', гараж / паркоместо'
		if self.playground:
			buildings += u', детская площадка'

		if self.add_buildings:
			buildings += u'. ' + self.add_buildings

		if buildings:
			return buildings[2:]
		return u''


	def print_showplaces(self):
		showplaces = u''
		if self.kindergarten:
			showplaces += u', детский сад'
		if self.school:
			showplaces += u', школа'
		if self.market:
			showplaces += u', рынок'
		if self.transport_stop:
			showplaces += u', остановка общ. транспорта'
		if self.park:
			showplaces += u', парк'
		if self.sport_center:
			showplaces += u', спортивно-оздоровительный центр'
		if self.entertainment:
			showplaces += u', развлекательные заведения'

		if self.add_showplaces:
			showplaces += '. ' + self.add_showplaces

		if showplaces:
			return showplaces[2:]
		return u''



class FlatsHeads(LivingHeadModel):
	class Meta:
		db_table = 'o_flats_heads'

	tid = OBJECTS_TYPES.flat()
	photos_model = FlatsPhotos

	body = models.ForeignKey(FlatsBodies)
	sale_terms = models.OneToOneField(FlatsSaleTerms)
	rent_terms = models.OneToOneField(FlatsRentTerms)


class ApartmentsPhotos(PhotosModel):
	class Meta:
		db_table = 'img_apartments_photos'

	destination_dir_name = 'apartments/'
	hid = models.ForeignKey('ApartmentsHeads', db_index=True)


class ApartmentsSaleTerms(SaleTermsModel):
	class Meta:
		db_table = 'o_apartments_sale_terms'


class ApartmentsRentTerms(LivingRentTermsModel):
	class Meta:
		db_table = 'o_apartments_rent_terms'


class ApartmentsBodies(BodyModel):
	class Meta:
		db_table = 'o_apartments_bodies'

	substitutions = {
		'market_type': {
			MARKET_TYPES.new_building(): u'новостройка',
			MARKET_TYPES.secondary_market(): u'вторичный рынок',
		},
		'building_type': {
			FLAT_BUILDING_TYPES.panel(): u'панель',
			FLAT_BUILDING_TYPES.brick(): u'кирпич',
			FLAT_BUILDING_TYPES.khrushchovka(): u'хрущевка',
			FLAT_BUILDING_TYPES.brezhnevka(): u'брежневка',
			FLAT_BUILDING_TYPES.stalinka(): u'сталинка',
			FLAT_BUILDING_TYPES.monolith(): u'монолит',
			FLAT_BUILDING_TYPES.pre_revolutionary(): u'дореволюционный',
			FLAT_BUILDING_TYPES.small_family(): u'малосемейка',
			FLAT_BUILDING_TYPES.individual_project(): u'индивидуальный проект',
		},
		'flat_type': {
			FLAT_TYPES.small_family(): u'малосемейка',
			FLAT_TYPES.separate(): u'отдельная',
			FLAT_TYPES.communal(): u'коммунальная',
			FLAT_TYPES.two_level(): u'двухуровневая',
			FLAT_TYPES.studio(): u'студия',
		},
		'rooms_planning': {
			FLAT_ROOMS_PLANNINGS.adjacent(): u'смежная',
			FLAT_ROOMS_PLANNINGS.separate(): u'раздельная',
			FLAT_ROOMS_PLANNINGS.separate_adjacent(): u'раздельно-смежная',
			FLAT_ROOMS_PLANNINGS.free(): u'свободная',
		},
		'condition': {
			OBJECT_CONDITIONS.cosmetic_repair(): u'косметический ремонт',
			OBJECT_CONDITIONS.living(): u'жилое / советское',
			OBJECT_CONDITIONS.euro_repair(): u'евроремонт',
			OBJECT_CONDITIONS.design_repair(): u'дизайнерский ремонт',
			OBJECT_CONDITIONS.cosmetic_repair_needed(): u'требуется косметический ремонт',
			OBJECT_CONDITIONS.unfinished_repair(): u'неоконченный ремонт',
			OBJECT_CONDITIONS.for_finishing(): u'под чистовую отделку',
		},
		'floor_types': {
			FLOOR_TYPES.mansard(): u'мансарда',
			FLOOR_TYPES.ground(): u'цоколь'
		},
	}


	market_type_sid = models.SmallIntegerField(default=MARKET_TYPES.secondary_market()) # Тип ринку

	building_type_sid = models.SmallIntegerField(default=APARTMENTS_BUILDINGS_TYPES.brick())
	custom_building_type = models.TextField(null=True)
	build_year = models.PositiveSmallIntegerField(null=True)
	flat_type_sid = models.SmallIntegerField(default=APARTMENTS_FLAT_TYPES.separate()) # тип квартири
	custom_flat_type = models.TextField(null=True)
	rooms_planning_sid = models.SmallIntegerField(default=APARTMENTS_ROOMS_PLANNING_TYPES.separate()) # планування кімнат
	condition_sid = models.SmallIntegerField(default=OBJECT_CONDITIONS.living()) # загальний стан

	floor = models.SmallIntegerField(null=True) # номер поверху
	floor_type_sid = models.SmallIntegerField(default=FLOOR_TYPES.floor()) # тип поверху: мансарда, цоколь, звичайний поверх і т.д
	floors_count = models.SmallIntegerField(null=True)
	ceiling_height = models.FloatField(null=True) # висота стелі

	total_area = models.FloatField(null=True)
	living_area = models.FloatField(null=True)
	kitchen_area = models.FloatField(null=True)

	rooms_count = models.PositiveSmallIntegerField(null=True)
	bedrooms_count = models.PositiveSmallIntegerField(null=True)
	vcs_count = models.SmallIntegerField(null=True)
	balconies_count = models.SmallIntegerField(null=True)
	loggias_count = models.SmallIntegerField(null=True)


	# Опалення
	heating_type_sid = models.SmallIntegerField(default=HEATING_TYPES.central())
	custom_heating_type = models.TextField(null=True) # якщо нічого не вказано в heating_type_sid
	# якщо вибрано ідивідуальний тип опалення в heating_type_sid
	ind_heating_type_sid = models.SmallIntegerField(default=INDIVIDUAL_HEATING_TYPES.gas())
	custom_ind_heating_type = models.TextField(null=True) # якщо нічого не вказано в ind_heating_type_sid

	# Інші зручності
	electricity = models.BooleanField(default=False)
	gas = models.BooleanField(default=False)
	hot_water = models.BooleanField(default=False)
	cold_water = models.BooleanField(default=False)

	security_alarm = models.BooleanField(default=False)
	fire_alarm = models.BooleanField(default=False)
	lift = models.BooleanField(default=False)
	add_facilities = models.TextField(null=True) # дод. відомості про зручності

	# Комунікації
	phone = models.BooleanField(default=False)
	internet = models.BooleanField(default=False)
	mobile_coverage = models.BooleanField(default=False) # покриття моб. операторами
	cable_tv = models.BooleanField(default=False) # кабельне / супутникове тб

	# Дод. будівлі
	garage = models.BooleanField(default=False) # гараж / паркомісце
	playground = models.BooleanField(default=False)
	add_buildings = models.TextField(null=True)

	# Поряд знаходиться
	kindergarten = models.BooleanField(default=False)
	school = models.BooleanField(default=False)
	market = models.BooleanField(default=False)
	transport_stop = models.BooleanField(default=False)
	entertainment = models.BooleanField(default=False) # розважальні установи
	sport_center = models.BooleanField(default=False)
	park = models.BooleanField(default=False)
	add_showplaces = models.TextField(null=True)


	#-- validation
	def check_extended_fields(self):
		if self.floor is None:
			raise EmptyFloor('Floor is None.')
		if self.total_area is None:
			raise EmptyTotalArea('Total area is None.')
		if self.living_area is None:
			raise EmptyLivingArea('Living area is None.')
		if self.rooms_count is None:
			raise EmptyRoomsCount('Rooms count is None.')


		#-- output
	def print_title(self):
		if self.title is None:
			return u''

		# if without_trailing_dot:
		# 	if self.title[-1] == u'.':
		# 		return self.title[:-1]
		# else:
		# 	if self.title[-1] != u'.':
		# 		return self.title + u'.'
		return self.title



	def print_description(self):
		if not self.description:
			return u''
		return self.description


	def print_market_type(self):
		return self.substitutions['market_type'][self.market_type_sid]


	def print_building_type(self):
		building_type = self.substitutions['building_type'].get(self.building_type_sid)
		if not building_type:
			return building_type

		if self.building_type_sid == FLAT_BUILDING_TYPES.custom() and self.custom_building_type:
			return self.custom_building_type
		return u''


	def print_build_year(self):
		if not self.build_year:
			return u''
		return unicode(self.build_year) + u' г.'


	def print_flat_type(self):
		flat_type = self.substitutions['flat_type'].get(self.flat_type_sid)
		if not flat_type:
			return flat_type

		if self.flat_type_sid == FLAT_TYPES.custom() and self.custom_flat_type:
			return self.custom_flat_type
		return u''


	def print_rooms_planning(self):
		return self.substitutions['rooms_planning'][self.rooms_planning_sid]


	def print_condition(self):
		return self.substitutions['condition'][self.condition_sid]


	def print_floor(self):
		# Поле "этаж" пропущено в floor_types умисно, щоб воно зайвий раз не потрапляло у видачу.
		floor_type = self.substitutions['floor_types'].get(self.floor_type_sid, u'')
		if floor_type:
			return floor_type
		return unicode(self.floor)


	def print_floors_count(self):
		if not self.floors_count:
			return u''
		return unicode(self.floors_count)


	def print_total_area(self):
		if not self.total_area:
			return u''
		return "{:.2f}".format(self.total_area).rstrip('0').rstrip('.')  + u'м²'


	def print_living_area(self):
		if not self.living_area:
			return u''
		return "{:.2f}".format(self.living_area).rstrip('0').rstrip('.')  + u'м²'


	def print_kitchen_area(self):
		if not self.kitchen_area:
			return u''
		return "{:.2f}".format(self.kitchen_area).rstrip('0').rstrip('.')  + u'м²'


	def print_rooms_count(self):
		if self.rooms_planning_sid == FLAT_ROOMS_PLANNINGS.free() or not self.rooms_count:
			return u''
		return unicode(self.rooms_count)


	def print_bedrooms_count(self):
		if not self.bedrooms_count:
			return u''
		return unicode(self.bedrooms_count)


	def print_vcs_count(self):
		if not self.vcs_count:
			return u''
		return unicode(self.vcs_count)


	def print_balconies_count(self):
		if not self.balconies_count:
			return u''
		return unicode(self.balconies_count)


	def print_loggias_count(self):
		if not self.loggias_count:
			return u''
		return unicode(self.loggias_count)


	def print_ceiling_height(self):
		if self.ceiling_height is None:
			return u''
		return unicode(self.ceiling_height) + u' м'


	def print_facilities(self):
		facilities = u''

		# Опалення (пункт "невідомо" не виводиться)
		if self.heating_type_sid == HEATING_TYPES.none():
			facilities += u'отопление отсутствует'
		elif self.heating_type_sid == HEATING_TYPES.central():
			facilities += u'центральное отопление'
		elif self.heating_type_sid == HEATING_TYPES.individual():
			facilities += u'индивидуальное отопление'
			if self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.electricity():
				facilities += u' (электричество)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.gas():
				facilities += u' (газ)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.firewood():
				facilities += u' (дрова)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.other():
				if self.custom_ind_heating_type is not None:
					facilities += u' ('+self.custom_ind_heating_type + u')'
		elif self.heating_type_sid == HEATING_TYPES.other():
			facilities += u'отопление — ' + self.custom_heating_type

		if self.electricity:
			facilities += u', электричество'
		if self.gas:
			facilities += u', газ'
		if self.hot_water:
			facilities += u', гарячая вода'
		if self.cold_water:
			facilities += u', холодная вода'

		if self.security_alarm and self.fire_alarm:
			facilities += u', охранная и пожарная сигнализации'
		else:
			if self.security_alarm:
				facilities += u', охранная сигнализация'
			if self.fire_alarm:
				facilities += u', пожарная сигнализация'
		if self.lift:
			facilities += u', лифт'

		if self.add_facilities:
			facilities = facilities + '. ' + self.add_facilities

		if facilities[:2] == u', ':
			facilities = facilities[2:]
		return facilities if facilities else u''


	def print_communications(self):
		communications = u''
		if self.phone:
			communications += u', телефон'
		if self.internet:
			communications += u', интернет'
		if self.mobile_coverage:
			communications += u', покрытие мобильными операторами'
		if self.cable_tv:
			communications += u', кабельное телевидение'

		if communications:
			return communications[2:]
		return u''


	def print_provided_add_buildings(self):
		buildings = u''
		if self.garage:
			buildings += u', гараж / паркоместо'
		if self.playground:
			buildings += u', детская площадка'

		if self.add_buildings:
			buildings += u'. ' + self.add_buildings

		if buildings:
			return buildings[2:]
		return u''


	def print_showplaces(self):
		showplaces = u''
		if self.kindergarten:
			showplaces += u', детский сад'
		if self.school:
			showplaces += u', школа'
		if self.market:
			showplaces += u', рынок'
		if self.transport_stop:
			showplaces += u', остановка общ. транспорта'
		if self.park:
			showplaces += u', парк'
		if self.sport_center:
			showplaces += u', спортивно-оздоровительный центр'
		if self.entertainment:
			showplaces += u', развлекательные заведения'

		if self.add_showplaces:
			showplaces += '. ' + self.add_showplaces

		if showplaces:
			return showplaces[2:]
		return u''



class ApartmentsHeads(LivingHeadModel):
	class Meta:
		db_table = 'o_apartments_heads'

	tid = OBJECTS_TYPES.apartments()
	photos_model = ApartmentsPhotos

	body = models.ForeignKey(ApartmentsBodies)
	sale_terms = models.OneToOneField(ApartmentsSaleTerms)
	rent_terms = models.OneToOneField(ApartmentsRentTerms)


class HousesPhotos(PhotosModel):
	class Meta:
		db_table = 'img_houses_photos'

	destination_dir_name = 'houses/'
	hid = models.ForeignKey('HousesHeads', db_index=True)


class HousesSaleTerms(SaleTermsModel):
	class Meta:
		db_table = 'o_houses_sale_terms'

	sale_type_sid = models.SmallIntegerField(default=HOUSE_SALE_TYPES.all_house())


class HousesRentTerms(LivingRentTermsModel):
	class Meta:
		db_table = 'o_houses_rent_terms'

	rent_type_sid = models.SmallIntegerField(default=HOUSE_RENT_TYPES.all_house())


class HousesBodies(BodyModel):
	class Meta:
		db_table = 'o_houses_bodies'

	substitutions = {
		'market_type': {
			MARKET_TYPES.new_building(): u'новостройка',
			MARKET_TYPES.secondary_market(): u'вторичный рынок',
		},
		'condition': {
			OBJECT_CONDITIONS.cosmetic_repair(): u'косметический ремонт',
			OBJECT_CONDITIONS.living(): u'жилое / советское',
			OBJECT_CONDITIONS.euro_repair(): u'евроремонт',
			OBJECT_CONDITIONS.design_repair(): u'дизайнерский ремонт',
			OBJECT_CONDITIONS.cosmetic_repair_needed(): u'требуется косметический ремонт',
			OBJECT_CONDITIONS.unfinished_repair(): u'неоконченный ремонт',
			OBJECT_CONDITIONS.for_finishing(): u'под чистовую отделку',
		},
	}


	market_type_sid = models.SmallIntegerField(default=MARKET_TYPES.secondary_market()) # Тип ринку

	condition_sid = models.SmallIntegerField(default=OBJECT_CONDITIONS.living()) # загальний стан
	total_area = models.FloatField(null=True)
	living_area = models.FloatField(null=True)
	kitchen_area = models.FloatField(null=True)

	mansard = models.BooleanField(default=False) # мансарда
	ground = models.BooleanField(default=False) # цокольний поверх
	lower_floor = models.BooleanField(default=False) # підвал

	floors_count = models.SmallIntegerField(null=True)
	rooms_count = models.PositiveSmallIntegerField(null=True)
	bedrooms_count = models.PositiveSmallIntegerField(null=True)
	vcs_count = models.SmallIntegerField(null=True)


	# Опалення
	heating_type_sid = models.SmallIntegerField(default=HEATING_TYPES.individual())
	custom_heating_type = models.TextField(null=True) # якщо нічого не вказано в heating_type_sid
	# якщо вибрано ідивідуальний тип опалення в heating_type_sid
	ind_heating_type_sid = models.SmallIntegerField(default=INDIVIDUAL_HEATING_TYPES.gas())
	custom_ind_heating_type = models.TextField(null=True) # якщо нічого не вказано в ind_heating_type_sid

	# Інші зручності
	electricity = models.BooleanField(default=False)
	gas = models.BooleanField(default=False)
	sewerage = models.BooleanField(default=False) # каналізація

	hot_water = models.BooleanField(default=False)
	cold_water = models.BooleanField(default=False)
	security_alarm = models.BooleanField(default=False)
	fire_alarm = models.BooleanField(default=False)
	add_facilities = models.TextField(null=True) # дод. відомості про зручності

	# Комунікації
	phone = models.BooleanField(default=False)
	internet = models.BooleanField(default=False)
	mobile_coverage = models.BooleanField(default=False) # покриття моб. операторами
	cable_tv = models.BooleanField(default=False) # кабельне / супутникове тб

	# Дод. будівлі
	garage = models.BooleanField(default=False) # гараж / паркомісце
	fence = models.BooleanField(default=False) # огорожа
	terrace = models.BooleanField(default=False)
	well = models.BooleanField(default=False) # колодязь
	alcove = models.BooleanField(default=False) # альтанка
	kaleyard = models.BooleanField(default=False) # огород
	garden = models.BooleanField(default=False) # сад
	pool = models.BooleanField(default=False)
	cellar = models.BooleanField(default=False) # погреб
	add_buildings = models.TextField(null=True)

	# Поряд знаходиться
	kindergarten = models.BooleanField(default=False)
	school = models.BooleanField(default=False)
	market = models.BooleanField(default=False)
	transport_stop = models.BooleanField(default=False)
	entertainment = models.BooleanField(default=False) # розважальні установи
	sport_center = models.BooleanField(default=False)
	park = models.BooleanField(default=False)
	add_showplaces = models.TextField(null=True)


	# validation
	def check_extended_fields(self):
		if self.total_area is None:
			raise EmptyTotalArea('Total area is None.')
		if self.living_area is None:
			raise EmptyLivingArea('Living area is None.')
		if self.floors_count is None:
			raise EmptyFloorsCount('Floors count is None.')
		if self.rooms_count is None:
			raise EmptyRoomsCount('Rooms count is None.')


	# output
	def print_title(self):
		if not self.title:
			return u''
		return self.title


	def print_description(self):
		if not self.description:
			return u''
		return self.description


	def print_market_type(self):
		return self.substitutions['market_type'][self.market_type_sid]


	def print_condition(self):
		return self.substitutions['condition'][self.condition_sid]


	def print_total_area(self):
		if not self.total_area:
			return u''
		return "{:.2f}".format(self.total_area).rstrip('0').rstrip('.') + u'м²'


	def print_living_area(self):
		if not self.living_area:
			return u''
		return "{:.2f}".format(self.living_area).rstrip('0').rstrip('.') + u'м²'


	def print_kitchen_area(self):
		if not self.kitchen_area:
			return u''
		return "{:.2f}".format(self.kitchen_area).rstrip('0').rstrip('.') + u'м²'


	def print_floors_count(self):
		if not self.floors_count:
			return u''

		floors = u''
		if self.ground:
			floors += u', цоколь'
		if self.lower_floor:
			floors += u', подвал'
		if self.mansard:
			floors += u', мансарда'

		if floors and self.floors_count:
			return unicode(self.floors_count) + u' (' + floors[2:] + u')'
		return unicode(self.floors_count)


	def print_rooms_count(self):
		if not self.rooms_count:
			return u''
		return unicode(self.rooms_count)


	def print_bedrooms_count(self):
		if not self.bedrooms_count:
			return u''
		return unicode(self.bedrooms_count)


	def print_vcs_count(self):
		if not self.vcs_count:
			return u''
		return unicode(self.vcs_count)


	def print_facilities(self):
		facilities = u''

		# Опалення (пункт "невідомо" не виводиться)
		if self.heating_type_sid == HEATING_TYPES.none():
			facilities += u'отопление отсутствует'
		elif self.heating_type_sid == HEATING_TYPES.central():
			facilities += u'центральное отопление'
		elif self.heating_type_sid == HEATING_TYPES.individual():
			facilities += u'индивидуальное отопление'
			if self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.electricity():
				facilities += u' (электричество)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.gas():
				facilities += u' (газ)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.firewood():
				facilities += u' (дрова)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.other():
				if self.custom_ind_heating_type is not None:
					facilities += u' ('+self.custom_ind_heating_type + u')'
		elif self.heating_type_sid == HEATING_TYPES.other():
			facilities += u'отопление: ' + self.custom_heating_type

		if self.electricity:
			facilities += u', электричество'
		if self.gas:
			facilities += u', газ'
		if self.hot_water:
			facilities += u', гарячая вода'
		if self.cold_water:
			facilities += u', холодная вода'
		if self.sewerage:
			facilities += u', канализация'

		if self.security_alarm and self.fire_alarm:
			facilities += u', охранная и пожарная сигнализации'
		else:
			if self.security_alarm:
				facilities += u', охранная сигнализация'
			if self.fire_alarm:
				facilities += u', пожарная сигнализация'


		if self.add_facilities:
			facilities = facilities + '. ' + self.add_facilities

		if facilities[:2] == u', ':
			facilities = facilities[2:]
		return facilities if facilities else u''


	def print_communications(self):
		communications = u''
		if self.phone:
			communications += u', телефон'
		if self.internet:
			communications += u', интернет'
		if self.mobile_coverage:
			communications += u', покрытие мобильными операторами'
		if self.cable_tv:
			communications += u', кабельное телевидение'

		if communications:
			return communications[2:]
		return u''


	def print_provided_add_buildings(self):
		buildings = u''
		if self.fence:
			buildings += u', ограждение участка'
		if self.well:
			buildings += u', колодец'
		if self.garage:
			buildings += u', гараж'
		if self.pool:
			buildings += u', бассейн'
		if self.terrace:
			buildings += u', терраса'
		if self.cellar:
			buildings += u', погреб'
		if self.alcove:
			buildings += u', беседка'
		if self.kaleyard:
			buildings += u', огород'
		if self.garden:
			buildings += u', сад'

		if self.add_buildings:
			buildings += u'. ' + self.add_buildings

		if buildings:
			return buildings[2:]
		return u''


	def print_showplaces(self):
		showplaces = u''
		if self.kindergarten:
			showplaces += u', детский сад'
		if self.school:
			showplaces += u', школа'
		if self.market:
			showplaces += u', рынок'
		if self.transport_stop:
			showplaces += u', остановка общ. транспорта'
		if self.park:
			showplaces += u', парк'
		if self.sport_center:
			showplaces += u', спортивно-оздоровительный центр'
		if self.entertainment:
			showplaces += u', развлекательные заведения'

		if self.add_showplaces:
			showplaces += '. ' + self.add_showplaces

		if showplaces:
			return showplaces[2:]
		return u''



class HousesHeads(LivingHeadModel):
	class Meta:
		db_table = 'o_houses_heads'

	tid = OBJECTS_TYPES.house()
	photos_model = HousesPhotos

	body = models.ForeignKey(HousesBodies)
	sale_terms = models.OneToOneField(HousesSaleTerms)
	rent_terms = models.OneToOneField(HousesRentTerms)


class DachasPhotos(PhotosModel):
	class Meta:
		db_table = 'img_dachas_photos'

	destination_dir_name = 'dachas/'
	hid = models.ForeignKey('DachasHeads', db_index=True)


class DachasSaleTerms(SaleTermsModel):
	class Meta:
		db_table = 'o_dachas_sale_terms'


class DachasRentTerms(LivingRentTermsModel):
	class Meta:
		db_table = 'o_dachas_rent_terms'


class DachasBodies(BodyModel):
	class Meta:
		db_table = 'o_dachas_bodies'

	market_type_sid = models.SmallIntegerField(default=MARKET_TYPES.secondary_market()) # Тип ринку

	condition_sid = models.SmallIntegerField(default=OBJECT_CONDITIONS.living()) # загальний стан
	total_area = models.FloatField(null=True)
	living_area = models.FloatField(null=True)
	kitchen_area = models.FloatField(null=True)

	mansard = models.BooleanField(default=False) # мансарда
	ground = models.BooleanField(default=False) # цокольний поверх
	lower_floor = models.BooleanField(default=False) # підвал

	floors_count = models.SmallIntegerField(null=True)
	rooms_count = models.PositiveSmallIntegerField(null=True)
	bedrooms_count = models.PositiveSmallIntegerField(null=True)

	# vc
	vc_sid = models.SmallIntegerField(default=DACHA_WC.present())
	vc_loc_sid = models.SmallIntegerField(default=DACHA_WC_LOCATIONS.inside())

	# Опалення
	heating_type_sid = models.SmallIntegerField(default=HEATING_TYPES.individual())
	custom_heating_type = models.TextField(null=True) # якщо нічого не вказано в heating_type_sid
	# якщо вибрано ідивідуальний тип опалення в heating_type_sid
	ind_heating_type_sid = models.SmallIntegerField(default=INDIVIDUAL_HEATING_TYPES.gas())
	custom_ind_heating_type = models.TextField(null=True) # якщо нічого не вказано в ind_heating_type_sid

	# Інші зручності
	electricity = models.BooleanField(default=False)
	gas = models.BooleanField(default=False)
	sewerage = models.BooleanField(default=False) # каналізація
	irrigation_water = models.BooleanField(default=False) # вода для поливу

	hot_water = models.BooleanField(default=False)
	cold_water = models.BooleanField(default=False)
	security_alarm = models.BooleanField(default=False)
	fire_alarm = models.BooleanField(default=False)
	add_facilities = models.TextField(null=True) # дод. відомості про зручності

	# Комунікації
	phone = models.BooleanField(default=False)
	internet = models.BooleanField(default=False)
	mobile_coverage = models.BooleanField(default=False) # покриття моб. операторами
	cable_tv = models.BooleanField(default=False) # кабельне / супутникове тб

	# Дод. будівлі
	garage = models.BooleanField(default=False) # гараж / паркомісце
	fence = models.BooleanField(default=False) # огорожа
	terrace = models.BooleanField(default=False)
	well = models.BooleanField(default=False) # колодязь
	alcove = models.BooleanField(default=False) # альтанка
	kaleyard = models.BooleanField(default=False) # огород
	garden = models.BooleanField(default=False) # сад
	pool = models.BooleanField(default=False)
	cellar = models.BooleanField(default=False) # погреб
	add_buildings = models.TextField(null=True)

	# Поряд знаходиться
	kindergarten = models.BooleanField(default=False)
	school = models.BooleanField(default=False)
	market = models.BooleanField(default=False)
	transport_stop = models.BooleanField(default=False)
	entertainment = models.BooleanField(default=False) # розважальні установи
	sport_center = models.BooleanField(default=False)
	park = models.BooleanField(default=False)
	add_showplaces = models.TextField(null=True)


	def check_extended_fields(self):
		if self.total_area is None:
			raise EmptyTotalArea('Total area is None.')
		if self.living_area is None:
			raise EmptyLivingArea('Living area is None.')
		if self.floors_count is None:
			raise EmptyFloorsCount('Floors count is None.')
		if self.rooms_count is None:
			raise EmptyRoomsCount('Rooms count is None.')



class DachasHeads(LivingHeadModel):
	class Meta:
		db_table = 'o_dachas_heads'

	tid = OBJECTS_TYPES.dacha()
	photos_model = DachasPhotos

	body = models.ForeignKey(DachasBodies)
	sale_terms = models.OneToOneField(DachasSaleTerms)
	rent_terms = models.OneToOneField(DachasRentTerms)


class CottagesPhotos(PhotosModel):
	class Meta:
		db_table = 'img_cottages_photos'

	destination_dir_name = 'cottages/'
	hid = models.ForeignKey('CottagesHeads', db_index=True)


class CottagesSaleTerms(SaleTermsModel):
	class Meta:
		db_table = 'o_cottages_sale_terms'

	sale_type_sid = models.SmallIntegerField(default=COTTAGE_SALE_TYPES.all_house())


class CottagesRentTerms(LivingRentTermsModel):
	class Meta:
		db_table = 'o_cottages_rent_terms'

	rent_type_sid = models.SmallIntegerField(default=COTTAGE_RENT_TYPES.all_house())


class CottagesBodies(BodyModel):
	class Meta:
		db_table = 'o_cottages_bodies'

	substitutions = {
		'market_type': {
			MARKET_TYPES.new_building(): u'новостройка',
			MARKET_TYPES.secondary_market(): u'вторичный рынок',
		},
		'condition': {
			OBJECT_CONDITIONS.cosmetic_repair(): u'косметический ремонт',
			OBJECT_CONDITIONS.living(): u'жилое / советское',
			OBJECT_CONDITIONS.euro_repair(): u'евроремонт',
			OBJECT_CONDITIONS.design_repair(): u'дизайнерский ремонт',
			OBJECT_CONDITIONS.cosmetic_repair_needed(): u'требуется косметический ремонт',
			OBJECT_CONDITIONS.unfinished_repair(): u'неоконченный ремонт',
			OBJECT_CONDITIONS.for_finishing(): u'под чистовую отделку',
		},
	}


	sale_type_sid = models.SmallIntegerField(default=COTTAGE_SALE_TYPES.all_house())
	market_type_sid = models.SmallIntegerField(default=MARKET_TYPES.secondary_market()) # Тип ринку

	condition_sid = models.SmallIntegerField(default=OBJECT_CONDITIONS.living()) # загальний стан
	total_area = models.FloatField(null=True)
	living_area = models.FloatField(null=True)
	kitchen_area = models.FloatField(null=True)

	mansard = models.BooleanField(default=False) # мансарда
	ground = models.BooleanField(default=False) # цокольний поверх
	lower_floor = models.BooleanField(default=False) # підвал

	floors_count = models.SmallIntegerField(null=True)
	rooms_count = models.PositiveSmallIntegerField(null=True)
	bedrooms_count = models.PositiveSmallIntegerField(null=True)
	vcs_count = models.SmallIntegerField(null=True)


	# Опалення
	heating_type_sid = models.SmallIntegerField(default=HEATING_TYPES.individual())
	custom_heating_type = models.TextField(null=True) # якщо нічого не вказано в heating_type_sid
	# якщо вибрано ідивідуальний тип опалення в heating_type_sid
	ind_heating_type_sid = models.SmallIntegerField(default=INDIVIDUAL_HEATING_TYPES.gas())
	custom_ind_heating_type = models.TextField(null=True) # якщо нічого не вказано в ind_heating_type_sid

	# Інші зручності
	electricity = models.BooleanField(default=False)
	gas = models.BooleanField(default=False)
	sewerage = models.BooleanField(default=False) # каналізація

	hot_water = models.BooleanField(default=False)
	cold_water = models.BooleanField(default=False)
	security_alarm = models.BooleanField(default=False)
	fire_alarm = models.BooleanField(default=False)
	add_facilities = models.TextField(null=True) # дод. відомості про зручності

	# Комунікації
	phone = models.BooleanField(default=False)
	internet = models.BooleanField(default=False)
	mobile_coverage = models.BooleanField(default=False) # покриття моб. операторами
	cable_tv = models.BooleanField(default=False) # кабельне / супутникове тб

	# Дод. будівлі
	garage = models.BooleanField(default=False) # гараж / паркомісце
	fence = models.BooleanField(default=False) # огорожа
	terrace = models.BooleanField(default=False)
	well = models.BooleanField(default=False) # колодязь
	alcove = models.BooleanField(default=False) # альтанка
	pool = models.BooleanField(default=False)
	add_buildings = models.TextField(null=True)

	# Поряд знаходиться
	kindergarten = models.BooleanField(default=False)
	school = models.BooleanField(default=False)
	market = models.BooleanField(default=False)
	transport_stop = models.BooleanField(default=False)
	entertainment = models.BooleanField(default=False) # розважальні установи
	sport_center = models.BooleanField(default=False)
	park = models.BooleanField(default=False)
	add_showplaces = models.TextField(null=True)

	# validation
	def check_extended_fields(self):
		if self.total_area is None:
			raise EmptyTotalArea('Total area is None.')
		if self.living_area is None:
			raise EmptyLivingArea('Living area is None.')
		if self.floors_count is None:
			raise EmptyFloorsCount('Floors count is None.')
		if self.rooms_count is None:
			raise EmptyRoomsCount('Rooms count is None.')


	# output
	def print_title(self):
		if not self.title:
			return u''
		return self.title


	def print_description(self):
		if not self.description:
			return u''
		return self.description


	def print_market_type(self):
		return self.substitutions['market_type'][self.market_type_sid]


	def print_condition(self):
		return self.substitutions['condition'][self.condition_sid]


	def print_total_area(self):
		if not self.total_area:
			return u''
		return "{:.2f}".format(self.total_area).rstrip('0').rstrip('.')  + u'м²'


	def print_living_area(self):
		if not self.living_area:
			return u''
		return "{:.2f}".format(self.living_area).rstrip('0').rstrip('.')  + u'м²'


	def print_kitchen_area(self):
		if not self.kitchen_area:
			return u''
		return "{:.2f}".format(self.kitchen_area).rstrip('0').rstrip('.')  + u'м²'


	def print_floors_count(self):
		if not self.floors_count:
			return u''

		floors = u''
		if self.ground:
			floors += u', цоколь'
		if self.lower_floor:
			floors += u', подвал'
		if self.mansard:
			floors += u', мансарда'

		if floors and self.floors_count:
			return unicode(self.floors_count) + u' (' + floors[2:] + u')'
		return unicode(self.floors_count)


	def print_rooms_count(self):
		if not self.rooms_count:
			return u''
		return unicode(self.rooms_count)


	def print_bedrooms_count(self):
		if not self.bedrooms_count:
			return u''
		return unicode(self.bedrooms_count)


	def print_vcs_count(self):
		if not self.vcs_count:
			return u''
		return unicode(self.vcs_count)


	def print_facilities(self):
		facilities = u''

		# Опалення (пункт "невідомо" не виводиться)
		if self.heating_type_sid == HEATING_TYPES.none():
			facilities += u'отопление отсутствует'
		elif self.heating_type_sid == HEATING_TYPES.central():
			facilities += u'центральное отопление'
		elif self.heating_type_sid == HEATING_TYPES.individual():
			facilities += u'индивидуальное отопление'
			if self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.electricity():
				facilities += u' (электричество)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.gas():
				facilities += u' (газ)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.firewood():
				facilities += u' (дрова)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.other():
				if self.custom_ind_heating_type is not None:
					facilities += u' ('+self.custom_ind_heating_type + u')'
		elif self.heating_type_sid == HEATING_TYPES.other():
			facilities += u'отопление: ' + self.custom_heating_type

		if self.electricity:
			facilities += u', электричество'
		if self.gas:
			facilities += u', газ'
		if self.hot_water:
			facilities += u', гарячая вода'
		if self.cold_water:
			facilities += u', холодная вода'
		if self.sewerage:
			facilities += u', канализация'

		if self.security_alarm and self.fire_alarm:
			facilities += u', охранная и пожарная сигнализации'
		else:
			if self.security_alarm:
				facilities += u', охранная сигнализация'
			if self.fire_alarm:
				facilities += u', пожарная сигнализация'


		if self.add_facilities:
			facilities = facilities + '. ' + self.add_facilities

		if facilities[:2] == u', ':
			facilities = facilities[2:]
		return facilities if facilities else u''


	def print_communications(self):
		communications = u''
		if self.phone:
			communications += u', телефон'
		if self.internet:
			communications += u', интернет'
		if self.mobile_coverage:
			communications += u', покрытие мобильными операторами'
		if self.cable_tv:
			communications += u', кабельное телевидение'

		if communications:
			return communications[2:]
		return u''


	def print_provided_add_buildings(self):
		buildings = u''
		if self.fence:
			buildings += u', ограждение участка'
		if self.well:
			buildings += u', колодец'
		if self.garage:
			buildings += u', гараж'
		if self.pool:
			buildings += u', бассейн'
		if self.terrace:
			buildings += u', терраса'
		if self.alcove:
			buildings += u', беседка'

		if self.add_buildings:
			buildings += u'. ' + self.add_buildings

		if buildings:
			return buildings[2:]
		return u''


	def print_showplaces(self):
		showplaces = u''
		if self.kindergarten:
			showplaces += u', детский сад'
		if self.school:
			showplaces += u', школа'
		if self.market:
			showplaces += u', рынок'
		if self.transport_stop:
			showplaces += u', остановка общ. транспорта'
		if self.park:
			showplaces += u', парк'
		if self.sport_center:
			showplaces += u', спортивно-оздоровительный центр'
		if self.entertainment:
			showplaces += u', развлекательные заведения'

		if self.add_showplaces:
			showplaces += '. ' + self.add_showplaces

		if showplaces:
			return showplaces[2:]
		return u''



class CottagesHeads(LivingHeadModel):
	class Meta:
		db_table = 'o_cottages_heads'

	tid = OBJECTS_TYPES.cottage()
	photos_model = CottagesPhotos

	body = models.ForeignKey(CottagesBodies)
	sale_terms = models.OneToOneField(CottagesSaleTerms)
	rent_terms = models.OneToOneField(CottagesRentTerms)


class RoomsPhotos(PhotosModel):
	class Meta:
		db_table = 'img_rooms_photos'

	destination_dir_name = 'rooms/'
	hid = models.ForeignKey('RoomsHeads', db_index=True)


class RoomsSaleTerms(SaleTermsModel):
	class Meta:
		db_table = 'o_rooms_sale_terms'


class RoomsRentTerms(LivingRentTermsModel):
	class Meta:
		db_table = 'o_rooms_rent_terms'


class RoomsBodies(BodyModel):
	class Meta:
		db_table = 'o_rooms_bodies'

	substitutions = {
		'market_type': {
			MARKET_TYPES.new_building(): u'новостройка',
			MARKET_TYPES.secondary_market(): u'вторичный рынок',
		},
		'building_type': {
			ROOMS_BUILDINGS_TYPES.panel(): u'панель',
			ROOMS_BUILDINGS_TYPES.brick(): u'кирпич',
			ROOMS_BUILDINGS_TYPES.khrushchovka(): u'хрущевка',
			ROOMS_BUILDINGS_TYPES.brezhnevka(): u'брежневка',
			ROOMS_BUILDINGS_TYPES.stalinka(): u'сталинка',
			ROOMS_BUILDINGS_TYPES.monolith(): u'монолит',
			ROOMS_BUILDINGS_TYPES.pre_revolutionary(): u'дореволюционный',
			ROOMS_BUILDINGS_TYPES.small_family(): u'малосемейка',
			ROOMS_BUILDINGS_TYPES.individual_project(): u'индивидуальный проект',
		},
		'rooms_planning': {
			FLAT_ROOMS_PLANNINGS.adjacent(): u'смежная',
			FLAT_ROOMS_PLANNINGS.separate(): u'раздельная',
			FLAT_ROOMS_PLANNINGS.separate_adjacent(): u'раздельно-смежная',
		},
		'condition': {
			OBJECT_CONDITIONS.cosmetic_repair(): u'косметический ремонт',
			OBJECT_CONDITIONS.living(): u'жилое / советское',
			OBJECT_CONDITIONS.euro_repair(): u'евроремонт',
			OBJECT_CONDITIONS.design_repair(): u'дизайнерский ремонт',
			OBJECT_CONDITIONS.cosmetic_repair_needed(): u'требуется косметический ремонт',
			OBJECT_CONDITIONS.unfinished_repair(): u'неоконченный ремонт',
			OBJECT_CONDITIONS.for_finishing(): u'под чистовую отделку',
		},
		'floor_types': {
			FLOOR_TYPES.mansard(): u'мансарда',
			FLOOR_TYPES.ground(): u'цоколь'
		},
	}


	market_type_sid = models.SmallIntegerField(default=MARKET_TYPES.secondary_market()) # Тип ринку

	building_type_sid = models.SmallIntegerField(default=ROOMS_BUILDINGS_TYPES.brick())
	custom_building_type = models.TextField(null=True)
	build_year = models.PositiveSmallIntegerField(null=True)

	floor = models.SmallIntegerField(null=True) # номер поверху
	floor_type_sid = models.SmallIntegerField(default=FLOOR_TYPES.floor()) # тип поверху: мансарда, цоколь, звичайний поверх і т.д
	floors_count = models.SmallIntegerField(null=True)
	rooms_planning_sid = models.SmallIntegerField(default=ROOMS_ROOMS_PLANNING_TYPES.separate()) # планування кімнат
	condition_sid = models.SmallIntegerField(default=OBJECT_CONDITIONS.living()) # загальний стан

	rooms_count = models.PositiveSmallIntegerField(null=True)
	total_area = models.FloatField(null=True)
	living_area = models.FloatField(null=True)
	kitchen_area = models.FloatField(null=True)

	wc_loc_sid = models.SmallIntegerField(default=ROOMS_WC_LOCATION.inside())

	# Опалення
	heating_type_sid = models.SmallIntegerField(default=HEATING_TYPES.central())
	custom_heating_type = models.TextField(null=True) # якщо нічого не вказано в heating_type_sid
	# якщо вибрано ідивідуальний тип опалення в heating_type_sid
	ind_heating_type_sid = models.SmallIntegerField(default=INDIVIDUAL_HEATING_TYPES.gas())
	custom_ind_heating_type = models.TextField(null=True) # якщо нічого не вказано в ind_heating_type_sid

	# Інші зручності
	electricity = models.BooleanField(default=False)
	gas = models.BooleanField(default=False)
	hot_water = models.BooleanField(default=False)
	cold_water = models.BooleanField(default=False)
	lift = models.BooleanField(default=False)
	add_facilities = models.TextField(null=True) # дод. відомості про зручності

	# Комунікації
	phone = models.BooleanField(default=False)
	internet = models.BooleanField(default=False)
	mobile_coverage = models.BooleanField(default=False) # покриття моб. операторами
	cable_tv = models.BooleanField(default=False) # кабельне / супутникове тб

	# Дод. будівлі
	playground = models.BooleanField(default=False)
	add_buildings = models.TextField(null=True)

	# Поряд знаходиться
	kindergarten = models.BooleanField(default=False)
	school = models.BooleanField(default=False)
	market = models.BooleanField(default=False)
	transport_stop = models.BooleanField(default=False)
	entertainment = models.BooleanField(default=False) # розважальні установи
	sport_center = models.BooleanField(default=False)
	park = models.BooleanField(default=False)
	add_showplaces = models.TextField(null=True)

	# validation
	def check_extended_fields(self):
		if self.floor is None:
			raise EmptyFloor('Floor count is None.')
		if self.rooms_count is None:
			raise EmptyRoomsCount('Rooms count is None.')
		if self.total_area is None:
			raise EmptyTotalArea('Total area is None.')
		if self.living_area is None:
			raise EmptyLivingArea('Living area is None.')


	# output
	def print_title(self):
		if not self.title:
			return u''
		return self.title


	def print_description(self):
		if not self.description:
			return u''
		return self.description


	def print_market_type(self):
		return self.substitutions['market_type'][self.market_type_sid]


	def print_building_type(self):
		building_type = self.substitutions['building_type'].get(self.building_type_sid)
		if building_type is not None:
			return building_type

		if self.building_type_sid == ROOMS_BUILDINGS_TYPES.custom() and self.custom_building_type:
			return self.custom_building_type
		return u''


	def print_build_year(self):
		if not self.build_year:
			return u''
		return unicode(self.build_year) + u' г.'


	def print_floor(self):
		floor_type = self.substitutions['floor_types'].get(self.floor_type_sid, u'')
		if floor_type:
			return floor_type
		return unicode(self.floor)


	def print_floors_count(self):
		if self.floors_count is None:
			return u''
		return unicode(self.floors_count)


	def print_rooms_planning(self):
		return self.substitutions['rooms_planning'][self.rooms_planning_sid]


	def print_condition(self):
		return self.substitutions['condition'][self.condition_sid]


	def print_rooms_count(self):
		if self.rooms_count is None:
			return u''
		return unicode(self.rooms_count)


	def print_total_area(self):
		if self.total_area is None:
			return u''
		return "{:.2f}".format(self.total_area).rstrip('0').rstrip('.')  + u'м²'


	def print_living_area(self):
		if self.living_area is None:
			return u''
		return "{:.2f}".format(self.living_area).rstrip('0').rstrip('.')  + u'м²'


	def print_kitchen_area(self):
		if self.kitchen_area is None:
			return u''
		return "{:.2f}".format(self.kitchen_area).rstrip('0').rstrip('.')  + u'м²'


	def print_facilities(self):
		facilities = u''

		# Опалення (пункт "невідомо" не виводиться)
		if self.heating_type_sid == HEATING_TYPES.none():
			facilities += u'отопление отсутствует'
		elif self.heating_type_sid == HEATING_TYPES.central():
			facilities += u'центральное отопление'
		elif self.heating_type_sid == HEATING_TYPES.individual():
			facilities += u'индивидуальное отопление'
			if self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.electricity():
				facilities += u' (электричество)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.gas():
				facilities += u' (газ)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.firewood():
				facilities += u' (дрова)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.other():
				if self.custom_ind_heating_type is not None:
					facilities += u' ('+self.custom_ind_heating_type + u')'
		elif self.heating_type_sid == HEATING_TYPES.other():
			facilities += u'отопление: ' + self.custom_heating_type

		# Розташування сан. вузла
		if self.wc_loc_sid == ROOMS_WC_LOCATION.inside():
			facilities += u', сан. узел в комнате'
		elif self.wc_loc_sid == ROOMS_WC_LOCATION.on_the_floor():
			facilities += u', сан. узел на этаже'
		elif self.wc_loc_sid == ROOMS_WC_LOCATION.none():
			facilities += u', сан. узел отсутсвует'

		if self.electricity:
			facilities += u', электричество'
		if self.gas:
			facilities += u', газ'
		if self.hot_water:
			facilities += u', гарячая вода'
		if self.cold_water:
			facilities += u', холодная вода'
		if self.lift:
			facilities += u', лифт'

		if self.add_facilities:
			facilities = facilities + '. ' + self.add_facilities

		if facilities[:2] == u', ':
			facilities = facilities[2:]
		return facilities if facilities else u''


	def print_communications(self):
		communications = u''
		if self.phone:
			communications += u', телефон'
		if self.internet:
			communications += u', интернет'
		if self.mobile_coverage:
			communications += u', покрытие мобильными операторами'
		if self.cable_tv:
			communications += u', кабельное телевидение'

		if communications:
			return communications[2:]
		return u''


	def print_provided_add_buildings(self):
		buildings = u''
		if self.playground:
			buildings += u', детская площадка'

		if self.add_buildings:
			buildings += u'. ' + self.add_buildings

		if buildings:
			return buildings[2:]
		return u''


	def print_showplaces(self):
		showplaces = u''
		if self.kindergarten:
			showplaces += u', детский сад'
		if self.school:
			showplaces += u', школа'
		if self.market:
			showplaces += u', рынок'
		if self.transport_stop:
			showplaces += u', остановка общ. транспорта'
		if self.park:
			showplaces += u', парк'
		if self.sport_center:
			showplaces += u', спортивно-оздоровительный центр'
		if self.entertainment:
			showplaces += u', развлекательные заведения'

		if self.add_showplaces:
			showplaces += '. ' + self.add_showplaces

		if showplaces:
			return showplaces[2:]
		return u''



class RoomsHeads(LivingHeadModel):
	class Meta:
		db_table = 'o_rooms_heads'

	tid = OBJECTS_TYPES.room()
	photos_model = RoomsPhotos

	body = models.ForeignKey(RoomsBodies)
	sale_terms = models.OneToOneField(RoomsSaleTerms)
	rent_terms = models.OneToOneField(RoomsRentTerms)


class TradesSaleTerms(SaleTermsModel):
	class Meta:
		db_table = 'o_trades_sale_terms'


class TradesRentTerms(CommercialRentTermsModel):
	class Meta:
		db_table = 'o_trades_rent_terms'


class TradesPhotos(PhotosModel):
	class Meta:
		db_table = 'img_trades_photos'

	destination_dir_name = 'trades/'
	hid = models.ForeignKey('TradesHeads', db_index=True)


class TradesBodies(BodyModel):
	class Meta:
		db_table = 'o_trades_bodies'

	substitutions = {
		'market_type': {
			MARKET_TYPES.new_building(): u'новостройка',
			MARKET_TYPES.secondary_market(): u'вторичный рынок',
		},
		'building_type': {
			TRADE_BUILDING_TYPES.residential(): u'жилое',
			TRADE_BUILDING_TYPES.entertainment(): u'торгово-развлекательный центр',
			TRADE_BUILDING_TYPES.business(): u'бизнес-центр',
			TRADE_BUILDING_TYPES.administrative(): u'административное',
			TRADE_BUILDING_TYPES.separate(): u'отдельное',
		},
		'condition': {
			OBJECT_CONDITIONS.cosmetic_repair(): u'косметический ремонт',
			OBJECT_CONDITIONS.living(): u'жилое / советское',
			OBJECT_CONDITIONS.euro_repair(): u'евроремонт',
			OBJECT_CONDITIONS.design_repair(): u'дизайнерский ремонт',
			OBJECT_CONDITIONS.cosmetic_repair_needed(): u'требуется косметический ремонт',
			OBJECT_CONDITIONS.unfinished_repair(): u'неоконченный ремонт',
			OBJECT_CONDITIONS.for_finishing(): u'под чистовую отделку',
		},
		'floor_types': {
			FLOOR_TYPES.mansard(): u'мансарда',
			FLOOR_TYPES.ground(): u'цоколь'
		},
	}


	market_type_sid = models.SmallIntegerField(default=MARKET_TYPES.secondary_market()) # Тип ринку
	building_type_sid = models.SmallIntegerField(default=TRADE_BUILDING_TYPES.entertainment())
	build_year = models.PositiveSmallIntegerField(null=True)
	condition_sid = models.SmallIntegerField(default=OBJECT_CONDITIONS.cosmetic_repair()) # загальний стан

	floor = models.SmallIntegerField(null=True) # номер поверху
	floor_type_sid = models.SmallIntegerField(default=FLOOR_TYPES.floor()) # тип поверху: мансарда, цоколь, звичайний поверх і т.д
	floors_count = models.SmallIntegerField(null=True)
	mansard = models.BooleanField(default=False) # мансарда
	ground = models.BooleanField(default=False) # цокольний поверх
	lower_floor = models.BooleanField(default=False) # підвал

	halls_count = models.PositiveSmallIntegerField(null=True)
	halls_area = models.FloatField(null=True)
	total_area = models.FloatField(null=True)
	closed_area = models.BooleanField(default=False)

	vcs_count = models.PositiveSmallIntegerField(null=True)
	ceiling_height = models.FloatField(null=True) # висота стелі


	# Опалення
	heating_type_sid = models.SmallIntegerField(default=HEATING_TYPES.central())
	custom_heating_type = models.TextField(null=True) # якщо нічого не вказано в heating_type_sid
	# якщо вибрано ідивідуальний тип опалення в heating_type_sid
	ind_heating_type_sid = models.SmallIntegerField(default=INDIVIDUAL_HEATING_TYPES.gas())
	custom_ind_heating_type = models.TextField(null=True) # якщо нічого не вказано в ind_heating_type_sid

	# Інші зручності
	electricity = models.BooleanField(default=False)
	gas = models.BooleanField(default=False)
	sewerage = models.BooleanField(default=False)

	hot_water = models.BooleanField(default=False)
	cold_water = models.BooleanField(default=False)
	ventilation = models.BooleanField(default=False)

	security_alarm = models.BooleanField(default=False)
	fire_alarm = models.BooleanField(default=False)
	security = models.BooleanField(default=False)

	add_facilities = models.TextField(null=True) # дод. відомості про зручності

	# Комунікації
	phone = models.BooleanField(default=False)
	phone_lines_count = models.PositiveSmallIntegerField(null=True)
	internet = models.BooleanField(default=False)
	mobile_coverage = models.BooleanField(default=False) # покриття моб. операторами
	cable_tv = models.BooleanField(default=False) # кабельне / супутникове тб
	lan = models.BooleanField(default=False)

	# Дод. будівлі
	parking = models.BooleanField(default=False) # гараж / паркомісце
	open_air = models.BooleanField(default=False)
	add_buildings = models.TextField(null=True)

	# Поряд знаходиться
	transport_stop = models.BooleanField(default=False)
	market = models.BooleanField(default=False)
	cafe = models.BooleanField(default=False)
	bank = models.BooleanField(default=False)
	cash_machine = models.BooleanField(default=False)
	entertainment = models.BooleanField(default=False) # розважальні установи
	add_showplaces = models.TextField(null=True)


	# validation
	def check_extended_fields(self):
		if self.floor is None:
			raise EmptyFloor('Floor is None.')
		if self.halls_area is None:
			raise EmptyHallsArea('Halls area is None.')
		if self.halls_count is None:
			raise EmptyHallsCount('Halls count is None.')


	# output
	def print_title(self):
		if self.title is None:
			return u''
		return self.title


	def print_description(self):
		if self.description is None:
			return u''
		return self.description


	def print_market_type(self):
		return self.substitutions['market_type'][self.market_type_sid]


	def print_building_type(self):
		return self.substitutions['building_type'][self.building_type_sid]


	def print_condition(self):
		return self.substitutions['condition'][self.condition_sid]


	#-- output numeric fields
	def print_build_year(self):
		if self.build_year is None:
			return u''
		return unicode(self.build_year) + u' г.'


	def print_floor(self):
		# Поле "этаж" пропущено в floor_types умисно, щоб воно зайвий раз не потрапляло у видачу.
		floor_type = self.substitutions['floor_types'].get(self.floor_type_sid, u'')
		if floor_type:
			return floor_type
		return unicode(self.floor)


	def print_floors_count(self):
		if not self.floors_count:
			return u''

		floors = u''
		if self.ground:
			floors += u', цоколь'
		if self.lower_floor:
			floors += u', подвал'
		if self.mansard:
			floors += u', мансарда'

		if floors and self.floors_count:
			return unicode(self.floors_count) + u' (' + floors[2:] + u')'
		return unicode(self.floors_count)


	def print_halls_count(self):
		if self.halls_count is None:
			return u''
		return unicode(self.halls_count)


	def print_halls_area(self):
		if self.halls_area is None:
			return u''
		return "{:.2f}".format(self.halls_area).rstrip('0').rstrip('.') + u' м²'


	def print_total_area(self):
		if self.total_area is None:
			return u''

		total_area = "{:.2f}".format(self.total_area).rstrip('0').rstrip('.') + u' м²'
		if self.closed_area:
			total_area += u' (закрытая територия)'
		return total_area


	def print_vcs_count(self):
		if self.vcs_count is None:
			return u''
		return unicode(self.vcs_count)


	def print_ceiling_height(self):
		if self.ceiling_height is None:
			return u''
		return unicode(self.ceiling_height) + u' м'


	#-- output formatted strings
	def print_facilities(self):
		facilities = u''

		# Опалення (пункт "невідомо" не виводиться)
		if self.heating_type_sid == HEATING_TYPES.none():
			facilities += u'отопление отсутствует'
		elif self.heating_type_sid == HEATING_TYPES.central():
			facilities += u'центральное отопление'
		elif self.heating_type_sid == HEATING_TYPES.individual():
			facilities += u'индивидуальное отопление'
			if self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.electricity():
				facilities += u' (электричество)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.gas():
				facilities += u' (газ)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.firewood():
				facilities += u' (дрова)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.other():
				if self.custom_ind_heating_type is not None:
					facilities += u' ('+self.custom_ind_heating_type + u')'
		elif self.heating_type_sid == HEATING_TYPES.other():
			facilities += u'отопление: ' + self.custom_heating_type

		if self.electricity:
			facilities += u', электричество'
		if self.gas:
			facilities += u', газ'
		if self.sewerage:
			facilities += u', канализация'
		if self.hot_water:
			facilities += u', гарячая вода'
		if self.cold_water:
			facilities += u', холодная вода'
		if self.ventilation:
			facilities += u', вентиляция'

		if self.security_alarm and self.fire_alarm:
			facilities += u', охранная и пожарная сигнализации'
		else:
			if self.security_alarm:
				facilities += u', охранная сигнализация'
			if self.fire_alarm:
				facilities += u', пожарная сигнализация'

		if self.security:
			facilities += u', охрана'

		if self.add_facilities:
			facilities = facilities + '. ' + self.add_facilities

		if facilities[:2] == u', ':
			facilities = facilities[2:]
		return facilities if facilities else u''


	def print_add_facilities(self):
		if self.add_facilities is None:
			return u''
		return self.add_facilities


	def print_communications(self):
		communications = u''
		if self.phone:
			communications += u', телефон'
			if self.phone_lines_count:
				communications += u' (количество линий - ' + unicode(self.phone_lines_count) + u')'

		if self.internet:
			communications += u', интернет'
		if self.mobile_coverage:
			communications += u', покрытие мобильными операторами'
		if self.cable_tv:
			communications += u', кабельное телевидение'
		if self.lan:
			communications += u', локальная сеть'

		if communications:
			return communications[2:].capitalize() + u"."
		return u''


	def print_provided_add_buildings(self):
		buildings = u''
		if self.parking:
			buildings += u', парковка'
		if self.open_air:
			buildings += u', открытая площадка'

		if self.add_buildings:
			buildings += u'. ' + self.add_buildings

		if buildings:
			return buildings[2:]
		return buildings[2:] if buildings else u''


	def print_showplaces(self):
		showplaces = u''
		if self.transport_stop:
			showplaces += u', остановка общ. транспорта'
		if self.bank:
			showplaces += u', отделения банка'
		if self.cash_machine:
			showplaces += u', банкомат'
		if self.cafe:
			showplaces += u', кафе / ресторан'
		if self.market:
			showplaces += u', рынок / супермаркет'
		if self.entertainment:
			showplaces += u', развлекательные заведения'

		if self.add_showplaces:
			showplaces += '. ' + self.add_showplaces

		if showplaces:
			return showplaces[2:].capitalize() + u'.'
		return u''


class TradesHeads(CommercialHeadModel):
	class Meta:
		db_table = 'o_trades_heads'

	tid = OBJECTS_TYPES.trade()
	photos_model = TradesPhotos

	body = models.ForeignKey(TradesBodies)
	sale_terms = models.OneToOneField(TradesSaleTerms)
	rent_terms = models.OneToOneField(TradesRentTerms)


class OfficesSaleTerms(SaleTermsModel):
	class Meta:
		db_table = 'o_offices_sale_terms'


class OfficesRentTerms(CommercialRentTermsModel):
	class Meta:
		db_table = 'o_offices_rent_terms'

	furniture = models.BooleanField(default=False)
	air_conditioning = models.BooleanField(default=False)


class OfficesPhotos(PhotosModel):
	class Meta:
		db_table = 'img_offices_photos'

	destination_dir_name = 'offices/'
	hid = models.ForeignKey('OfficesHeads', db_index=True)


class OfficesBodies(BodyModel):
	class Meta:
		db_table = 'o_offices_bodies'

	substitutions = {
		'market_type': {
			MARKET_TYPES.new_building(): u'новостройка',
			MARKET_TYPES.secondary_market(): u'вторичный рынок',
		},
		'building_type': {
			TRADE_BUILDING_TYPES.residential(): u'жилое',
			TRADE_BUILDING_TYPES.business(): u'бизнес-центр',
			TRADE_BUILDING_TYPES.administrative(): u'административное',
			TRADE_BUILDING_TYPES.separate(): u'отдельное',
		},
		'condition': {
			OBJECT_CONDITIONS.cosmetic_repair(): u'косметический ремонт',
			OBJECT_CONDITIONS.euro_repair(): u'евроремонт',
			OBJECT_CONDITIONS.design_repair(): u'дизайнерский ремонт',
			OBJECT_CONDITIONS.cosmetic_repair_needed(): u'требуется косметический ремонт',
			OBJECT_CONDITIONS.unfinished_repair(): u'неоконченный ремонт',
			OBJECT_CONDITIONS.for_finishing(): u'под чистовую отделку',
		},
		'floor_types': {
			FLOOR_TYPES.mansard(): u'мансарда',
			FLOOR_TYPES.ground(): u'цоколь'
		},
	}


	market_type_sid = models.SmallIntegerField(default=MARKET_TYPES.secondary_market()) # Тип ринку
	building_type_sid = models.SmallIntegerField(default=TRADE_BUILDING_TYPES.business())
	build_year = models.PositiveSmallIntegerField(null=True)
	condition_sid = models.SmallIntegerField(default=OBJECT_CONDITIONS.cosmetic_repair()) # загальний стан

	floor = models.SmallIntegerField(null=True) # номер поверху
	floor_type_sid = models.SmallIntegerField(default=FLOOR_TYPES.floor()) # тип поверху: мансарда, цоколь, звичайний поверх і т.д
	floors_count = models.SmallIntegerField(null=True)

	cabinets_count = models.PositiveSmallIntegerField(null=True)
	cabinets_area = models.FloatField(null=True)
	total_area = models.FloatField(null=True)
	closed_area = models.BooleanField(default=False)

	vcs_count = models.PositiveSmallIntegerField(null=True)
	ceiling_height = models.FloatField(null=True) # висота стелі


	# Опалення
	heating_type_sid = models.SmallIntegerField(default=HEATING_TYPES.central())
	custom_heating_type = models.TextField(null=True) # якщо нічого не вказано в heating_type_sid
	# якщо вибрано ідивідуальний тип опалення в heating_type_sid
	ind_heating_type_sid = models.SmallIntegerField(default=INDIVIDUAL_HEATING_TYPES.gas())
	custom_ind_heating_type = models.TextField(null=True) # якщо нічого не вказано в ind_heating_type_sid

	# Інші зручності
	hot_water = models.BooleanField(default=False)
	cold_water = models.BooleanField(default=False)
	kitchen = models.BooleanField(default=False)

	security_alarm = models.BooleanField(default=False)
	fire_alarm = models.BooleanField(default=False)
	security = models.BooleanField(default=False)

	add_equipment = models.TextField(null=True) # наявність техніки та меблів
	add_facilities = models.TextField(null=True) # дод. відомості про зручності

	# Комунікації
	phone = models.BooleanField(default=False)
	phone_lines_count = models.PositiveSmallIntegerField(null=True)
	internet = models.BooleanField(default=False)
	mobile_coverage = models.BooleanField(default=False) # покриття моб. операторами
	cable_tv = models.BooleanField(default=False) # кабельне / супутникове тб
	lan = models.BooleanField(default=False)

	# Дод. будівлі
	parking = models.BooleanField(default=False) # гараж / паркомісце
	open_air = models.BooleanField(default=False)
	add_buildings = models.TextField(null=True)

	# Поряд знаходиться
	transport_stop = models.BooleanField(default=False)
	market = models.BooleanField(default=False)
	cafe = models.BooleanField(default=False)
	bank = models.BooleanField(default=False)
	cash_machine = models.BooleanField(default=False)
	entertainment = models.BooleanField(default=False) # розважальні установи
	add_showplaces = models.TextField(null=True)


	# validation
	def check_extended_fields(self):
		if self.floor is None:
			raise EmptyFloor('Floor is None.')
		if self.cabinets_count is None:
			raise EmptyCabinetsCount('Cabinets count is None.')


	# output
	def print_title(self):
		if not self.title:
			return u''
		return self.title


	def print_description(self):
		if not self.description:
			return u''
		return self.description


	def print_market_type(self):
		return self.substitutions['market_type'][self.market_type_sid]


	def print_building_type(self):
		return self.substitutions['building_type'][self.building_type_sid]


	def print_build_year(self):
		if not self.build_year:
			return u''
		return unicode(self.build_year) + u' г.'


	def print_condition(self):
		return self.substitutions['condition'][self.condition_sid]


	def print_floor(self):
		# Поле "этаж" пропущено в floor_types умисно, щоб воно зайвий раз не потрапляло у видачу.
		floor_type = self.substitutions['floor_types'].get(self.floor_type_sid, u'')
		if floor_type:
			return floor_type
		return unicode(self.floor)


	def print_floors_count(self):
		if not self.floors_count:
			return u''
		return unicode(self.floors_count)


	def print_cabinets_count(self):
		if not self.cabinets_count:
			return u''
		return unicode(self.cabinets_count)


	def print_total_area(self):
		if not self.total_area:
			return u''

		total_area = "{:.2f}".format(self.total_area).rstrip('0').rstrip('.') + u' м²'
		if self.closed_area:
			total_area += u' (закрытая територия)'
		return total_area


	def print_vcs_count(self):
		if not self.vcs_count:
			return u''
		return unicode(self.vcs_count)


	def print_ceiling_height(self):
		if not self.ceiling_height:
			return u''
		return unicode(self.ceiling_height) + u' м'


	#-- output formatted strings
	def print_facilities(self):
		facilities = u''

		# Опалення (пункт "невідомо" не виводиться)
		if self.heating_type_sid == HEATING_TYPES.none():
			facilities += u'отопление отсутствует'
		elif self.heating_type_sid == HEATING_TYPES.central():
			facilities += u'центральное отопление'
		elif self.heating_type_sid == HEATING_TYPES.individual():
			facilities += u'индивидуальное отопление'
			if self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.electricity():
				facilities += u' (электричество)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.gas():
				facilities += u' (газ)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.firewood():
				facilities += u' (дрова)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.other():
				if self.custom_ind_heating_type is not None:
					facilities += u' ('+self.custom_ind_heating_type + u')'
		elif self.heating_type_sid == HEATING_TYPES.other():
			facilities += u'отопление: ' + self.custom_heating_type

		if self.kitchen:
			facilities += u', кухня'
		if self.hot_water:
			facilities += u', гарячая вода'
		if self.cold_water:
			facilities += u', холодная вода'

		if self.security_alarm and self.fire_alarm:
			facilities += u', охранная и пожарная сигнализации'
		else:
			if self.security_alarm:
				facilities += u', охранная сигнализация'
			if self.fire_alarm:
				facilities += u', пожарная сигнализация'

		if self.security:
			facilities += u', охрана'

		if self.add_facilities:
			facilities = facilities + '. ' + self.add_facilities

		if facilities[:2] == u', ':
			facilities = facilities[2:]
		return facilities if facilities else u''


	def print_communications(self):
		communications = u''
		if self.phone:
			communications += u', телефон'
			if self.phone_lines_count:
				communications += u' (количество линий - ' + unicode(self.phone_lines_count) + u')'

		if self.internet:
			communications += u', интернет'
		if self.mobile_coverage:
			communications += u', покрытие мобильными операторами'
		if self.cable_tv:
			communications += u', кабельное телевидение'
		if self.lan:
			communications += u', локальная сеть'

		if communications:
			return communications[2:].capitalize() + u"."
		return u''


	def print_provided_add_buildings(self):
		buildings = u''
		if self.parking:
			buildings += u', парковка'
		if self.open_air:
			buildings += u', открытая площадка'

		if self.add_buildings:
			buildings += u'.' + self.add_buildings

		return buildings[2:] if buildings else u''


	def print_showplaces(self):
		showplaces = u''
		if self.transport_stop:
			showplaces += u', остановка общ. транспорта'
		if self.bank:
			showplaces += u', отделения банка'
		if self.cash_machine:
			showplaces += u', банкомат'
		if self.cafe:
			showplaces += u', кафе / ресторан'
		if self.market:
			showplaces += u', рынок / супермаркет'
		if self.entertainment:
			showplaces += u', развлекательные заведения'

		if self.add_showplaces:
			showplaces += u'. ' + self.add_showplaces

		if showplaces:
			return showplaces[2:].capitalize() + u'.'
		return u''



class OfficesHeads(CommercialHeadModel):
	class Meta:
		db_table = 'o_offices_heads'

	tid = OBJECTS_TYPES.office()
	photos_model = OfficesPhotos

	body = models.ForeignKey(OfficesBodies)
	sale_terms = models.OneToOneField(OfficesSaleTerms)
	rent_terms = models.OneToOneField(OfficesRentTerms)


class WarehousesSaleTerms(SaleTermsModel):
	class Meta:
		db_table = 'o_warehouses_sale_terms'


class WarehousesRentTerms(CommercialRentTermsModel):
	class Meta:
		db_table = 'o_warehouses_rent_terms'

	furniture = models.BooleanField(default=False)
	air_conditioning = models.BooleanField(default=False)


class WarehousesPhotos(PhotosModel):
	class Meta:
		db_table = 'img_warehouses_photos'

	destination_dir_name = 'warehouses/'
	hid = models.ForeignKey('WarehousesHeads', db_index=True)


class WarehousesBodies(BodyModel):
	class Meta:
		db_table = 'o_warehouses_bodies'

	substitutions = {
		'market_type': {
			MARKET_TYPES.new_building(): u'новостройка',
			MARKET_TYPES.secondary_market(): u'вторичный рынок',
		},
	}


	market_type_sid = models.SmallIntegerField(default=MARKET_TYPES.secondary_market()) # Тип ринку
	area = models.FloatField(null=True)
	plot_area = models.FloatField(null=True) # площа участку
	open_space = models.BooleanField(default=False) # вільне плаування
	closed_area = models.BooleanField(default=False) # закрита територія

	# Опалення
	heating_type_sid = models.SmallIntegerField(default=HEATING_TYPES.central())
	custom_heating_type = models.TextField(null=True) # якщо нічого не вказано в heating_type_sid
	# якщо вибрано ідивідуальний тип опалення в heating_type_sid
	ind_heating_type_sid = models.SmallIntegerField(default=INDIVIDUAL_HEATING_TYPES.gas())
	custom_ind_heating_type = models.TextField(null=True) # якщо нічого не вказано в ind_heating_type_sid

	# Інші зручності
	electricity = models.BooleanField(default=False)
	gas = models.BooleanField(default=False)
	sewerage = models.BooleanField(default=False)

	hot_water = models.BooleanField(default=False)
	cold_water = models.BooleanField(default=False)
	ventilation = models.BooleanField(default=False)

	security_alarm = models.BooleanField(default=False)
	fire_alarm = models.BooleanField(default=False)
	security = models.BooleanField(default=False)

	add_facilities = models.TextField(null=True) # дод. відомості про зручності

	# Комунікації
	phone = models.BooleanField(default=False)
	phone_lines_count = models.PositiveSmallIntegerField(null=True)
	internet = models.BooleanField(default=False)
	mobile_coverage = models.BooleanField(default=False) # покриття моб. операторами
	lan = models.BooleanField(default=False)

	# Дод. будівлі
	parking = models.BooleanField(default=False) # гараж / паркомісце
	ramp = models.BooleanField(default=False) # авторампа
	storeroom = models.BooleanField(default=False) # підсобка
	offices = models.BooleanField(default=False)
	cathead = models.BooleanField(default=False) # кран-балка
	vc = models.BooleanField(default=False) # уборна
	add_buildings = models.TextField(null=True) # дод. відомості про зручності

	# підїздні шляхи
	railway = models.BooleanField(default=False)
	asphalt = models.BooleanField(default=False)
	concrete = models.BooleanField(default=False)
	ground = models.BooleanField(default=False)
	add_driveways = models.TextField(null=True)

	# Поряд знаходиться
	transport_stop = models.BooleanField(default=False)
	market = models.BooleanField(default=False)
	cafe = models.BooleanField(default=False)
	bank = models.BooleanField(default=False)
	cash_machine = models.BooleanField(default=False)
	refueling = models.BooleanField(default=False) # автозапрака
	railway_station = models.BooleanField(default=False)
	add_showplaces = models.TextField(null=True)


	# validation
	def check_extended_fields(self):
		if self.area is None:
			raise EmptyHallsArea('Halls area is None.')
		if self.plot_area is None:
			raise EmptyPlotArea('Halls count is None.')


	# output
	def print_title(self):
		if not self.title:
			return u''
		return self.title


	def print_description(self):
		if not self.description:
			return u''
		return self.description


	def print_market_type(self):
		return self.substitutions['market_type'][self.market_type_sid]


	def print_halls_area(self):
		if not self.area:
			return u''

		area = "{:.2f}".format(self.area).rstrip('0').rstrip('.') + u' м²'
		if self.open_space:
			area += u' (свободная планировка)'
		return area


	def print_plot_area(self):
		if not self.plot_area:
			return u''

		area = "{:.2f}".format(self.plot_area).rstrip('0').rstrip('.') + u' м²'
		if self.closed_area:
			area += u' (закрытая територия)'
		return area


	def print_facilities(self):
		facilities = u''

		# Опалення (пункт "невідомо" не виводиться)
		if self.heating_type_sid == HEATING_TYPES.none():
			facilities += u'отопление отсутствует'
		elif self.heating_type_sid == HEATING_TYPES.central():
			facilities += u'центральное отопление'
		elif self.heating_type_sid == HEATING_TYPES.individual():
			facilities += u'индивидуальное отопление'
			if self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.electricity():
				facilities += u' (электричество)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.gas():
				facilities += u' (газ)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.firewood():
				facilities += u' (дрова)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.other():
				if self.custom_ind_heating_type is not None:
					facilities += u' ('+self.custom_ind_heating_type + u')'
		elif self.heating_type_sid == HEATING_TYPES.other():
			facilities += u'отопление: ' + self.custom_heating_type

		if self.electricity:
			facilities += u', электричество'
		if self.gas:
			facilities += u', газ'
		if self.sewerage:
			facilities += u', канализация'
		if self.hot_water:
			facilities += u', гарячая вода'
		if self.cold_water:
			facilities += u', холодная вода'
		if self.ventilation:
			facilities += u', вентиляция'

		if self.security_alarm and self.fire_alarm:
			facilities += u', охранная и пожарная сигнализации'
		else:
			if self.security_alarm:
				facilities += u', охранная сигнализация'
			if self.fire_alarm:
				facilities += u', пожарная сигнализация'

		if self.security:
			facilities += u', охрана'

		if self.add_facilities:
			facilities += u'. ' + self.add_facilities

		if facilities[:2] == u', ':
			facilities = facilities[2:]
		return(facilities.capitalize() + u'.') if facilities else u''


	def print_communications(self):
		communications = u''
		if self.phone:
			communications += u', телефон'
			if self.phone_lines_count:
				communications += u' (количество линий - ' + unicode(self.phone_lines_count) + u')'

		if self.internet:
			communications += u', интернет'
		if self.mobile_coverage:
			communications += u', покрытие мобильными операторами'
		if self.lan:
			communications += u', локальная сеть'

		if communications:
			return communications[2:].capitalize() + u"."
		return u''


	def print_provided_add_buildings(self):
		buildings = u''
		if self.ramp:
			buildings += u', авторампа'
		if self.parking:
			buildings += u', парковка'
		if self.cathead:
			buildings += u', кран-балка'
		if self.offices:
			buildings += u', офисные помещения'
		if self.storeroom:
			buildings += u', подсобка / кладовая'
		if self.vc:
			buildings += u', уборная'

		if self.add_buildings:
			buildings += u'. ' + self.add_buildings

		return buildings[2:].capitalize() + u'.' if buildings else u''


	def print_driveways(self):
		driveways = u''
		if self.railway:
			driveways += u', Ж/Д ветка'
		if self.asphalt:
			driveways += u', асфальт'
		if self.concrete:
			driveways += u', бетон'
		if self.ground:
			driveways += u', грунт'

		if self.add_driveways:
			driveways += u'. ' + self.add_driveways.capitalize()

		return driveways[2:].capitalize() + u'.' if driveways else u''


	def print_showplaces(self):
		showplaces = u''
		if self.transport_stop:
			showplaces += u', остановка общ. транспорта'
		if self.bank:
			showplaces += u', отделения банка'
		if self.cash_machine:
			showplaces += u', банкомат'
		if self.cafe:
			showplaces += u', кафе'
		if self.market:
			showplaces += u', рынок / супермаркет'
		if self.railway:
			showplaces += u', Ж/Д станция'
		if self.refueling:
			showplaces += u', заправка'

		if self.add_showplaces:
			showplaces += u'. ' + self.add_showplaces

		if showplaces:
			return showplaces[2:].capitalize() + u'.'
		return u''


class WarehousesHeads(CommercialHeadModel):
	class Meta:
		db_table = 'o_warehouses_heads'

	tid = OBJECTS_TYPES.warehouse()
	photos_model = WarehousesPhotos

	body = models.ForeignKey(WarehousesBodies)
	sale_terms = models.OneToOneField(WarehousesSaleTerms)
	rent_terms = models.OneToOneField(WarehousesRentTerms)


class BusinessesSaleTerms(SaleTermsModel):
	class Meta:
		db_table = 'o_business_sale_terms'


class BusinessesRentTerms(CommercialRentTermsModel):
	class Meta:
		db_table = 'o_business_rent_terms'


class BusinessesPhotos(PhotosModel):
	class Meta:
		db_table = 'img_business_photos'

	destination_dir_name = 'businesses/'
	hid = models.ForeignKey('BusinessesHeads', db_index=True)


class BusinessesBodies(BodyModel):
	class Meta:
		db_table = 'o_business_bodies'

	substitutions = {
		'market_type': {
			MARKET_TYPES.new_building(): u'новостройка',
			MARKET_TYPES.secondary_market(): u'вторичный рынок',
		},
		'building_type': {
			TRADE_BUILDING_TYPES.residential(): u'жилое',
			TRADE_BUILDING_TYPES.entertainment(): u'торгово-развлекательный центр',
			TRADE_BUILDING_TYPES.business(): u'бизнес-центр',
			TRADE_BUILDING_TYPES.administrative(): u'административное',
			TRADE_BUILDING_TYPES.separate(): u'отдельное',
		},
		'condition': {
			OBJECT_CONDITIONS.cosmetic_repair(): u'косметический ремонт',
			OBJECT_CONDITIONS.living(): u'жилое / советское',
			OBJECT_CONDITIONS.euro_repair(): u'евроремонт',
			OBJECT_CONDITIONS.design_repair(): u'дизайнерский ремонт',
			OBJECT_CONDITIONS.cosmetic_repair_needed(): u'требуется косметический ремонт',
			OBJECT_CONDITIONS.unfinished_repair(): u'неоконченный ремонт',
			OBJECT_CONDITIONS.for_finishing(): u'под чистовую отделку',
		},
		'floor_types': {
			FLOOR_TYPES.mansard(): u'мансарда',
			FLOOR_TYPES.ground(): u'цоколь'
		},
	}


	age = models.FloatField(null=True)
	workers_count = models.PositiveIntegerField(null=True)
	monthly_costs = models.DecimalField(null=True, max_digits=AbstractModel.max_price_symbols_count, decimal_places=2)
	mc_currency_sid = models.SmallIntegerField(default=CURRENCIES.dol())
	annual_receipts = models.DecimalField(null=True, max_digits=AbstractModel.max_price_symbols_count, decimal_places=2)
	ar_currency_sid = models.SmallIntegerField(default=CURRENCIES.dol())
	share = models.FloatField(null=True)

	building_type_sid = models.SmallIntegerField(default=TRADE_BUILDING_TYPES.entertainment())
	build_year = models.PositiveSmallIntegerField(null=True)
	condition_sid = models.SmallIntegerField(default=OBJECT_CONDITIONS.living()) # загальний стан

	floor = models.SmallIntegerField(null=True) # номер поверху
	floor_type_sid = models.SmallIntegerField(default=FLOOR_TYPES.floor()) # тип поверху: мансарда, цоколь, звичайний поверх і т.д
	floors_count = models.SmallIntegerField(null=True)
	mansard = models.BooleanField(default=False) # мансарда
	ground = models.BooleanField(default=False) # цокольний поверх
	lower_floor = models.BooleanField(default=False) # підвал

	total_area = models.FloatField(null=True)
	closed_area = models.BooleanField(default=False)
	plot_area = models.FloatField(null=True) # площа участку
	halls_area = models.FloatField(null=True) # площа приміщень

	halls_count = models.PositiveSmallIntegerField(null=True)

	# Опалення
	heating_type_sid = models.SmallIntegerField(default=HEATING_TYPES.central())
	custom_heating_type = models.TextField(null=True) # якщо нічого не вказано в heating_type_sid
	# якщо вибрано ідивідуальний тип опалення в heating_type_sid
	ind_heating_type_sid = models.SmallIntegerField(default=INDIVIDUAL_HEATING_TYPES.gas())
	custom_ind_heating_type = models.TextField(null=True) # якщо нічого не вказано в ind_heating_type_sid

	# Інші зручності
	electricity = models.BooleanField(default=False)
	gas = models.BooleanField(default=False)
	sewerage = models.BooleanField(default=False)

	hot_water = models.BooleanField(default=False)
	cold_water = models.BooleanField(default=False)
	ventilation = models.BooleanField(default=False)

	security_alarm = models.BooleanField(default=False)
	fire_alarm = models.BooleanField(default=False)
	security = models.BooleanField(default=False)

	add_facilities = models.TextField(null=True) # дод. відомості про зручності

	# Комунікації
	phone = models.BooleanField(default=False)
	phone_lines_count = models.PositiveSmallIntegerField(null=True)
	internet = models.BooleanField(default=False)
	mobile_coverage = models.BooleanField(default=False) # покриття моб. операторами
	cable_tv = models.BooleanField(default=False) # кабельне / супутникове тб
	lan = models.BooleanField(default=False)

	# Дод. будівлі
	parking = models.BooleanField(default=False) # гараж / паркомісце
	open_air = models.BooleanField(default=False)
	add_buildings = models.TextField(null=True)

	# Поряд знаходиться
	transport_stop = models.BooleanField(default=False)
	market = models.BooleanField(default=False)
	cafe = models.BooleanField(default=False)
	bank = models.BooleanField(default=False)
	cash_machine = models.BooleanField(default=False)
	entertainment = models.BooleanField(default=False) # розважальні установи
	add_showplaces = models.TextField(null=True)


	# validation
	def check_extended_fields(self):
		if self.floor is None:
			raise EmptyFloor('Floor is None.')
		if self.total_area is None:
			raise EmptyTotalArea('Total area count is None.')


	# output
	def print_title(self):
		if not self.title:
			return u''
		return self.title


	def print_description(self):
		if not self.description:
			return u''
		return self.description


	def print_monthly_cost(self):
		# todo: змінити для видачі по всім валютам окремо
		if not self.monthly_costs:
			return u'' # WARN: необов’язкове поле

		cost = "{:.2f}".format(self.monthly_costs).rstrip('0').rstrip('.')
		if self.mc_currency_sid == CURRENCIES.dol():
			cost += u' дол. США'
		elif self.mc_currency_sid == CURRENCIES.eur():
			cost += u' евро'
		elif self.mc_currency_sid == CURRENCIES.uah():
			cost += u' грн.'
		return cost
	
	
	def print_annual_receipts(self):
		# todo: змінити для видачі по всім валютам окремо
		if not self.annual_receipts:
			return u'' # WARN: необов’язкове поле

		cost = "{:.2f}".format(self.annual_receipts).rstrip('0').rstrip('.')
		if self.ar_currency_sid == CURRENCIES.dol():
			cost += u' дол. США'
		elif self.ar_currency_sid == CURRENCIES.eur():
			cost += u' евро'
		elif self.ar_currency_sid == CURRENCIES.uah():
			cost += u' грн.'
		return cost
	
	
	def print_age(self):
		if not self.age:
			# Якщо вік бізнесу — 0, все одно не показувати.
			# Перевірка на not це передбачає.
			return u'' # не обов’язкове поле може бути відсутнім

		age = "{:.2f}".format(self.age).rstrip('0').rstrip('.')

		# Відмінювання
		if age.split(u'.')[0][-1] == u'1':
			age += u' год'
		elif age.split(u'.')[0][-1] in [u'2', u'3', u'4']:
			age += u' года'
		else:
			age += u' лет'
		return age


	def print_workers_count(self):
		if not self.workers_count:
			# Якщо к-сть працівників — 0, все одно не показувати.
			# Перевірка на not це передбачає.
			return u'' # необов’язкове поле
		return unicode(self.workers_count) + u' чел.'


	def print_share(self):
		if not self.share:
			# Якщо відсоткова доля — 0, все одно не показувати.
			# Перевірка на not це передбачає.
			return u'' # необов’язкове поле
		return "{:.2f}".format(self.share) + u'%'


	def print_building_type(self):
		return self.substitutions['building_type'][self.building_type_sid]


	def print_build_year(self):
		if not self.build_year:
			# Якщо рік побудови — 0, все одно не показувати.
			# Перевірка на not це передбачає.
			return u''
		return unicode(self.build_year) + u' г.'


	def print_condition(self):
		return self.substitutions['condition'][self.condition_sid]


	def print_floor(self):
		# Поле "этаж" пропущено в floor_types умисно, щоб воно зайвий раз не потрапляло у видачу.
		floor_type = self.substitutions['floor_types'].get(self.floor_type_sid, u'')
		if floor_type:
			return floor_type
		return unicode(self.floor)


	def print_floors_count(self):
		if not self.floors_count:
			return u''

		floors = u''
		if self.ground:
			floors += u', цоколь'
		if self.lower_floor:
			floors += u', подвал'
		if self.mansard:
			floors += u', мансарда'

		if floors and self.floors_count:
			return unicode(self.floors_count) + u' (' + floors[2:] + u')'
		return unicode(self.floors_count)


	def print_extra_floors(self):
		floors = u''
		if self.ground:
			floors += u', цокольный этаж'
		if self.lower_floor:
			floors += u', подвал'
		if self.mansard:
			floors += u', мансарда'

		if floors[:2] == u', ':
			floors = floors[2:]
		return floors


	def print_total_area(self):
		if not self.total_area:
			return u''

		area = "{:.2f}".format(self.total_area).rstrip('0').rstrip('.') + u' м²'
		if self.closed_area:
			area += u' (закрытая територия)'
		return area


	def print_plot_area(self):
		if not self.plot_area:
			return u''
		return "{:.2f}".format(self.plot_area).rstrip('0').rstrip('.') + u' м²'


	def print_halls_area(self):
		if not self.halls_area:
			return u''
		return "{:.2f}".format(self.halls_area).rstrip('0').rstrip('.') + u' м²'


	def print_facilities(self):
		facilities = u''

		# Опалення (пункт "невідомо" не виводиться)
		if self.heating_type_sid == HEATING_TYPES.none():
			facilities += u'отопление отсутствует'
		elif self.heating_type_sid == HEATING_TYPES.central():
			facilities += u'центральное отопление'
		elif self.heating_type_sid == HEATING_TYPES.individual():
			facilities += u'индивидуальное отопление'
			if self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.electricity():
				facilities += u' (электричество)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.gas():
				facilities += u' (газ)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.firewood():
				facilities += u' (дрова)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.other():
				if self.custom_ind_heating_type is not None:
					facilities += u' ('+self.custom_ind_heating_type + u')'
		elif self.heating_type_sid == HEATING_TYPES.other():
			facilities += u'отопление: ' + self.custom_heating_type

		if self.electricity:
			facilities += u', электричество'
		if self.gas:
			facilities += u', газ'
		if self.sewerage:
			facilities += u', канализация'
		if self.hot_water:
			facilities += u', гарячая вода'
		if self.cold_water:
			facilities += u', холодная вода'
		if self.ventilation:
			facilities += u', вентиляция'

		if self.security_alarm and self.fire_alarm:
			facilities += u', охранная и пожарная сигнализации'
		else:
			if self.security_alarm:
				facilities += u', охранная сигнализация'
			if self.fire_alarm:
				facilities += u', пожарная сигнализация'

		if self.security:
			facilities += u', охрана'

		if self.add_facilities:
			facilities += '. ' + self.add_facilities

		if facilities[:2] == u', ':
			facilities = facilities[2:]
		return(facilities.capitalize() + u'.') if facilities else u''


	def print_communications(self):
		communications = u''
		if self.phone:
			communications += u', телефон'
			if self.phone_lines_count:
				communications += u' (количество линий - ' + unicode(self.phone_lines_count) + u')'

		if self.internet:
			communications += u', интернет'
		if self.mobile_coverage:
			communications += u', покрытие мобильными операторами'
		if self.lan:
			communications += u', локальная сеть'

		if communications:
			return communications[2:].capitalize() + u"."
		return u''


	def print_add_buildings(self):
		buildings = u''
		if self.parking:
			buildings += u', парковка'
		if self.open_air:
			buildings += u', открытая площадка'

		if self.add_buildings:
			buildings += u'. ' + self.add_buildings

		if buildings:
			return buildings[2:].capitalize() + u"."
		return u''


	def print_showplaces(self):
		showplaces = u''
		if self.transport_stop:
			showplaces += u', остановка общ. транспорта'
		if self.bank:
			showplaces += u', отделения банка'
		if self.cash_machine:
			showplaces += u', банкомат'
		if self.cafe:
			showplaces += u', кафе / ресторан'
		if self.market:
			showplaces += u', рынок / супермаркет'
		if self.entertainment:
			showplaces += u', развлекательные заведения'

		if self.add_showplaces:
			showplaces += u'. ' + self.add_showplaces

		if showplaces:
			return showplaces[2:].capitalize() + u'.'
		return u''



class BusinessesHeads(CommercialHeadModel):
	class Meta:
		db_table = 'o_business_heads'

	tid = OBJECTS_TYPES.business()
	photos_model = BusinessesPhotos

	body = models.ForeignKey(BusinessesBodies)
	sale_terms = models.OneToOneField(BusinessesSaleTerms)
	rent_terms = models.OneToOneField(BusinessesRentTerms)


class CateringsSaleTerms(SaleTermsModel):
	class Meta:
		db_table = 'o_caterings_sale_terms'


class CateringsRentTerms(CommercialRentTermsModel):
	class Meta:
		db_table = 'o_caterings_rent_terms'


class CateringsPhotos(PhotosModel):
	class Meta:
		db_table = 'img_caterings_photos'

	destination_dir_name = 'caterings/'
	hid = models.ForeignKey('CateringsHeads', db_index=True)


class CateringsBodies(BodyModel):
	class Meta:
		db_table = 'o_caterings_bodies'

	substitutions = {
		'market_type': {
			MARKET_TYPES.new_building(): u'новостройка',
			MARKET_TYPES.secondary_market(): u'вторичный рынок',
		},
		'building_type': {
			TRADE_BUILDING_TYPES.residential(): u'жилое',
			TRADE_BUILDING_TYPES.entertainment(): u'торгово-развлекательный центр',
			TRADE_BUILDING_TYPES.business(): u'бизнес-центр',
			TRADE_BUILDING_TYPES.administrative(): u'административное',
			TRADE_BUILDING_TYPES.separate(): u'отдельное',
		},
		'condition': {
			OBJECT_CONDITIONS.cosmetic_repair(): u'косметический ремонт',
			OBJECT_CONDITIONS.living(): u'жилое / советское',
			OBJECT_CONDITIONS.euro_repair(): u'евроремонт',
			OBJECT_CONDITIONS.design_repair(): u'дизайнерский ремонт',
			OBJECT_CONDITIONS.cosmetic_repair_needed(): u'требуется косметический ремонт',
			OBJECT_CONDITIONS.unfinished_repair(): u'неоконченный ремонт',
			OBJECT_CONDITIONS.for_finishing(): u'под чистовую отделку',
		},
		'floor_types': {
			FLOOR_TYPES.mansard(): u'мансарда',
			FLOOR_TYPES.ground(): u'цоколь'
		},
	}


	market_type_sid = models.SmallIntegerField(default=MARKET_TYPES.secondary_market()) # Тип ринку
	building_type_sid = models.SmallIntegerField(default=TRADE_BUILDING_TYPES.entertainment())
	build_year = models.PositiveSmallIntegerField(null=True)
	condition_sid = models.SmallIntegerField(default=OBJECT_CONDITIONS.living()) # загальний стан

	floor = models.SmallIntegerField(null=True) # номер поверху
	floor_type_sid = models.SmallIntegerField(default=FLOOR_TYPES.floor()) # тип поверху: мансарда, цоколь, звичайний поверх і т.д
	floors_count = models.SmallIntegerField(null=True)
	mansard = models.BooleanField(default=False) # мансарда
	ground = models.BooleanField(default=False) # цокольний поверх
	lower_floor = models.BooleanField(default=False) # підвал

	halls_count = models.PositiveSmallIntegerField(null=True)
	halls_area = models.FloatField(null=True)
	total_area = models.FloatField(null=True)
	closed_area = models.BooleanField(default=False)

	vcs_count = models.PositiveSmallIntegerField(null=True)
	ceiling_height = models.FloatField(null=True) # висота стелі

	# Опалення
	heating_type_sid = models.SmallIntegerField(default=HEATING_TYPES.central())
	custom_heating_type = models.TextField(null=True) # якщо нічого не вказано в heating_type_sid
	# якщо вибрано ідивідуальний тип опалення в heating_type_sid
	ind_heating_type_sid = models.SmallIntegerField(default=INDIVIDUAL_HEATING_TYPES.gas())
	custom_ind_heating_type = models.TextField(null=True) # якщо нічого не вказано в ind_heating_type_sid

	# Інші зручності
	electricity = models.BooleanField(default=False)
	gas = models.BooleanField(default=False)
	sewerage = models.BooleanField(default=False)

	hot_water = models.BooleanField(default=False)
	cold_water = models.BooleanField(default=False)
	ventilation = models.BooleanField(default=False)

	security_alarm = models.BooleanField(default=False)
	fire_alarm = models.BooleanField(default=False)
	security = models.BooleanField(default=False)

	add_facilities = models.TextField(null=True) # дод. відомості про зручності

	# Комунікації
	phone = models.BooleanField(default=False)
	phone_lines_count = models.PositiveSmallIntegerField(null=True)
	internet = models.BooleanField(default=False)
	mobile_coverage = models.BooleanField(default=False) # покриття моб. операторами
	cable_tv = models.BooleanField(default=False) # кабельне / супутникове тб
	lan = models.BooleanField(default=False)

	# Дод. будівлі
	parking = models.BooleanField(default=False) # гараж / паркомісце
	open_air = models.BooleanField(default=False)
	add_buildings = models.TextField(null=True)

	# Поряд знаходиться
	transport_stop = models.BooleanField(default=False)
	market = models.BooleanField(default=False)
	cafe = models.BooleanField(default=False)
	bank = models.BooleanField(default=False)
	cash_machine = models.BooleanField(default=False)
	entertainment = models.BooleanField(default=False) # розважальні установи
	add_showplaces = models.TextField(null=True)


	# validation
	def check_extended_fields(self):
		if self.floor is None:
			raise EmptyFloor('Floor is None.')
		if self.halls_count is None:
			raise EmptyHallsCount('Halls count is None.')
		if self.halls_area is None:
			raise EmptyHallsArea('Halls area is None.')


	# output
	def print_title(self):
		if self.title is None:
			return u''
		return self.title


	def print_description(self):
		if self.description is None:
			return u''
		return self.description


	def print_market_type(self):
		return self.substitutions['market_type'][self.market_type_sid]


	def print_building_type(self):
		return self.substitutions['building_type'][self.building_type_sid]


	def print_condition(self):
		return self.substitutions['condition'][self.condition_sid]


	#-- output numeric fields
	def print_build_year(self):
		if self.build_year is None:
			return u''
		return unicode(self.build_year) + u' г.'


	def print_floor(self):
		# Поле "этаж" пропущено в floor_types умисно, щоб воно зайвий раз не потрапляло у видачу.
		floor_type = self.substitutions['floor_types'].get(self.floor_type_sid, u'')
		if floor_type:
			return floor_type
		return unicode(self.floor)


	def print_floors_count(self):
		if not self.floors_count:
			return u''

		floors = u''
		if self.ground:
			floors += u', цоколь'
		if self.lower_floor:
			floors += u', подвал'
		if self.mansard:
			floors += u', мансарда'

		if floors and self.floors_count:
			return unicode(self.floors_count) + u' (' + floors[2:] + u')'
		return unicode(self.floors_count)


	def print_halls_count(self):
		if self.halls_count is None:
			return u''
		return unicode(self.halls_count)


	def print_halls_area(self):
		if self.halls_area is None:
			return u''
		return "{:.2f}".format(self.halls_area).rstrip('0').rstrip('.') + u' м²'


	def print_total_area(self):
		if self.total_area is None:
			return u''

		total_area = "{:.2f}".format(self.total_area).rstrip('0').rstrip('.') + u' м²'
		if self.closed_area:
			total_area += u' (закрытая територия)'
		return total_area


	def print_vcs_count(self):
		if self.vcs_count is None:
			return u''
		return unicode(self.vcs_count)


	def print_ceiling_height(self):
		if self.ceiling_height is None:
			return u''
		return unicode(self.ceiling_height) + u' м'


	#-- output formatted strings
	def print_facilities(self):
		facilities = u''

		# Опалення (пункт "невідомо" не виводиться)
		if self.heating_type_sid == HEATING_TYPES.none():
			facilities += u'отопление отсутствует'
		elif self.heating_type_sid == HEATING_TYPES.central():
			facilities += u'центральное отопление'
		elif self.heating_type_sid == HEATING_TYPES.individual():
			facilities += u'индивидуальное отопление'
			if self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.electricity():
				facilities += u' (электричество)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.gas():
				facilities += u' (газ)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.firewood():
				facilities += u' (дрова)'
			elif self.ind_heating_type_sid == INDIVIDUAL_HEATING_TYPES.other():
				if self.custom_ind_heating_type is not None:
					facilities += u' ('+self.custom_ind_heating_type + u')'
		elif self.heating_type_sid == HEATING_TYPES.other():
			facilities += u'отопление: ' + self.custom_heating_type

		if self.electricity:
			facilities += u', электричество'
		if self.gas:
			facilities += u', газ'
		if self.sewerage:
			facilities += u', канализация'
		if self.hot_water:
			facilities += u', гарячая вода'
		if self.cold_water:
			facilities += u', холодная вода'
		if self.ventilation:
			facilities += u', вентиляция'

		if self.security_alarm and self.fire_alarm:
			facilities += u', охранная и пожарная сигнализации'
		else:
			if self.security_alarm:
				facilities += u', охранная сигнализация'
			if self.fire_alarm:
				facilities += u', пожарная сигнализация'

		if self.security:
			facilities += u', охрана'

		if self.add_facilities:
			facilities = facilities + '. ' + self.add_facilities

		if facilities[:2] == u', ':
			facilities = facilities[2:]
		return facilities if facilities else u''


	def print_add_facilities(self):
		if self.add_facilities is None:
			return u''
		return self.add_facilities


	def print_communications(self):
		communications = u''
		if self.phone:
			communications += u', телефон'
			if self.phone_lines_count:
				communications += u' (количество линий - ' + unicode(self.phone_lines_count) + u')'

		if self.internet:
			communications += u', интернет'
		if self.mobile_coverage:
			communications += u', покрытие мобильными операторами'
		if self.cable_tv:
			communications += u', кабельное телевидение'
		if self.lan:
			communications += u', локальная сеть'

		if communications:
			return communications[2:].capitalize() + u"."
		return u''


	def print_provided_add_buildings(self):
		buildings = u''
		if self.parking:
			buildings += u', парковка'
		if self.open_air:
			buildings += u', открытая площадка'

		if self.add_buildings:
			buildings += u'. ' + self.add_buildings

		if buildings:
			return buildings[2:]
		return buildings[2:] if buildings else u''


	def print_showplaces(self):
		showplaces = u''
		if self.transport_stop:
			showplaces += u', остановка общ. транспорта'
		if self.bank:
			showplaces += u', отделения банка'
		if self.cash_machine:
			showplaces += u', банкомат'
		if self.cafe:
			showplaces += u', кафе / ресторан'
		if self.market:
			showplaces += u', рынок / супермаркет'
		if self.entertainment:
			showplaces += u', развлекательные заведения'

		if self.add_showplaces:
			showplaces += '. ' + self.add_showplaces

		if showplaces:
			return showplaces[2:].capitalize() + u'.'
		return u''



class CateringsHeads(CommercialHeadModel):
	class Meta:
		db_table = 'o_caterings_heads'

	tid = OBJECTS_TYPES.catering()
	photos_model = CateringsPhotos

	body = models.ForeignKey(CateringsBodies)
	sale_terms = models.OneToOneField(CateringsSaleTerms)
	rent_terms = models.OneToOneField(CateringsRentTerms)


class GaragesSaleTerms(SaleTermsModel):
	class Meta:
		db_table = 'o_garages_sale_terms'


class GaragesRentTerms(CommercialRentTermsModel):
	class Meta:
		db_table = 'o_garages_rent_terms'


class GaragesPhotos(PhotosModel):
	class Meta:
		db_table = 'img_garages_photos'

	destination_dir_name = 'garages/'
	hid = models.ForeignKey('GaragesHeads', db_index=True)


class GaragesBodies(BodyModel):
	class Meta:
		db_table = 'o_garages_bodies'

	substitutions = {
		'market_type': {
			MARKET_TYPES.new_building(): u'новостройка',
			MARKET_TYPES.secondary_market(): u'вторичный рынок',
		},
	}


	market_type_sid = models.SmallIntegerField(default=MARKET_TYPES.secondary_market()) # Тип ринку
	area = models.FloatField(null=True)
	ceiling_height = models.FloatField(null=True) # висота стелі
	pit = models.BooleanField(default=False) # яма
	driveways_sid = models.SmallIntegerField(default=GARAGE_DRIVE_WAYS.asphalt())

	# Інші зручності
	electricity = models.BooleanField(default=False)
	gas = models.BooleanField(default=False)

	hot_water = models.BooleanField(default=False)
	cold_water = models.BooleanField(default=False)
	ventilation = models.BooleanField(default=False)

	security_alarm = models.BooleanField(default=False)
	fire_alarm = models.BooleanField(default=False)
	security = models.BooleanField(default=False)
	add_facilities = models.TextField(null=True) # дод. відомості про зручності


	# validation
	def check_extended_fields(self):
		if self.area is None:
			raise EmptyTotalArea('Total area is None.')


	# output
	def print_title(self):
		if not self.title:
			return u''
		return self.title


	def print_description(self):
		if not self.description:
			return u''
		return self.description


	def print_market_type(self):
		return self.substitutions['market_type'][self.market_type_sid]


	def print_area(self):
		if not self.area:
			return u''
		return "{:.2f}".format(self.area).rstrip('0').rstrip('.') + u' м²'


	def print_ceiling_height(self):
		if not self.ceiling_height:
			return u''
		return unicode(self.ceiling_height) + u' м'


	def print_driveways(self):
		driveways = u''
		if self.driveways_sid == GARAGE_DRIVE_WAYS.asphalt():
			driveways = u'асфальт'+ u'.'
		elif self.driveways_sid == GARAGE_DRIVE_WAYS.ground():
			driveways = u'грунт'+ u'.'
		return driveways


	def print_facilities(self):
		facilities = u''

		if self.electricity:
			facilities += u', электричество'
		if self.gas:
			facilities += u', газ'
		if self.hot_water:
			facilities += u', гарячая вода'
		if self.cold_water:
			facilities += u', холодная вода'
		if self.ventilation:
			facilities += u', вентиляция'

		if self.security_alarm and self.fire_alarm:
			facilities += u', охранная и пожарная сигнализации'
		else:
			if self.security_alarm:
				facilities += u', охранная сигнализация'
			if self.fire_alarm:
				facilities += u', пожарная сигнализация'

		if self.security:
			facilities += u', охрана'

		if self.add_facilities:
			facilities += u'.' + self.add_facilities

		if facilities[:2] == u', ':
			facilities = facilities[2:]
		return(facilities.capitalize() + u'.') if facilities else u''



class GaragesHeads(LivingHeadModel):
	class Meta:
		db_table = 'o_garages_heads'

	tid = OBJECTS_TYPES.garage()
	photos_model = GaragesPhotos

	body = models.ForeignKey(GaragesBodies)
	sale_terms = models.OneToOneField(GaragesSaleTerms)
	rent_terms = models.OneToOneField(GaragesRentTerms)


class LandsSaleTerms(SaleTermsModel):
	class Meta:
		db_table = 'o_lands_sale_terms'


class LandsRentTerms(CommercialRentTermsModel):
	class Meta:
		db_table = 'o_lands_rent_terms'


class LandsPhotos(PhotosModel):
	class Meta:
		db_table = 'img_lands_photos'

	destination_dir_name = 'lands/'
	hid = models.ForeignKey('LandsHeads', db_index=True)


class LandsBodies(BodyModel):
	class Meta:
		db_table = 'o_lands_bodies'

	destination_sid = models.SmallIntegerField(null=True)
	area = models.FloatField(null=True)
	closed_area = models.BooleanField(default=False)
	driveways_sid = models.SmallIntegerField(default=LAND_DRIVEWAYS.asphalt())

	# Інші зручності
	electricity = models.BooleanField(default=False)
	gas = models.BooleanField(default=False)
	water = models.BooleanField(default=False)
	sewerage = models.BooleanField(default=False)
	add_facilities = models.TextField(null=True) # дод. відомості про зручності

	# Додаткові побудови
	well = models.BooleanField(default=False)
	add_buildings = models.TextField(null=True)

	# Поряд знаходяться
	transport_stop = models.BooleanField(default=False)
	market = models.BooleanField(default=False)
	cafe = models.BooleanField(default=False)
	bank = models.BooleanField(default=False)
	cash_machine = models.BooleanField(default=False)
	entertainment = models.BooleanField(default=False) # розважальні установи
	add_showplaces = models.TextField(null=True)


	# validation
	def check_extended_fields(self):
		if self.area is None:
			raise EmptyTotalArea('Total area is None.')


	# output
	def print_title(self):
		if not self.title:
			return u''
		return self.title


	def print_description(self):
		if self.description is None:
			return u''
		return self.description


	def print_area(self):
		if self.area is None:
			return u''
		return "{:.2f}".format(self.area).rstrip('0').rstrip('.') + u' м²'


	def print_driveways(self):
		driveways = u''
		if self.driveways_sid == LAND_DRIVEWAYS.asphalt():
			driveways = u'асфальт'+ u'.'
		elif self.driveways_sid == LAND_DRIVEWAYS.ground():
			driveways = u'грунт'+ u'.'
		return driveways


	def print_facilities(self):
		facilities = u''

		if self.electricity:
			facilities += u', электричество'
		if self.gas:
			facilities += u', газ'
		if self.water:
			facilities += u', вода'
		if self.canalisation:
			facilities += u', канализация'

		if facilities[:2] == u', ':
			facilities = facilities[2:]
		return(facilities.capitalize() + u'.') if facilities else u''
	
	
	def print_provided_add_buildings(self):
		buildings = u''
		if self.well:
			buildings += u'колодец / скважина'

		if self.add_buildings:
			buildings += '. ' + self.add_buildings

		return buildings.capitalize() + u'.' if buildings else u''


	def print_showplaces(self):
		showplaces = u''
		if self.transport_stop:
			showplaces += u', остановка общ. транспорта'
		if self.bank:
			showplaces += u', отделения банка'
		if self.cash_machine:
			showplaces += u', банкомат'
		if self.cafe:
			showplaces += u', кафе / ресторан'
		if self.market:
			showplaces += u', рынок / супермаркет'
		if self.entertainment:
			showplaces += u', развлекательные заведения'

		if self.add_showplaces:
			showplaces += u'.' + self.add_showplaces

		if showplaces:
			return showplaces[2:].capitalize() + u'.'
		return u''


class LandsHeads(LivingHeadModel):
	class Meta:
		db_table = 'o_lands_heads'

	tid = OBJECTS_TYPES.land()
	photos_model = LandsPhotos

	body = models.ForeignKey(LandsBodies)
	sale_terms = models.OneToOneField(LandsSaleTerms)
	rent_terms = models.OneToOneField(LandsRentTerms)