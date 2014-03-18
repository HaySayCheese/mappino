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
	hid = models.ForeignKey('FlatsHeads')


class FlatsSaleTerms(SaleTermsModel):
	class Meta:
		db_table = 'o_flats_sale_terms'


class FlatsRentTerms(LivingRentTermsModel):
	class Meta:
		db_table = 'o_flats_rent_terms'


class FlatsBodies(BodyModel):
	class Meta:
		db_table = 'o_flats_bodies'

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

	def check_extended_fields(self):
		if self.floor is None:
			raise EmptyFloor('Floor is None.')
		if self.total_area is None:
			raise EmptyTotalArea('Total area is None.')
		if self.living_area is None:
			raise EmptyLivingArea('Living area is None.')
		if self.rooms_count is None:
			raise EmptyRoomsCount('Rooms count is None.')


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
	hid = models.ForeignKey('ApartmentsHeads')


class ApartmentsSaleTerms(SaleTermsModel):
	class Meta:
		db_table = 'o_apartments_sale_terms'


class ApartmentsRentTerms(LivingRentTermsModel):
	class Meta:
		db_table = 'o_apartments_rent_terms'


class ApartmentsBodies(BodyModel):
	class Meta:
		db_table = 'o_apartments_bodies'

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


	def check_extended_fields(self):
		if self.floor is None:
			raise EmptyFloor('Floor is None.')
		if self.total_area is None:
			raise EmptyTotalArea('Total area is None.')
		if self.living_area is None:
			raise EmptyLivingArea('Living area is None.')
		if self.rooms_count is None:
			raise EmptyRoomsCount('Rooms count is None.')



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
	hid = models.ForeignKey('HousesHeads')


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


	def check_extended_fields(self):
		if self.total_area is None:
			raise EmptyTotalArea('Total area is None.')
		if self.living_area is None:
			raise EmptyLivingArea('Living area is None.')
		if self.floors_count is None:
			raise EmptyFloorsCount('Floors count is None.')
		if self.rooms_count is None:
			raise EmptyRoomsCount('Rooms count is None.')



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
	hid = models.ForeignKey('DachasHeads')


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
	hid = models.ForeignKey('CottagesHeads')


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

	def check_extended_fields(self):
		if self.total_area is None:
			raise EmptyTotalArea('Total area is None.')
		if self.living_area is None:
			raise EmptyLivingArea('Living area is None.')
		if self.floors_count is None:
			raise EmptyFloorsCount('Floors count is None.')
		if self.rooms_count is None:
			raise EmptyRoomsCount('Rooms count is None.')



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
	hid = models.ForeignKey('RoomsHeads')


class RoomsSaleTerms(SaleTermsModel):
	class Meta:
		db_table = 'o_rooms_sale_terms'


class RoomsRentTerms(LivingRentTermsModel):
	class Meta:
		db_table = 'o_rooms_rent_terms'


class RoomsBodies(BodyModel):
	class Meta:
		db_table = 'o_rooms_bodies'

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

	def check_extended_fields(self):
		if self.floor is None:
			raise EmptyFloor('Floor count is None.')
		if self.rooms_count is None:
			raise EmptyRoomsCount('Rooms count is None.')
		if self.total_area is None:
			raise EmptyTotalArea('Total area is None.')
		if self.living_area is None:
			raise EmptyLivingArea('Living area is None.')



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
	hid = models.ForeignKey('TradesHeads')


class TradesBodies(BodyModel):
	class Meta:
		db_table = 'o_trades_bodies'

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
	canalisation = models.BooleanField(default=False)

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


	def check_extended_fields(self):
		if self.floor is None:
			raise EmptyFloor('Floor is None.')
		if self.halls_count is None:
			raise EmptyHallsCount('Halls count is None.')
		if self.halls_area is None:
			raise EmptyHallsArea('Halls area is None.')



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
	hid = models.ForeignKey('OfficesHeads')


class OfficesBodies(BodyModel):
	class Meta:
		db_table = 'o_offices_bodies'

	market_type_sid = models.SmallIntegerField(default=MARKET_TYPES.secondary_market()) # Тип ринку
	building_type_sid = models.SmallIntegerField(default=TRADE_BUILDING_TYPES.entertainment())
	build_year = models.PositiveSmallIntegerField(null=True)
	condition_sid = models.SmallIntegerField(default=OBJECT_CONDITIONS.living()) # загальний стан

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


	def check_extended_fields(self):
		if self.floor is None:
			raise EmptyFloor('Floor is None.')
		if self.cabinets_count is None:
			raise EmptyCabinetsCount('Cabinets count is None.')



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
	hid = models.ForeignKey('WarehousesHeads')


class WarehousesBodies(BodyModel):
	class Meta:
		db_table = 'o_warehouses_bodies'

	market_type_sid = models.SmallIntegerField(default=MARKET_TYPES.secondary_market()) # Тип ринку
	area = models.FloatField(null=True)
	plot_area = models.FloatField(null=True) # площа участку
	open_space = models.FloatField(null=True) # вільне плаування
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
	canalisation = models.BooleanField(default=False)

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
	entertainment = models.BooleanField(default=False) # розважальні установи
	refueling = models.BooleanField(default=False) # автозапрака
	railway_station = models.BooleanField(default=False)
	add_showplaces = models.TextField(null=True)


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
	hid = models.ForeignKey('BusinessesHeads')


class BusinessesBodies(BodyModel):
	class Meta:
		db_table = 'o_business_bodies'

	age = models.FloatField(null=True)
	workers_count = models.PositiveIntegerField(null=True)
	monthly_costs = models.DecimalField(
		null=True,
		max_digits=AbstractModel.max_price_symbols_count,
		decimal_places=2)
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
	canalisation = models.BooleanField(default=False)

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


	def check_extended_fields(self):
		if self.floor is None:
			raise EmptyFloor('Floor is None.')
		if self.total_area is None:
			raise EmptyTotalArea('Total area count is None.')



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
	hid = models.ForeignKey('CateringsHeads')


class CateringsBodies(BodyModel):
	class Meta:
		db_table = 'o_caterings_bodies'

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
	canalisation = models.BooleanField(default=False)

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


	def check_extended_fields(self):
		if self.floor is None:
			raise EmptyFloor('Floor is None.')
		if self.halls_count is None:
			raise EmptyHallsCount('Halls count is None.')
		if self.halls_area is None:
			raise EmptyHallsArea('Halls area is None.')



class CateringsHeads(CommercialHeadModel):
	class Meta:
		db_table = 'o_caterings_heads'

	tid = OBJECTS_TYPES.catering()
	photos_model = CateringsPhotos

	body = models.ForeignKey(CateringsBodies)
	sale_terms = models.OneToOneField(CateringsSaleTerms)
	rent_terms = models.OneToOneField(CateringsRentTerms)


class GaragesSaleTerms(CommercialRentTermsModel):
	class Meta:
		db_table = 'o_garages_sale_terms'


class GaragesRentTerms(CommercialRentTermsModel):
	class Meta:
		db_table = 'o_garages_rent_terms'


class GaragesPhotos(PhotosModel):
	class Meta:
		db_table = 'img_garages_photos'

	destination_dir_name = 'garages/'
	hid = models.ForeignKey('GaragesHeads')


class GaragesBodies(BodyModel):
	class Meta:
		db_table = 'o_garages_bodies'

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


	def check_extended_fields(self):
		if self.area is None:
			raise EmptyTotalArea('Total area is None.')



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
	hid = models.ForeignKey('LandsHeads')


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
	canalisation = models.BooleanField(default=False)
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


	def check_extended_fields(self):
		if self.area is None:
			raise EmptyTotalArea('Total area is None.')



class LandsHeads(LivingHeadModel):
	class Meta:
		db_table = 'o_lands_heads'

	tid = OBJECTS_TYPES.land()
	photos_model = LandsPhotos

	body = models.ForeignKey(LandsBodies)
	sale_terms = models.OneToOneField(LandsSaleTerms)
	rent_terms = models.OneToOneField(LandsRentTerms)