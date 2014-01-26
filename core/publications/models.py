#coding=utf-8
from django.db import models
from core.publications.abstract_models import LivingHeadModel, BodyModel, LivingRentTermsModel, CommercialRentTermsModel, PhotosModel, SaleTermsModel, CommercialHeadModel, AbstractModel
from core.publications.constants import MARKET_TYPES, OBJECT_CONDITIONS, FLOOR_TYPES, HEATING_TYPES, INDIVIDUAL_HEATING_TYPES, CURRENCIES
from core.publications.objects_constants.apartments import APARTMENTS_BUILDINGS_TYPES, APARTMENTS_FLAT_TYPES, APARTMENTS_ROOMS_PLANING_TYPES
from core.publications.objects_constants.cottages import COTTAGE_RENT_TYPES, COTTAGE_SALE_TYPES
from core.publications.objects_constants.dachas import DACHA_WC_LOCATIONS
from core.publications.objects_constants.flats import FLAT_BUILDING_TYPES, FLAT_TYPES, FLAT_ROOMS_PLANNINGS
from core.publications.objects_constants.garages import GARAGE_DRIVE_WAYS
from core.publications.objects_constants.houses import HOUSE_RENT_TYPES, HOUSE_SALE_TYPES
from core.publications.objects_constants.lands import LAND_DRIVEWAYS
from core.publications.objects_constants.rooms import ROOMS_BUILDINGS_TYPES, ROOMS_ROOMS_PLANING_TYPES, ROOMS_WC_LOCATION
from core.publications.objects_constants.trades import TRADE_BUILDING_TYPES


class FlatsPhotos(PhotosModel):
	class Meta:
		db_table = 'img_flats_photos'

	destination_destination_dir_name = 'flats/photos/'
	head = models.ForeignKey('FlatsHeads')


class FlatsSaleTerms(SaleTermsModel):
	class Meta:
		db_table = 'o_flats_sale_terms'


class FlatsRentTerms(LivingRentTermsModel):
	class Meta:
		db_table = 'o_flats_rent_terms'

	furniture = models.BooleanField(default=False) # меблі
	refrigerator = models.BooleanField(default=False)
	tv = models.BooleanField(default=False)
	washing_machine = models.BooleanField(default=False)
	conditioner = models.BooleanField(default=False)
	home_theater = models.BooleanField(default=False)
	other = models.TextField(default='') # todo: використати це поле


class FlatsBodies(BodyModel):
	class Meta:
		db_table = 'o_flats_bodies'

	market_type_sid = models.SmallIntegerField(default=MARKET_TYPES.secondary_market()) # Тип ринку

	building_type_sid = models.SmallIntegerField(default=FLAT_BUILDING_TYPES.brick())
	custom_building_type = models.TextField(null=True)
	build_year = models.PositiveSmallIntegerField(null=True)
	flat_type_sid = models.SmallIntegerField(default=FLAT_TYPES.separate()) # тип квартири
	custom_flat_type = models.TextField(null=True)
	rooms_planing_sid = models.SmallIntegerField(default=FLAT_ROOMS_PLANNINGS.separate()) # планування кімнат
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


class FlatsHeads(LivingHeadModel):
	class Meta:
		db_table = 'o_flats_heads'

	body_model = FlatsBodies
	sale_terms_model = FlatsSaleTerms
	rent_terms_model = FlatsRentTerms
	photos_model = FlatsPhotos


class ApartmentsPhotos(PhotosModel):
	class Meta:
		db_table = 'img_apartments_photos'

	destination_destination_dir_name = 'apartments/photos/'
	head = models.ForeignKey('ApartmentsHeads')


class ApartmentsSaleTerms(SaleTermsModel):
	class Meta:
		db_table = 'o_apartments_sale_terms'


class ApartmentsRentTerms(LivingRentTermsModel):
	class Meta:
		db_table = 'o_apartments_rent_terms'

	furniture = models.BooleanField(default=False)
	refrigerator = models.BooleanField(default=False)
	tv = models.BooleanField(default=False)
	washing_machine = models.BooleanField(default=False)
	conditioner = models.BooleanField(default=False)
	home_theater = models.BooleanField(default=False)


class ApartmentsBodies(BodyModel):
	class Meta:
		db_table = 'o_apartments_bodies'

	market_type_sid = models.SmallIntegerField(default=MARKET_TYPES.secondary_market()) # Тип ринку

	building_type_sid = models.SmallIntegerField(default=APARTMENTS_BUILDINGS_TYPES.brick())
	custom_building_type = models.TextField(null=True)
	build_year = models.PositiveSmallIntegerField(null=True)
	flat_type_sid = models.SmallIntegerField(default=APARTMENTS_FLAT_TYPES.separate()) # тип квартири
	custom_flat_type = models.TextField(null=True)
	rooms_planing_sid = models.SmallIntegerField(default=APARTMENTS_ROOMS_PLANING_TYPES.separate()) # планування кімнат
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
	water = models.BooleanField(default=False) # річка, озеро, водойма
	wood = models.BooleanField(default=False)
	sea = models.BooleanField(default=False)
	add_showplaces = models.TextField(null=True)


class ApartmentsHeads(LivingHeadModel):
	class Meta:
		db_table = 'o_apartments_heads'

	body_model = ApartmentsBodies
	sale_terms_model = ApartmentsSaleTerms
	rent_terms_model = ApartmentsRentTerms
	photos_model = ApartmentsPhotos


class HousesPhotos(PhotosModel):
	class Meta:
		db_table = 'img_houses_photos'

	destination_destination_dir_name = 'houses/photos/'
	head = models.ForeignKey('HousesHeads')


class HousesSaleTerms(SaleTermsModel):
	class Meta:
		db_table = 'o_houses_sale_terms'


class HousesRentTerms(LivingRentTermsModel):
	class Meta:
		db_table = 'o_houses_rent_terms'

	rent_type_sid = models.SmallIntegerField(default=HOUSE_RENT_TYPES.all_house())

	furniture = models.BooleanField(default=False)
	refrigerator = models.BooleanField(default=False)
	tv = models.BooleanField(default=False)
	washing_machine = models.BooleanField(default=False)
	conditioner = models.BooleanField(default=False)
	home_theater = models.BooleanField(default=False)


class HousesBodies(BodyModel):
	class Meta:
		db_table = 'o_houses_bodies'

	sale_type_sid = models.SmallIntegerField(default=HOUSE_SALE_TYPES.all_house())
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
	water = models.BooleanField(default=False) # річка, озеро, водойма
	wood = models.BooleanField(default=False)
	sea = models.BooleanField(default=False)
	add_showplaces = models.TextField(null=True)


class HousesHeads(LivingHeadModel):
	class Meta:
		db_table = 'o_houses_heads'

	body_model = HousesBodies
	sale_terms_model = HousesSaleTerms
	rent_terms_model = HousesRentTerms
	photos_model = HousesPhotos


class DachasPhotos(PhotosModel):
	class Meta:
		db_table = 'img_dachas_photos'

	destination_destination_dir_name = 'dachas/photos/'
	head = models.ForeignKey('DachasHeads')


class DachasSaleTerms(SaleTermsModel):
	class Meta:
		db_table = 'o_dachas_sale_terms'


class DachasRentTerms(LivingRentTermsModel):
	class Meta:
		db_table = 'o_dachas_rent_terms'

	furniture = models.BooleanField(default=False) # меблі
	refrigerator = models.BooleanField(default=False)
	tv = models.BooleanField(default=False)
	washing_machine = models.BooleanField(default=False)
	conditioner = models.BooleanField(default=False)
	home_theater = models.BooleanField(default=False)


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
	vcs_count = models.SmallIntegerField(null=True)


	# vc
	vc_sid = models.BooleanField(null=True, default=None)
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
	water = models.BooleanField(default=False) # річка, озеро, водойма
	wood = models.BooleanField(default=False)
	sea = models.BooleanField(default=False)
	add_showplaces = models.TextField(null=True)


class DachasHeads(LivingHeadModel):
	class Meta:
		db_table = 'o_dachas_heads'

	body_model = DachasBodies
	sale_terms_model = SaleTermsModel
	rent_terms_model = DachasRentTerms
	photos_model = DachasPhotos


class CottagesPhotos(PhotosModel):
	class Meta:
		db_table = 'img_cottages_photos'

	destination_destination_dir_name = 'cottages/photos/'
	head = models.ForeignKey('CottagesHeads')


class CottagesSaleTerms(SaleTermsModel):
	class Meta:
		db_table = 'o_cottages_sale_terms'


class CottagesRentTerms(LivingRentTermsModel):
	class Meta:
		db_table = 'o_cottages_rent_terms'

	rent_type_sid = models.SmallIntegerField(default=COTTAGE_RENT_TYPES.all_house())

	furniture = models.BooleanField(default=False) # меблі
	refrigerator = models.BooleanField(default=False)
	tv = models.BooleanField(default=False)
	washing_machine = models.BooleanField(default=False)
	conditioner = models.BooleanField(default=False)
	home_theater = models.BooleanField(default=False)


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
	water = models.BooleanField(default=False) # річка, озеро, водойма
	wood = models.BooleanField(default=False)
	sea = models.BooleanField(default=False)
	add_showplaces = models.TextField(null=True)


class CottagesHeads(LivingHeadModel):
	class Meta:
		db_table = 'o_cottages_heads'

	body_model = CottagesBodies
	sale_terms_model = CottagesSaleTerms
	rent_terms_model = CottagesRentTerms
	photos_model = CottagesPhotos


class RoomsPhotos(PhotosModel):
	class Meta:
		db_table = 'img_rooms_photos'

	destination_dir_name = 'rooms/photos/'
	head = models.ForeignKey('RoomsHeads')


class RoomsSaleTerms(SaleTermsModel):
	class Meta:
		db_table = 'o_rooms_sale_terms'


class RoomsRentTerms(LivingRentTermsModel):
	class Meta:
		db_table = 'o_rooms_rent_terms'

	furniture = models.BooleanField(default=False) # меблі
	refrigerator = models.BooleanField(default=False)
	tv = models.BooleanField(default=False)
	washing_machine = models.BooleanField(default=False)
	conditioner = models.BooleanField(default=False)
	home_theater = models.BooleanField(default=False)


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
	rooms_planing_sid = models.SmallIntegerField(default=ROOMS_ROOMS_PLANING_TYPES.separate()) # планування кімнат
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
	water = models.BooleanField(default=False) # річка, озеро, водойма
	wood = models.BooleanField(default=False)
	sea = models.BooleanField(default=False)
	add_showplaces = models.TextField(null=True)


class RoomsHeads(LivingHeadModel):
	class Meta:
		db_table = 'o_rooms_heads'

	body_model = RoomsBodies
	sale_terms_model = RoomsSaleTerms
	rent_terms_model = RoomsRentTerms
	photos_model = RoomsPhotos


class TradesSaleTerms(SaleTermsModel):
	class Meta:
		db_table = 'o_trades_sale_terms'


class TradesRentTerms(CommercialRentTermsModel):
	class Meta:
		db_table = 'o_trades_rent_terms'


class TradesPhotos(PhotosModel):
	class Meta:
		db_table = 'img_trades_photos'

	destination_dir_name = 'trades/photos/'
	head = models.ForeignKey('TradesHeads')


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


class TradesHeads(CommercialHeadModel):
	class Meta:
		db_table = 'o_trades_heads'

	body_model = TradesBodies
	sale_sale_terms = TradesSaleTerms
	rent_sale_terms = TradesRentTerms
	photos_model = TradesPhotos


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

	destination_dir_name = 'offices/photos/'
	head = models.ForeignKey('OfficesHeads')


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


class OfficesHeads(CommercialHeadModel):
	class Meta:
		db_table = 'o_offices_heads'

	body_model = OfficesBodies
	sale_terms_model = OfficesSaleTerms
	rent_terms_model = OfficesRentTerms
	photos_model = OfficesPhotos


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

	destination_dir_name = 'warehouses/photos/'
	head = models.ForeignKey('WarehousesHeads')


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

	body_models = WarehousesBodies
	sale_terms_model = WarehousesSaleTerms
	rent_terms_model = WarehousesRentTerms
	photos_model = WarehousesPhotos


class BusinessesSaleTerms(SaleTermsModel):
	class Meta:
		db_table = 'o_business_sale_terms'


class BusinessesRentTerms(CommercialRentTermsModel):
	class Meta:
		db_table = 'o_business_rent_terms'


class BusinessesPhotos(PhotosModel):
	class Meta:
		db_table = 'img_business_photos'

	destination_dir_name = 'businesses/photos/'
	head = models.ForeignKey('BusinessesHeads')


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



class BusinessesHeads(CommercialHeadModel):
	class Meta:
		db_table = 'o_business_heads'

	body_model = BusinessesBodies
	sale_terms_model = BusinessesSaleTerms
	rent_terms_model = BusinessesRentTerms
	photos_model = BusinessesPhotos


class CateringsSaleTerms(SaleTermsModel):
	class Meta:
		db_table = 'o_caterings_sale_terms'


class CateringsRentTerms(CommercialRentTermsModel):
	class Meta:
		db_table = 'o_caterings_rent_terms'


class CateringsPhotos(PhotosModel):
	class Meta:
		db_table = 'img_caterings_photos'

	destination_dir_name = 'caterings/photos/'
	head = models.ForeignKey('CateringsHeads')


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


class CateringsHeads(CommercialHeadModel):
	class Meta:
		db_table = 'o_caterings_heads'

	body_model = CateringsBodies
	sale_terms_model = CateringsSaleTerms
	rent_terms_model = CateringsRentTerms
	photos_model = CateringsPhotos


class GaragesSaleTerms(CommercialRentTermsModel):
	class Meta:
		db_table = 'o_garages_sale_terms'


class GaragesRentTerms(CommercialRentTermsModel):
	class Meta:
		db_table = 'o_garages_rent_terms'


class GaragesPhotos(PhotosModel):
	class Meta:
		db_table = 'img_garages_photos'

	destination_dir_name = 'garages/photos/'
	head = models.ForeignKey('GaragesHeads')


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


class GaragesHeads(LivingHeadModel):
	class Meta:
		db_table = 'o_garages_heads'

	body_model = GaragesBodies
	sale_terms_model = GaragesSaleTerms
	rent_terms_model = GaragesRentTerms
	photos_model = GaragesPhotos


class LandsSaleTerms(SaleTermsModel):
	class Meta:
		db_table = 'o_lands_sale_terms'


class LandsRentTerms(CommercialRentTermsModel):
	class Meta:
		db_table = 'o_lands_rent_terms'


class LandsPhotos(PhotosModel):
	class Meta:
		db_table = 'img_lands_photos'

	destination_dir_name = 'lands/photos/'
	head = models.ForeignKey('LandsHeads')


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


class LandsHeads(LivingHeadModel):
	class Meta:
		db_table = 'o_lands_heads'

	body_model = LandsBodies
	sale_terms_model = LandsSaleTerms
	rent_terms_model = LandsRentTerms
	photos_model = LandsPhotos