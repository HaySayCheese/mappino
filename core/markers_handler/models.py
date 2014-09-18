#coding=utf-8
from django.db import models, connections
from django.db.models import Q
from djorm_pgarray.fields import BigIntegerArrayField
from collective.exceptions import InvalidArgument

from core.currencies.constants import CURRENCIES

from core.markers_handler.classes import Grid
from core.markers_handler.exceptions import TooBigTransaction
from core.publications.constants import OBJECTS_TYPES, MARKET_TYPES, FLOOR_TYPES, HEATING_TYPES, LIVING_RENT_PERIODS
from core.currencies.currencies_manager import convert as convert_price
from core.publications.objects_constants.flats import FLAT_ROOMS_PLANNINGS
from core.publications.objects_constants.trades import TRADE_BUILDING_TYPES


class AbstractBaseIndex(models.Model):
	"""
	В даному модулі індекс це — таблиця, яка містить всі необхідні поля для того,
	щоб забезпечити роботу фільтрів, передбачених логікою фронтенда.

	Абсолютна більшість полів даної таблиці індексуються B-Tree індексом (в django за замовчуванням).
	Перенасичення таблиці індексами в даному випадку не розглядається як проблема, оскільки
	    * передбачається, що всі похідні таблиці (тобто всі індеки для кожного з типів)
	      будуть обслуговуватись окремим сервером PostgreSQL в якому буде вимкнено ACID,
	      за рахунок чого, вставка в дані таблиці повинна відбуватись досить швидко.

	      Дані в індексі дублюватимуть дані з основних таблиць, тому втрата навіть всього індексу
	      не веде до проблем, оскільки індекс в будь-який момент може бути перебудований
	      ціної декількох годин процесрного часу.

	    * неможливо з необхідним рівнем достовірності спрогноувати які саме фільтри
	      буде використовувати середньо-статистинчий користувач. Як наслідок — для забепечення ефективної
		  роботи фільтрів за таких умов слід індексувати кожне поле, по якому може йти вибірка.
		  Проактивна оптимізація з метою побудови такої системи, яка швидше працює лише за певного,
		  наперед визначеного спектру запитів веде до необгрунтованого ускладення алгоритмів системи в цілому
		  і тому в даній задачі не розглядаєаться як потенційне рішення.
	"""

	# publication_id умисно не помічено за первинний ключ.
	# Для індекса не критично якщо час-від-часу в ньому виникатимуть дублі записів.
	# Більш критичним є неможливість користувача опублікувати оголошення через потенційно можливий конфлікт
	# із уже існуючим записом в ндексі.
	#
	# Така ситуація достатньо вірогідна через те, що довелось змішати чистий sql з django-orm,
	# через що порушився механізм транзакцій (зараз транзакцій як таких немає).
	publication_id = models.PositiveIntegerField()
	hash_id = models.TextField()

	# lat, lng дублюються в індексі щоб уникнути зайвого join-а з таблицею даних по оголошеннях.
	# Аналогічним чином дублюються всі дані, які, так чи інакше, формують видачу по фільтрах,
	# в тому числі в дочірніх індексах.
	lat = models.FloatField()
	lng = models.FloatField()

	class Meta:
		abstract = True


	@classmethod
	def remove(cls, record, using=None):
		cls.objects.using(using).filter(publication_id = record.id).delete()


	@classmethod
	def min_queryset(cls): # virtual
		return cls.objects.none()


	@classmethod
	def min_add_queryset(cls): # virtual
		return cls.objects.none()


	@classmethod
	def min_remove_queryset(cls):
		return cls.objects.all().only(
			'degree_lat',
		    'degree_lng',
		    'segment_lat',
		    'segment_lng',
		    'pos_lat',
		    'pos_lng',
		)


	@staticmethod
	def convert_and_format_price(price, base_currency, destination_currency):
		"""
		Поверне рядок з ціною price сконвертованою з валюти base_currency у валюту destination_currency.
		Якщо валюти base_currency та destination_currency відмінні — перед результатом буде додано "≈",
		як індикатор того, що ціна в отриманій валюті приблизна.
		"""
		converted_price = convert_price(price, base_currency, destination_currency)
		converted_price = int(converted_price) # копійок в кінці ціни нам не потрібно
		result = u'{0}'.format(converted_price).replace(',',' ') # форматування на наш лад

		if base_currency != destination_currency:
			return u'≈' + result
		return result


	@staticmethod
	def currency_to_str(currency):
		if currency == CURRENCIES.dol():
			return u'дол.'
		elif currency == CURRENCIES.uah():
			return u'грн.'
		elif currency == CURRENCIES.eur():
			return u'евро'
		else:
			raise InvalidArgument('Invalid currency.')


	@staticmethod
	def currency_from_filters(filters):
		# Гривня як базова валюта обирається згідно з чинним законодавством,
		# але якщо у фільтрі вказана інша валюта - переформатувати бриф на неї.
		if filters is None:
			return CURRENCIES.uah()

		return filters.get('currency_sid', CURRENCIES.uah())


	#-- filters methods

	@staticmethod # range
	def apply_price_filter(filters, markers):
		currency = filters.get('currency_sid')
		if (currency is None) or (currency not in CURRENCIES.values()):
			raise InvalidArgument('filters does not contains or contains invalid currency_sid.')


		price_min = filters.get('price_from')
		if price_min:
			markers = markers.filter(
				Q(
					Q(
						price__gte = convert_price(price_min, currency, CURRENCIES.dol()),
						currency_sid = CURRENCIES.dol()
					) | Q(
						price__gte = convert_price(price_min, currency, CURRENCIES.eur()),
						currency_sid = CURRENCIES.eur()
					) | Q (
						price__gte = convert_price(price_min, currency, CURRENCIES.uah()),
						currency_sid = CURRENCIES.uah()
					)
				)
			)

		price_max = filters.get('price_to')
		if price_max:
			markers = markers.filter(
				Q(
					Q(
						price__lte = convert_price(price_max, currency, CURRENCIES.dol()),
						currency_sid = CURRENCIES.dol()
					) | Q(
						price__lte = convert_price(price_max, currency, CURRENCIES.eur()),
						currency_sid = CURRENCIES.eur()
					) | Q (
						price__lte = convert_price(price_max, currency, CURRENCIES.uah()),
						currency_sid = CURRENCIES.uah()
					)
				)
			)

		return markers


	@staticmethod # range
	def apply_total_area_filter(filters, markers):
		ta_min = filters.get('total_area_from')
		if ta_min is not None:
			markers = markers.filter(total_area__gte = ta_min)

		ta_max = filters.get('total_area_to')
		if ta_max is not None:
			markers = markers.filter(total_area__lte = ta_max)

		return markers


	@staticmethod # range
	def apply_halls_area_filter(filters, markers):
		ha_min = filters.get('halls_area_from')
		if ha_min is not None:
			markers = markers.filter(halls_area__gte = ha_min)

		ha_max = filters.get('halls_area_to')
		if ha_max is not None:
			markers = markers.filter(halls_area__lte = ha_max)

		return markers


	@staticmethod # range
	def apply_floor_filter(filters, markers):
		floor_min = filters.get('floor_from')
		if floor_min is not None:
			markers = markers.filter(floor__gte = floor_min)

		floor_max = filters.get('floor_to')
		if floor_max is not None:
			markers = markers.filter(floor_lte = floor_max)

		if 'mansard' in filters and not 'ground' in filters:
			markers = markers.exclude(floor_type_sid = FLOOR_TYPES.mansard())

		if 'ground' in filters and not 'mansard' in filters:
			markers = markers.exclude(floor_type_sid = FLOOR_TYPES.ground())

		return markers


	@staticmethod # range
	def apply_floors_count_filter(filters, markers):
		floor_min = filters.get('floors_count_from')
		if floor_min is not None:
			markers = markers.filter(floors_count__gte = floor_min)

		floor_max = filters.get('floors_count_to')
		if floor_max is not None:
			markers = markers.filter(floors_count__lte = floor_max)

		return markers


	@staticmethod # range
	def apply_ceiling_height_filter(filters, markers):
		height_min = filters.get('ceiling_height_from')
		if height_min is not None:
			markers = markers.filter(ceiling_height__gte = height_min)

		height_max = filters.get('ceiling_height_to')
		if height_max is not None:
			markers = markers.filter(ceiling_height__lte = height_max)

		return markers


	@staticmethod # range
	def apply_rooms_count_filter(filters, markers):
		rooms_count_min = filters.get('rooms_count_from')
		if rooms_count_min is not None:
			markers = markers.filter(rooms_count__gte = rooms_count_min)

		rooms_count_max = filters.get('rooms_count_to')
		if rooms_count_max is not None:
			markers = markers.filter(rooms_count__lte = rooms_count_max)

		return markers


	@staticmethod # range
	def apply_persons_count_filter(filters, markers):
		count_min = filters.get('persons_count_from')
		if count_min is not None:
			markers = markers.filter(persons_count__gte = count_min)

		count_max = filters.get('persons_count_to')
		if count_max is not None:
			markers = markers.filter(persons_count__lte = count_max)

		return markers


	@staticmethod # range
	def apply_cabinets_count_filter(filters, markers):
		count_min = filters.get('cabinets_count_from')
		if count_min is not None:
			markers = markers.filter(cabinets_count__gte = count_min)

		count_max = filters.get('cabinets_count_to')
		if count_max is not None:
			markers = markers.filter(cabinets_count__gte = count_max)

		return markers


	@staticmethod # sid
	def apply_living_rent_period_filter(filters, markers):
		period = filters.get('rent_period_sid')
		if period == 1:
			markers = markers.filter(period_sid = LIVING_RENT_PERIODS.daily())

		elif period == 2:
			markers = markers.filter(period_sid = LIVING_RENT_PERIODS.monthly())

		return markers


	@staticmethod # sid
	def apply_market_type_filter(filters, markers):
		if 'new_buildings' in filters and not 'secondary_market' in filters:
			markers = markers.filter(market_type_sid = MARKET_TYPES.new_building())

		elif 'secondary_market' in filters and not 'new_buildings' in filters:
			markers = markers.filter(market_type_sid = MARKET_TYPES.secondary_market())

		return markers


	@staticmethod # sid
	def apply_rooms_planning_filter(filters, markers):
		rooms_planning_sid = filters.get('rooms_planning_sid')
		if rooms_planning_sid == 1:
			markers = markers.filter(rooms_planning_sid = FLAT_ROOMS_PLANNINGS.free())
		elif rooms_planning_sid == 2:
			markers = markers.exclude(rooms_planning_sid = FLAT_ROOMS_PLANNINGS.free())

		return markers


	@staticmethod
	def apply_trade_building_type_filter(filters, markers):
		building_type = filters.get('building_type_sid')
		if building_type == 1:
			markers = markers.filter(building_type_sid = TRADE_BUILDING_TYPES.entertainment())
		elif building_type == 2:
			markers = markers.filter(building_type_sid = TRADE_BUILDING_TYPES.business())
		elif building_type == 3:
			markers = markers.filter(building_type_sid = TRADE_BUILDING_TYPES.separate())

		return markers


	@staticmethod # sid
	def apply_heating_type_filter(filters, markers):
		heating = filters.get('heating_type_sid')
		if heating == 1:
			markers = markers.filter(heating_type_sid = HEATING_TYPES.central())
		elif heating == 2:
			markers = markers.filter(heating_type_sid = HEATING_TYPES.individual())
		elif heating == 3:
			markers = markers.filter(heating_type_sid = HEATING_TYPES.none())

		return markers


	@staticmethod # bool
	def apply_electricity_filter(filters, markers):
		if 'electricity' in filters:
			return markers.filter(electricity = True)
		return markers


	@staticmethod # bool
	def apply_gas_filter(filters, markers):
		if 'gas' in filters:
			return markers.filter(gas = True)
		return markers


	@staticmethod # bool
	def apply_hot_water_filter(filters, markers):
		if 'hot_water' in filters:
			return markers.filter(hot_water = True)
		return markers


	@staticmethod # bool
	def apply_cold_water_filter(filters, markers):
		if 'cold_water' in filters:
			return markers.filter(cold_water = True)
		return markers


	@staticmethod # bool
	def apply_water_filter(filters, markers):
		if 'water' in filters:
			return markers.filter(water = True)
		return markers


	@staticmethod # bool
	def apply_sewerage_filter(filters, markers):
		if 'sewerage' in filters:
			return markers.filter(sewerage = True)
		return markers


	@staticmethod # bool
	def apply_lift_filter(filters, markers):
		if 'lift' in filters:
			return markers.filter(lift = True)
		return markers


	@staticmethod # bool
	def apply_family_filter(filters, markers):
		if 'family' in filters:
			return markers.filter(family = True)
		return markers


	@staticmethod # bool
	def apply_foreigners_filter(filters, markers):
		if 'foreigners' in filters:
			return markers.filter(foreigners = True)
		return markers


	@staticmethod # bool
	def apply_security_filter(filters, markers):
		if 'security' in filters:
			return markers.filter(security = True)
		return markers


	@staticmethod # bool
	def apply_kitchen_filter(filters, markers):
		if 'kitchen' in filters:
			return markers.filter(kitchen = True)
		return markers


	@staticmethod # bool
	def apply_fire_alarm_filter(filters, markers):
		if 'fire_alarm' in filters:
			return markers.filter(fire_alarm = True)
		return markers


	@staticmethod # bool
	def apply_security_alarm_filter(filters, markers):
		if 'security_alarm' in filters:
			return markers.filter(security_alarm = True)
		return markers


	@staticmethod # bool
	def apply_pit_filter(filters, markers):
		if 'pit' in filters:
			return markers.filter(pit = True)
		return markers


class FlatsSaleIndexAbstract(AbstractBaseIndex):
	market_type_sid = models.PositiveSmallIntegerField(db_index=True)
	price = models.FloatField(db_index=True)
	currency_sid = models.PositiveSmallIntegerField()
	rooms_count = models.PositiveSmallIntegerField(db_index=True)
	rooms_planning_sid = models.PositiveSmallIntegerField(db_index=True)
	total_area = models.FloatField(db_index=True)
	floor = models.PositiveSmallIntegerField(db_index=True)
	floor_type_sid = models.PositiveSmallIntegerField(db_index=True)
	lift = models.BooleanField(db_index=True)
	hot_water = models.BooleanField(db_index=True)
	cold_water = models.BooleanField(db_index=True)
	gas = models.BooleanField(db_index=True)
	electricity = models.BooleanField(db_index=True)
	heating_type_sid = models.PositiveSmallIntegerField(db_index=True)

	class Meta:
		db_table = 'index_flats_sale'


	@classmethod
	def add(cls, record, using=None):
		cls.objects.using(using).create(
			publication_id = record.id,
		    hash_id = record.hash_id,
		    lat = float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
		    lng = float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

		    market_type_sid = record.body.market_type_sid,
		    price = record.sale_terms.price,
		    currency_sid = record.sale_terms.currency_sid,
		    rooms_count = record.body.rooms_count,
		    rooms_planning_sid = record.body.rooms_planning_sid,
		    total_area = record.body.total_area,
			floor = record.body.floor,
			floor_type_sid = record.body.floor_type_sid,
			lift = record.body.lift,
			hot_water = record.body.hot_water,
			cold_water = record.body.cold_water,
			gas = record.body.gas,
			electricity = record.body.electricity,
			heating_type_sid = record.body.heating_type_sid,
		)


	@classmethod
	def min_queryset(cls):
		return cls.objects.all().only(
			'hash_id', 'lat', 'lng', 'price', 'currency_sid', 'rooms_count') # todo: fixme


	@classmethod
	def min_add_queryset(cls):
		return cls.objects.all().only(
			'degree_lat',
			'degree_lng',
			'segment_lat',
			'segment_lng',
			'pos_lat',
			'pos_lng',

		    'id',
		    'hash_id',

			'body__market_type_sid',
			'body__rooms_count',
			'body__rooms_planning_sid',
			'body__total_area',
			'body__floor',
			'body__floor_type_sid',
			'body__lift',
			'body__how_water',
			'body__cold_water',
			'body__gas',
			'body__electricity',
			'body__heating_type_sid',

			'sale_terms__price',
			'sale_terms__currency_sid'
		)


	@classmethod
	def apply_filters(cls, filters, markers):
		markers = cls.apply_price_filter(filters, markers)
		markers = cls.apply_market_type_filter(filters, markers)
		markers = cls.apply_rooms_count_filter(filters, markers)
		markers = cls.apply_rooms_planning_filter(filters, markers)
		markers = cls.apply_total_area_filter(filters, markers)
		markers = cls.apply_floor_filter(filters, markers)
		markers = cls.apply_electricity_filter(filters, markers)
		markers = cls.apply_gas_filter(filters, markers)
		markers = cls.apply_hot_water_filter(filters, markers)
		markers = cls.apply_cold_water_filter(filters, markers)
		markers = cls.apply_lift_filter(filters, markers)
		markers = cls.apply_heating_type_filter(filters, markers)
		return markers


	@classmethod
	def brief(cls, marker, filters=None):
		currency = cls.currency_from_filters(filters)
		price = cls.convert_and_format_price(marker.price, marker.currency_sid, currency)

		return {
			'id': marker.hash_id,
		    'd0': u'Комнат: {0}'.format(marker.rooms_count) if marker.rooms_count else 'Комнат: не указано',
			'd1': u'{0} {1}'.format(price, cls.currency_to_str(currency)),
		}


class FlatsRentIndexAbstract(AbstractBaseIndex):
	period_sid = models.PositiveSmallIntegerField(db_index=True)
	price = models.FloatField(db_index=True)
	currency_sid = models.PositiveSmallIntegerField()
	persons_count = models.PositiveSmallIntegerField(db_index=True)
	family = models.BooleanField(db_index=True)
	foreigners = models.BooleanField(db_index=True)

	total_area = models.FloatField(db_index=True)
	floor = models.PositiveSmallIntegerField(db_index=True)
	floor_type_sid = models.PositiveSmallIntegerField(db_index=True)
	lift = models.BooleanField(db_index=True)
	hot_water = models.BooleanField(db_index=True)
	cold_water = models.BooleanField(db_index=True)
	gas = models.BooleanField(db_index=True)
	electricity = models.BooleanField(db_index=True)

	class Meta:
		db_table = 'index_flats_rent'


	@classmethod
	def add(cls, record, using=None):
		cls.objects.using(using).create(
			publication_id = record.id,
		    hash_id = record.hash_id,
		    lat = float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
		    lng = float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

			period_sid = record.rent_terms.period_sid,
		    price = record.rent_terms.price,
		    currency_sid = record.rent_terms.currency_sid,
		    persons_count = record.rent_terms.persons_count,
		    family = record.rent_terms.family,
		    foreigners = record.rent_terms.foreigners,

		    total_area = record.body.total_area,
			floor = record.body.floor,
			floor_type_sid = record.body.floor_type_sid,
			lift = record.body.lift,
			hot_water = record.body.hot_water,
			cold_water = record.body.cold_water,
			gas = record.body.gas,
			electricity = record.body.electricity,
		)


	@classmethod
	def min_queryset(cls):
		return cls.objects.all().only(
			'hash_id', 'lat', 'lng', 'price', 'currency_sid', 'rooms_count') # todo: fixme


	@classmethod
	def min_add_queryset(cls):
		return cls.objects.all().only(
			'degree_lat',
			'degree_lng',
			'segment_lat',
			'segment_lng',
			'pos_lat',
			'pos_lng',

		    'id',
		    'hash_id',

			'body__total_area',
			'body__floor',
			'body__floor_type_sid',
			'body__lift',
			'body__how_water',
			'body__cold_water',
			'body__gas',
			'body__electricity',

			'rent_terms__price',
			'rent_terms__currency_sid'
			'rent_terms__period_sid'
			'rent_terms__persons_count'
			'rent_terms__family'
			'rent_terms__foreigners'
		)


	@classmethod
	def apply_filters(cls, filters, markers):
		markers = cls.apply_price_filter(filters, markers)
		markers = cls.apply_living_rent_period_filter(filters, markers)
		markers = cls.apply_persons_count_filter(filters, markers)
		markers = cls.apply_total_area_filter(filters, markers)
		markers = cls.apply_floor_filter(filters, markers)
		markers = cls.apply_family_filter(filters, markers)
		markers = cls.apply_foreigners_filter(filters, markers)
		markers = cls.apply_electricity_filter(filters, markers)
		markers = cls.apply_gas_filter(filters, markers)
		markers = cls.apply_hot_water_filter(filters, markers)
		markers = cls.apply_cold_water_filter(filters, markers)
		markers = cls.apply_lift_filter(filters, markers)
		return markers


	@classmethod
	def brief(cls, marker, filters=None):
		currency = cls.currency_from_filters(filters)
		price = cls.convert_and_format_price(marker.price, marker.currency_sid, currency)

		return {
			'id': marker.hash_id,
		    'd0': u'Мест: {0}'.format(marker.persons_count) if marker.persons_count else 'Мест: не указано',
			'd1': u'{0} {1}'.format(price, cls.currency_to_str(currency)),
		}


class HousesSaleIndexAbstract(AbstractBaseIndex):
	market_type_sid = models.PositiveSmallIntegerField(db_index=True)
	price = models.FloatField(db_index=True)
	currency_sid = models.PositiveSmallIntegerField()
	total_area = models.FloatField(db_index=True)
	rooms_count = models.PositiveSmallIntegerField(db_index=True)
	floors_count = models.PositiveSmallIntegerField(db_index=True)
	hot_water = models.BooleanField(db_index=True)
	cold_water = models.BooleanField(db_index=True)
	gas = models.BooleanField(db_index=True)
	electricity = models.BooleanField(db_index=True)
	sewerage = models.BooleanField(db_index=True)
	heating_type_sid = models.PositiveSmallIntegerField(db_index=True)

	class Meta:
		db_table = 'index_houses_sale'


	@classmethod
	def add(cls, record, using=None):
		cls.objects.using(using).create(
			publication_id = record.id,
		    hash_id = record.hash_id,
		    lat = float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
		    lng = float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

		    market_type_sid = record.body.market_type_sid,
		    price = record.sale_terms.price,
		    currency_sid = record.sale_terms.currency_sid,
		    total_area = record.body.total_area,
		    rooms_count = record.body.rooms_count,
		    floors_count = record.body.floors_count,
			hot_water = record.body.hot_water,
			cold_water = record.body.cold_water,
			gas = record.body.gas,
			electricity = record.body.electricity,
			sewerage = record.body.sewerage,
			heating_type_sid = record.body.heating_type_sid,
		)


	@classmethod
	def min_queryset(cls):
		return cls.objects.all().only(
			'hash_id', 'lat', 'lng', 'price', 'currency_sid', 'total_area')


	@classmethod
	def min_add_queryset(cls):
		return cls.objects.all().only(
			'degree_lat',
			'degree_lng',
			'segment_lat',
			'segment_lng',
			'pos_lat',
			'pos_lng',

		    'id',
		    'hash_id',

			'body__market_type_sid',
		    'body__total_area',
			'body__rooms_count',
			'body__floors_count',
			'body__how_water',
			'body__cold_water',
			'body__electricity',
		    'body__gas',
		    'body__sewerage',
			'body__heating_type_sid',

			'sale_terms__price',
			'sale_terms__currency_sid'
		)


	@classmethod
	def apply_filters(cls, filters, markers):
		markers = cls.apply_price_filter(filters, markers)
		markers = cls.apply_market_type_filter(filters, markers)
		markers = cls.apply_total_area_filter(filters, markers)
		markers = cls.apply_rooms_count_filter(filters, markers)
		markers = cls.apply_floors_count_filter(filters, markers)
		markers = cls.apply_electricity_filter(filters, markers)
		markers = cls.apply_gas_filter(filters, markers)
		markers = cls.apply_hot_water_filter(filters, markers)
		markers = cls.apply_cold_water_filter(filters, markers)
		markers = cls.apply_sewerage_filter(filters, markers)
		markers = cls.apply_heating_type_filter(filters, markers)
		return markers


	@classmethod
	def brief(cls, marker, filters=None):
		currency = cls.currency_from_filters(filters)
		price = cls.convert_and_format_price(marker.price, marker.currency_sid, currency)
		total_area = '{0}'.format(marker.total_area).rstrip('0').rstrip('.')

		return {
			'id': marker.hash_id,
		    'd0': u'{0} м²'.format(total_area),
			'd1': u'{0} {1}'.format(price, cls.currency_to_str(currency)),
		}


class HousesRentIndexAbstract(AbstractBaseIndex):
	period_sid = models.PositiveSmallIntegerField(db_index=True)
	price = models.FloatField(db_index=True)
	currency_sid = models.PositiveSmallIntegerField()
	persons_count = models.PositiveSmallIntegerField(db_index=True)
	total_area = models.FloatField(db_index=True)
	family = models.BooleanField(db_index=True)
	foreigners = models.BooleanField(db_index=True)
	lift = models.BooleanField(db_index=True)
	hot_water = models.BooleanField(db_index=True)
	cold_water = models.BooleanField(db_index=True)
	gas = models.BooleanField(db_index=True)
	electricity = models.BooleanField(db_index=True)

	class Meta:
		db_table = 'index_houses_rent'


	@classmethod
	def add(cls, record, using=None):
		cls.objects.using(using).create(
			publication_id = record.id,
		    hash_id = record.hash_id,
		    lat = float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
		    lng = float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

		    period_sid = record.rent_terms.period_sid,
		    price = record.rent_terms.price,
		    currency_sid = record.rent_terms.currency_sid,
		    persons_count = record.rent_terms.persons_count,
		    family = record.rent_terms.family,
		    foreigners = record.rent_terms.foreigners,

		    total_area = record.body.total_area,
			hot_water = record.body.hot_water,
			cold_water = record.body.cold_water,
			gas = record.body.gas,
			electricity = record.body.electricity,
		)


	@classmethod
	def min_queryset(cls):
		return cls.objects.all().only(
			'hash_id', 'lat', 'lng', 'price', 'currency_sid', 'persons_count')


	@classmethod
	def min_add_queryset(cls):
		return cls.objects.all().only(
			'degree_lat',
			'degree_lng',
			'segment_lat',
			'segment_lng',
			'pos_lat',
			'pos_lng',

		    'id',
		    'hash_id',

			'body__total_area',
			'body__how_water',
			'body__cold_water',
			'body__gas',
			'body__electricity',

			'rent_terms__period_sid'
			'rent_terms__price',
			'rent_terms__currency_sid'
			'rent_terms__persons_count'
			'rent_terms__family'
			'rent_terms__foreigners'
		)


	@classmethod
	def apply_filters(cls, filters, markers):
		markers = cls.apply_price_filter(filters, markers)
		markers = cls.apply_living_rent_period_filter(filters, markers)
		markers = cls.apply_persons_count_filter(filters, markers)
		markers = cls.apply_total_area_filter(filters, markers)
		markers = cls.apply_family_filter(filters, markers)
		markers = cls.apply_foreigners_filter(filters, markers)
		markers = cls.apply_electricity_filter(filters, markers)
		markers = cls.apply_gas_filter(filters, markers)
		markers = cls.apply_hot_water_filter(filters, markers)
		markers = cls.apply_cold_water_filter(filters, markers)
		return markers


	@classmethod
	def brief(cls, marker, filters=None):
		currency = cls.currency_from_filters(filters)
		price = cls.convert_and_format_price(marker.price, marker.currency_sid, currency)

		return {
			'id': marker.hash_id,
		    'd0': u'Мест {0}'.format(marker.persons_count),
			'd1': u'{0} {1}'.format(price, cls.currency_to_str(currency)),
		}


class RoomsSaleIndexAbstract(AbstractBaseIndex):
	price = models.FloatField(db_index=True)
	currency_sid = models.PositiveSmallIntegerField()
	market_type_sid = models.PositiveSmallIntegerField(db_index=True)
	rooms_count = models.PositiveSmallIntegerField(db_index=True)
	total_area = models.FloatField(db_index=True)
	floor = models.PositiveSmallIntegerField(db_index=True)
	floor_type_sid = models.PositiveSmallIntegerField(db_index=True)
	lift = models.BooleanField(db_index=True)
	hot_water = models.BooleanField(db_index=True)
	cold_water = models.BooleanField(db_index=True)
	gas = models.BooleanField(db_index=True)
	electricity = models.BooleanField(db_index=True)
	heating_type_sid = models.PositiveSmallIntegerField(db_index=True)

	class Meta:
		db_table = 'index_rooms_sale'


	@classmethod
	def add(cls, record, using=None):
		cls.objects.using(using).create(
			publication_id = record.id,
		    hash_id = record.hash_id,
		    lat = float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
		    lng = float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

		    market_type_sid = record.body.market_type_sid,
		    rooms_count = record.body.rooms_count,
		    total_area = record.body.total_area,
			floor = record.body.floor,
			floor_type_sid = record.body.floor_type_sid,
			lift = record.body.lift,
			hot_water = record.body.hot_water,
			cold_water = record.body.cold_water,
			electricity = record.body.electricity,
		    gas = record.body.gas,
			heating_type_sid = record.body.heating_type_sid,

		    price = record.sale_terms.price,
		    currency_sid = record.sale_terms.currency_sid,
		)


	@classmethod
	def min_queryset(cls):
		return cls.objects.all().only(
			'hash_id', 'lat', 'lng', 'price', 'currency_sid', 'total_area')


	@classmethod
	def min_add_queryset(cls):
		return cls.objects.all().only(
			'degree_lat',
			'degree_lng',
			'segment_lat',
			'segment_lng',
			'pos_lat',
			'pos_lng',

		    'id',
		    'hash_id',

			'body__market_type_sid',
		    'body__rooms_count',
			'body__total_area',
			'body__floor',
			'body__floor_type_sid',
			'body__lift'
			'body__hot_water',
			'body__cold_water',
			'body__electricity',
		    'body__gas',
			'body__heating_type_sid',

			'sale_terms__price',
			'sale_terms__currency_sid'
		)


	@classmethod
	def apply_filters(cls, filters, markers):
		markers = cls.apply_price_filter(filters, markers)
		markers = cls.apply_market_type_filter(filters, markers)
		markers = cls.apply_rooms_count_filter(filters, markers)
		markers = cls.apply_total_area_filter(filters, markers)
		markers = cls.apply_floor_filter(filters, markers)
		markers = cls.apply_electricity_filter(filters, markers)
		markers = cls.apply_gas_filter(filters, markers)
		markers = cls.apply_hot_water_filter(filters, markers)
		markers = cls.apply_cold_water_filter(filters, markers)
		markers = cls.apply_lift_filter(filters, markers)
		markers = cls.apply_heating_type_filter(filters, markers)
		return markers


	@classmethod
	def brief(cls, marker, filters=None):
		currency = cls.currency_from_filters(filters)
		price = cls.convert_and_format_price(marker.price, marker.currency_sid, currency)
		total_area = '{0:.2f}'.format(marker.total_area).rstrip('0').rstrip('.')

		return {
			'id': marker.hash_id,
		    'd0': u'Площадь: {0} м²'.format(total_area),
			'd1': u'{0} {1}'.format(price, cls.currency_to_str(currency)),
		}


class RoomsRentIndex(AbstractBaseIndex):
	period_sid = models.PositiveSmallIntegerField(db_index=True)
	price = models.FloatField(db_index=True)
	currency_sid = models.PositiveSmallIntegerField()
	persons_count = models.PositiveSmallIntegerField(db_index=True)
	total_area = models.FloatField(db_index=True)
	floor = models.PositiveSmallIntegerField(db_index=True)
	floor_type_sid = models.PositiveSmallIntegerField(db_index=True)
	family = models.BooleanField(db_index=True)
	foreigners = models.BooleanField(db_index=True)
	lift = models.BooleanField(db_index=True)
	hot_water = models.BooleanField(db_index=True)
	cold_water = models.BooleanField(db_index=True)
	gas = models.BooleanField(db_index=True)
	electricity = models.BooleanField(db_index=True)

	class Meta:
		db_table = 'index_rooms_rent'


	@classmethod
	def add(cls, record, using=None):
		cls.objects.using(using).create(
			publication_id = record.id,
		    hash_id = record.hash_id,
		    lat = float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
		    lng = float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

			period_sid = record.rent_terms.period_sid,
		    price = record.rent_terms.price,
		    currency_sid = record.rent_terms.currency_sid,
		    persons_count = record.rent_terms.persons_count,
		    family = record.rent_terms.family,
		    foreigners = record.rent_terms.foreigners,

		    total_area = record.body.total_area,
			floor = record.body.floor,
			floor_type_sid = record.body.floor_type_sid,
			lift = record.body.lift,
			hot_water = record.body.hot_water,
			cold_water = record.body.cold_water,
			gas = record.body.gas,
			electricity = record.body.electricity,
		)


	@classmethod
	def min_queryset(cls):
		return cls.objects.all().only(
			'hash_id', 'lat', 'lng', 'price', 'currency_sid', 'persons_count')


	@classmethod
	def min_add_queryset(cls):
		return cls.objects.all().only(
			'degree_lat',
			'degree_lng',
			'segment_lat',
			'segment_lng',
			'pos_lat',
			'pos_lng',

		    'id',
		    'hash_id',

			'body__total_area',
		    'body__floor',
		    'body__floor_type_sid',
		    'body__lift',
			'body__how_water',
			'body__cold_water',
			'body__gas',
			'body__electricity',

			'rent_terms__period_sid'
			'rent_terms__price',
			'rent_terms__currency_sid'
			'rent_terms__persons_count'
			'rent_terms__family'
			'rent_terms__foreigners'
		)


	@classmethod
	def apply_filters(cls, filters, markers):
		markers = cls.apply_living_rent_period_filter(filters, markers)
		markers = cls.apply_price_filter(filters, markers)
		markers = cls.apply_persons_count_filter(filters, markers)
		markers = cls.apply_total_area_filter(filters, markers)
		markers = cls.apply_floor_filter(filters, markers)
		markers = cls.apply_family_filter(filters, markers)
		markers = cls.apply_foreigners_filter(filters, markers)
		markers = cls.apply_electricity_filter(filters, markers)
		markers = cls.apply_gas_filter(filters, markers)
		markers = cls.apply_hot_water_filter(filters, markers)
		markers = cls.apply_cold_water_filter(filters, markers)
		markers = cls.apply_lift_filter(filters, markers)
		return markers


	@classmethod
	def brief(cls, marker, filters=None):
		currency = cls.currency_from_filters(filters)
		price = cls.convert_and_format_price(marker.price, marker.currency_sid, currency)

		return {
			'id': marker.hash_id,
		    'd0': u'Мест: {0}'.format(marker.persons_count) if marker.persons_count else 'Мест: не указано',
			'd1': u'{0} {1}'.format(price, cls.currency_to_str(currency)),
		}


#-- commercial real estate

class TradesIndex(AbstractBaseIndex):
	price = models.FloatField(db_index=True)
	currency_sid = models.PositiveSmallIntegerField()
	market_type_sid = models.PositiveSmallIntegerField(db_index=True)
	halls_area = models.FloatField(db_index=True)
	total_area = models.FloatField(db_index=True)
	building_type_sid = models.PositiveSmallIntegerField(db_index=True)
	hot_water = models.BooleanField(db_index=True)
	cold_water = models.BooleanField(db_index=True)
	gas = models.BooleanField(db_index=True)
	electricity = models.BooleanField(db_index=True)
	sewerage = models.BooleanField(db_index=True)

	class Meta:
		db_table = 'index_trades'


	@classmethod
	def add(cls, record, using=None):
		cls.objects.using(using).create(
			publication_id = record.id,
		    hash_id = record.hash_id,
		    lat = float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
		    lng = float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

		    market_type_sid = record.body.market_type_sid,
		    halls_area = record.body.total_area,
		    total_area = record.body.total_area,
		    building_type_sid = record.body.building_type_sid,
			hot_water = record.body.hot_water,
			cold_water = record.body.cold_water,
			gas = record.body.gas,
			electricity = record.body.electricity,
			sewerage = record.body.sewerage,

		    price = record.sale_terms.price,
		    currency_sid = record.sale_terms.currency_sid,
		)


	@classmethod
	def min_queryset(cls):
		return cls.objects.all().only(
			'hash_id', 'lat', 'lng', 'price', 'currency_sid', 'total_area')


	@classmethod
	def min_add_queryset(cls):
		return cls.objects.all().only(
			'degree_lat',
			'degree_lng',
			'segment_lat',
			'segment_lng',
			'pos_lat',
			'pos_lng',

		    'id',
		    'hash_id',

			'body__market_type_sid',
		    'body__halls_area',
		    'body__total_area',
			'body__building_type_sid',
			'body__hot_water',
			'body__cold_water',
			'body__electricity',
		    'body__gas',
		    'body__sewerage',

			'sale_terms__price',
			'sale_terms__currency_sid'
		)


	@classmethod
	def apply_filters(cls, filters, markers):
		markers = cls.apply_market_type_filter(filters, markers)
		markers = cls.apply_price_filter(filters, markers)
		markers = cls.apply_halls_area_filter(filters, markers)
		markers = cls.apply_total_area_filter(filters, markers)
		markers = cls.apply_trade_building_type_filter(filters, markers)
		markers = cls.apply_electricity_filter(filters, markers)
		markers = cls.apply_gas_filter(filters, markers)
		markers = cls.apply_hot_water_filter(filters, markers)
		markers = cls.apply_cold_water_filter(filters, markers)
		markers = cls.apply_sewerage_filter(filters, markers)
		return markers


	@classmethod
	def brief(cls, marker, filters=None):
		currency = cls.currency_from_filters(filters)
		price = cls.convert_and_format_price(marker.price, marker.currency_sid, currency)
		total_area = '{0}'.format(marker.total_area).rstrip('0').rstrip('.')

		return {
			'id': marker.hash_id,
		    'd0': u'{0} м²'.format(total_area),
			'd1': u'{0} {1}'.format(price, cls.currency_to_str(currency)),
		}


class OfficesIndex(AbstractBaseIndex):
	price = models.FloatField(db_index=True)
	currency_sid = models.PositiveSmallIntegerField()
	market_type_sid = models.PositiveSmallIntegerField(db_index=True)
	total_area = models.FloatField(db_index=True)
	cabinets_count = models.PositiveSmallIntegerField(db_index=True)
	hot_water = models.BooleanField(db_index=True)
	cold_water = models.BooleanField(db_index=True)
	security = models.BooleanField(db_index=True)
	kitchen = models.BooleanField(db_index=True)

	class Meta:
		db_table = 'index_offices'


	@classmethod
	def add(cls, record, using=None):
		cls.objects.using(using).create(
			publication_id = record.id,
		    hash_id = record.hash_id,
		    lat = float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
		    lng = float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

		    market_type_sid = record.body.market_type_sid,
		    total_area = record.body.total_area,
		    cabinets_count = record.body.cabinets_count,
			hot_water = record.body.hot_water,
			cold_water = record.body.cold_water,
			security = record.body.security,
		    kitchen = record.body.kitchen,

		    price = record.sale_terms.price,
		    currency_sid = record.sale_terms.currency_sid,
		)


	@classmethod
	def min_queryset(cls):
		return cls.objects.all().only(
			'hash_id', 'lat', 'lng', 'price', 'currency_sid', 'total_area')


	@classmethod
	def min_add_queryset(cls):
		return cls.objects.all().only(
			'degree_lat',
			'degree_lng',
			'segment_lat',
			'segment_lng',
			'pos_lat',
			'pos_lng',

		    'id',
		    'hash_id',

			'body__market_type_sid',
		    'body__total_area',
			'body__cabinets_count',
			'body__hot_water',
			'body__cold_water',
			'body__security',
		    'body__kitchen',

			'sale_terms__price',
			'sale_terms__currency_sid'
		)


	@classmethod
	def apply_filters(cls, filters, markers):
		markers = cls.apply_market_type_filter(filters, markers)
		markers = cls.apply_price_filter(filters, markers)
		markers = cls.apply_total_area_filter(filters, markers)
		markers = cls.apply_cabinets_count_filter(filters, markers)
		markers = cls.apply_hot_water_filter(filters, markers)
		markers = cls.apply_cold_water_filter(filters, markers)
		markers = cls.apply_kitchen_filter(filters, markers)
		markers = cls.apply_security_filter(filters, markers)
		return markers


	@classmethod
	def brief(cls, marker, filters=None):
		currency = cls.currency_from_filters(filters)
		price = cls.convert_and_format_price(marker.price, marker.currency_sid, currency)
		total_area = '{0}'.format(marker.total_area).rstrip('0').rstrip('.')

		return {
			'id': marker.hash_id,
		    'd0': u'{0} м²'.format(total_area),
			'd1': u'{0} {1}'.format(price, cls.currency_to_str(currency)),
		}


class WarehousesIndex(AbstractBaseIndex):
	price = models.FloatField(db_index=True)
	currency_sid = models.PositiveSmallIntegerField()
	market_type_sid = models.PositiveSmallIntegerField(db_index=True)
	halls_area =  models.FloatField(db_index=True)
	hot_water = models.BooleanField(db_index=True)
	cold_water = models.BooleanField(db_index=True)
	electricity = models.BooleanField(db_index=True)
	gas = models.BooleanField(db_index=True)
	security_alarm = models.BooleanField(db_index=True)
	fire_alarm = models.BooleanField(db_index=True)

	class Meta:
		db_table = 'index_warehouses'


	@classmethod
	def add(cls, record, using=None):
		cls.objects.using(using).create(
			publication_id = record.id,
		    hash_id = record.hash_id,
		    lat = float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
		    lng = float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

		    market_type_sid = record.body.market_type_sid,
		    halls_area = record.body.halls_area,
			hot_water = record.body.hot_water,
			cold_water = record.body.cold_water,
			electricity = record.body.electricity,
		    gas = record.body.gas,
		    fire_alarm = record.body.fire_alarm,
		    security_alarm = record.body.security_alarm,

		    price = record.sale_terms.price,
		    currency_sid = record.sale_terms.currency_sid,
		)


	@classmethod
	def min_queryset(cls):
		return cls.objects.all().only(
			'hash_id', 'lat', 'lng', 'price', 'currency_sid', 'halls_area') # todo: fixme


	@classmethod
	def min_add_queryset(cls):
		return cls.objects.all().only(
			'degree_lat',
			'degree_lng',
			'segment_lat',
			'segment_lng',
			'pos_lat',
			'pos_lng',

		    'id',
		    'hash_id',

			'body__market_type_sid',
		    'body__halls_area',
			'body__hot_water',
			'body__cold_water',
			'body__electricity',
		    'body__gas',
		    'body__fire_alarm',
		    'body__security_alarm',

			'sale_terms__price',
			'sale_terms__currency_sid'
		)


	@classmethod
	def apply_filters(cls, filters, markers):
		markers = cls.apply_market_type_filter(filters, markers)
		markers = cls.apply_price_filter(filters, markers)
		markers = cls.apply_halls_area_filter(filters, markers)
		markers = cls.apply_hot_water_filter(filters, markers)
		markers = cls.apply_cold_water_filter(filters, markers)
		markers = cls.apply_electricity_filter(filters, markers)
		markers = cls.apply_gas_filter(filters, markers)
		markers = cls.apply_fire_alarm_filter(filters, markers)
		markers = cls.apply_security_alarm_filter(filters, markers)
		return markers


	@classmethod
	def brief(cls, marker, filters=None):
		currency = cls.currency_from_filters(filters)
		price = cls.convert_and_format_price(marker.price, marker.currency_sid, currency)
		halls_area = '{0}'.format(marker.halls_area).rstrip('0').rstrip('.')

		return {
			'id': marker.hash_id,
		    'd0': u'{0} м²'.format(halls_area),
			'd1': u'{0} {1}'.format(price, cls.currency_to_str(currency)),
		}


class BusinessesIndex(AbstractBaseIndex):
	price = models.FloatField(db_index=True)
	currency_sid = models.PositiveSmallIntegerField()

	class Meta:
		db_table = 'index_businesses'


	@classmethod
	def add(cls, record, using=None):
		cls.objects.using(using).create(
			publication_id = record.id,
		    hash_id = record.hash_id,
		    lat = float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
		    lng = float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

			price = record.sale_terms.price,
		    currency_sid = record.sale_terms.currency_sid,
		)


	@classmethod
	def min_queryset(cls):
		return cls.objects.all().only(
			'hash_id', 'lat', 'lng', 'price', 'currency_sid')


	@classmethod
	def min_add_queryset(cls):
		return cls.objects.all().only(
			'degree_lat',
			'degree_lng',
			'segment_lat',
			'segment_lng',
			'pos_lat',
			'pos_lng',

		    'id',
		    'hash_id',

			'sale_terms__price',
			'sale_terms__currency_sid'
		)


	@classmethod
	def apply_filters(cls, filters, markers):
		markers = cls.apply_price_filter(filters, markers)
		return markers


	@classmethod
	def brief(cls, marker, filters=None):
		currency = cls.currency_from_filters(filters)
		price = cls.convert_and_format_price(marker.price, marker.currency_sid, currency)

		return {
			'id': marker.hash_id,
		    'd0': u'',
			'd1': u'{0} {1}'.format(price, cls.currency_to_str(currency)),
		}


class CateringsIndex(AbstractBaseIndex):
	price = models.FloatField(db_index=True)
	currency_sid = models.PositiveSmallIntegerField()
	market_type_sid = models.PositiveSmallIntegerField(db_index=True)
	halls_area = models.FloatField(db_index=True)
	total_area = models.FloatField(db_index=True)
	building_type_sid = models.PositiveSmallIntegerField(db_index=True)
	hot_water = models.BooleanField(db_index=True)
	cold_water = models.BooleanField(db_index=True)
	gas = models.BooleanField(db_index=True)
	electricity = models.BooleanField(db_index=True)
	sewerage = models.BooleanField(db_index=True)

	class Meta:
		db_table = 'index_caterings'


	@classmethod
	def add(cls, record, using=None):
		cls.objects.using(using).create(
			publication_id = record.id,
		    hash_id = record.hash_id,
		    lat = float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
		    lng = float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

		    market_type_sid = record.body.market_type_sid,
		    halls_area = record.body.halls_area,
		    total_area = record.body.total_area,
		    building_type_sid = record.body.building_type_sid,
			hot_water = record.body.hot_water,
			cold_water = record.body.cold_water,
			gas = record.body.gas,
			electricity = record.body.electricity,
			sewerage = record.body.sewerage,

		    price = record.sale_terms.price,
		    currency_sid = record.sale_terms.currency_sid,
		)


	@classmethod
	def min_queryset(cls):
		return cls.objects.all().only(
			'hash_id', 'lat', 'lng', 'price', 'currency_sid', 'total_area') # todo: fixme


	@classmethod
	def min_add_queryset(cls):
		return cls.objects.all().only(
			'degree_lat',
			'degree_lng',
			'segment_lat',
			'segment_lng',
			'pos_lat',
			'pos_lng',

		    'id',
		    'hash_id',

			'body__market_type_sid',
		    'body__halls_area',
		    'body__total_area',
		    'body__building_type_sid',
			'body__hot_water',
			'body__cold_water',
			'body__electricity',
		    'body__gas',
		    'body__fire_alarm',
		    'body__security_alarm',

			'sale_terms__price',
			'sale_terms__currency_sid'
		)


	@classmethod
	def apply_filters(cls, filters, markers):
		markers = cls.apply_market_type_filter(filters, markers)
		markers = cls.apply_price_filter(filters, markers)
		markers = cls.apply_halls_area_filter(filters, markers)
		markers = cls.apply_total_area_filter(filters, markers)
		markers = cls.apply_trade_building_type_filter(filters, markers)
		markers = cls.apply_electricity_filter(filters, markers)
		markers = cls.apply_gas_filter(filters, markers)
		markers = cls.apply_hot_water_filter(filters, markers)
		markers = cls.apply_cold_water_filter(filters, markers)
		markers = cls.apply_sewerage_filter(filters, markers)
		return markers


	@classmethod
	def brief(cls, marker, filters=None):
		currency = cls.currency_from_filters(filters)
		price = cls.convert_and_format_price(marker.price, marker.currency_sid, currency)
		total_area = '{0}'.format(marker.total_area).rstrip('0').rstrip('.')

		return {
			'id': marker.hash_id,
		    'd0': u'{0} м²'.format(total_area),
			'd1': u'{0} {1}'.format(price, cls.currency_to_str(currency)),
		}


class GaragesIndex(AbstractBaseIndex):
	price = models.FloatField(db_index=True)
	currency_sid = models.PositiveSmallIntegerField()
	total_area = models.FloatField(db_index=True)
	ceiling_height = models.FloatField(db_index=True)
	pit = models.BooleanField(db_index=True)

	class Meta:
		db_table = 'index_garages'


	@classmethod
	def add(cls, record, using=None):
		cls.objects.using(using).create(
			publication_id = record.id,
		    hash_id = record.hash_id,
		    lat = float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
		    lng = float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

		    total_area = record.body.total_area,
		    ceiling_height = record.body.ceiling_height,
		    pit = record.body.pit,

		    price = record.sale_terms.price,
		    currency_sid = record.sale_terms.currency_sid,
		)


	@classmethod
	def min_queryset(cls):
		return cls.objects.all().only(
			'hash_id', 'lat', 'lng', 'price', 'currency_sid', 'total_area') # todo: fixme


	@classmethod
	def min_add_queryset(cls):
		return cls.objects.all().only(
			'degree_lat',
			'degree_lng',
			'segment_lat',
			'segment_lng',
			'pos_lat',
			'pos_lng',

		    'id',
		    'hash_id',

			'body__total_area',
		    'body__ceiling_height',
			'body__pit',

			'sale_terms__price',
			'sale_terms__currency_sid'
		)


	@classmethod
	def apply_filters(cls, filters, markers):
		markers = cls.apply_market_type_filter(filters, markers)
		markers = cls.apply_price_filter(filters, markers)
		markers = cls.apply_total_area_filter(filters, markers)
		markers = cls.apply_ceiling_height_filter(filters, markers)
		markers = cls.apply_pit_filter(filters, markers)
		return markers


	@classmethod
	def brief(cls, marker, filters=None):
		currency = cls.currency_from_filters(filters)
		price = cls.convert_and_format_price(marker.price, marker.currency_sid, currency)
		total_area = '{0}'.format(marker.total_area).rstrip('0').rstrip('.')

		return {
			'id': marker.hash_id,
		    'd0': u'{0} м²'.format(total_area),
			'd1': u'{0} {1}'.format(price, cls.currency_to_str(currency)),
		}


class LandsIndex(AbstractBaseIndex):
	price = models.FloatField(db_index=True)
	currency_sid = models.PositiveSmallIntegerField()
	total_area = models.FloatField(db_index=True)
	water = models.BooleanField(db_index=True)
	electricity = models.BooleanField(db_index=True)
	gas = models.BooleanField(db_index=True)
	sewerage = models.BooleanField(db_index=True)

	class Meta:
		db_table = 'index_lands'


	@classmethod
	def add(cls, record, using=None):
		cls.objects.using(using).create(
			publication_id = record.id,
		    hash_id = record.hash_id,
		    lat = float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
		    lng = float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

		    total_area = record.body.total_area,
		    water = record.body.water,
		    electricity = record.body.electricity,
		    gas = record.body.gas,
		    sewerage = record.body.sewerage,

		    price = record.sale_terms.price,
		    currency_sid = record.sale_terms.currency_sid,
		)


	@classmethod
	def min_queryset(cls):
		return cls.objects.all().only(
			'hash_id', 'lat', 'lng', 'price', 'currency_sid', 'total_area') # todo: fixme


	@classmethod
	def min_add_queryset(cls):
		return cls.objects.all().only(
			'degree_lat',
			'degree_lng',
			'segment_lat',
			'segment_lng',
			'pos_lat',
			'pos_lng',

		    'id',
		    'hash_id',

			'body__total_area',
		    'body__water',
			'body__electricity',
			'body__gas',
			'body__sewerage',

			'sale_terms__price',
			'sale_terms__currency_sid'
		)


	@classmethod
	def apply_filters(cls, filters, markers):
		markers = cls.apply_market_type_filter(filters, markers)
		markers = cls.apply_price_filter(filters, markers)
		markers = cls.apply_total_area_filter(filters, markers)
		markers = cls.apply_water_filter(filters, markers)
		markers = cls.apply_electricity_filter(filters, markers)
		markers = cls.apply_gas_filter(filters, markers)
		markers = cls.apply_sewerage_filter(filters, markers)
		return markers


	@classmethod
	def brief(cls, marker, filters=None):
		currency = cls.currency_from_filters(filters)
		price = cls.convert_and_format_price(marker.price, marker.currency_sid, currency)
		total_area = '{0}'.format(marker.total_area).rstrip('0').rstrip('.')

		return {
			'id': marker.hash_id,
		    'd0': u'{0} м²'.format(total_area),
			'd1': u'{0} {1}'.format(price, cls.currency_to_str(currency)),
		}


#-- index handler
class SegmentsIndex(models.Model):
	index_db_name = 'markers_index'
	min_zoom = 1
	max_zoom = 15


	# static members
	grid = Grid(min_zoom, max_zoom)

	sale_indexes = {
		OBJECTS_TYPES.flat():   FlatsSaleIndexAbstract,
		OBJECTS_TYPES.house():  HousesSaleIndexAbstract,
		OBJECTS_TYPES.room():   RoomsSaleIndexAbstract,
	}
	rent_indexes = {
		OBJECTS_TYPES.flat():   FlatsRentIndexAbstract,
		OBJECTS_TYPES.house():  HousesRentIndexAbstract,
		OBJECTS_TYPES.room():   RoomsRentIndex,
	}
	commercial_indexes = {
		OBJECTS_TYPES.trade():      TradesIndex,
		OBJECTS_TYPES.office():     OfficesIndex,
		OBJECTS_TYPES.warehouse():  WarehousesIndex,
		OBJECTS_TYPES.business():   BusinessesIndex,
		OBJECTS_TYPES.catering():   CateringsIndex,
		OBJECTS_TYPES.garage():     GaragesIndex,
		OBJECTS_TYPES.land():       LandsIndex,
	}


	# fields
	tid = models.SmallIntegerField(db_index=True)
	zoom = models.SmallIntegerField(db_index=True)
	x = models.SmallIntegerField(db_index=True)
	y = models.SmallIntegerField(db_index=True)
	ids = BigIntegerArrayField()

	class Meta:
		db_table = 'index_all_segments'


	@classmethod
	def add_record(cls, tid, hid):
		index = cls.commercial_indexes.get(tid)
		if index is None:
			index = cls.sale_indexes.get(tid)
			if index is None:
				index = cls.rent_indexes.get(tid)
				if index is None:
					raise ValueError('Invalid tid')

		record = index.min_add_queryset().filter(id = hid)[:1][0]


		lat, lng = cls.record_lat_lng(record)
		lat, lng = cls.grid.normalize_lat_lng(lat, lng)


		# todo: add transaction here (find a way to combine custom sql and django orm to perform a transaction)
		if record.for_sale:
			cls.sale_indexes[record.tid].add(record, using=cls.index_db_name)
		else:
			cls.rent_indexes[record.tid].add(record, using=cls.index_db_name)


		cursor = cls.cursor()
		cursor.execute('BEGIN;')
		for zoom, x, y in cls.grid.segments_digests(lat, lng):
			# UPSERT emulation.
			# Query will execute UPDATE if record with such segment digest already exists,
			# otherwise the INSERT will be executed.
			cursor.execute(
				"UPDATE {table}"
				"   SET ids = array_append(ids, '{id}')"
				"   WHERE tid='{tid}' AND zoom='{zoom}' AND x='{x}' AND y='{y}';"

				"INSERT INTO {table} (tid, zoom, x, y, ids)"
				"   (SELECT {tid}, {zoom}, {x}, {y}, '{{ {id} }}'"
				"    WHERE NOT EXISTS ("
				"       SELECT 1 FROM {table} WHERE tid='{tid}' AND zoom='{zoom}' AND x='{x}' AND y='{y}'));"
				.format(
					table = cls._meta.db_table,
				    id = record.id,
				    tid = record.tid,
				    zoom = zoom,
				    x = x,
				    y = y,
				)
			)
		cursor.execute('END;')
		cursor.close()


	@classmethod
	def remove_record(cls, tid, hid):
		# todo: даний метод потребує перевірки на реальному сервері postgres >=9.3
		# todo: даний метод потребує тестів

		index = cls.commercial_indexes.get(tid)
		if index is None:
			index = cls.sale_indexes.get(tid)
			if index is None:
				index = cls.rent_indexes.get(tid)
				if index is None:
					raise ValueError('Invalid tid')

		record = index.min_remove_queryset().filter(id = hid)[:1][0]


		lat, lng = cls.record_lat_lng(record)


		# todo: add transaction here (find a way to combine custom sql and django orm to perform a transaction)
		if record.for_sale:
			cls.sale_indexes[record.tid].remove(record, using=cls.index_db_name)
		else:
			cls.rent_indexes[record.tid].remove(record, using=cls.index_db_name)


		cursor = cls.cursor()
		cursor.execute('BEGIN;')
		for zoom, x, y in cls.grid.segments_digests(lat, lng):

			# Removing of the id from the index
			cursor.execute(
				"SELECT array_remove(ids, {id}) FROM {table};"
				.format(
					table = cls._meta.db_table,
					id = record.id,
				))

			# If segment digest contains no more ids - remove it too
			cursor.execute(
				"DELETE FROM {table}"
				"   WHERE tid='{tid}' AND zoom='{zoom}' AND x='{x}' AND y='{y}' AND array_length('ids', 1) = 0;"
				.format(
					table = cls._meta.db_table,
				    id = record.id,
				    tid = record.tid,
				    zoom = zoom,
				    x = x,
				    y = y,
				)
			)
		cursor.execute('END;')
		cursor.close()


	@classmethod
	def estimate_count(cls, tid, ne_lat, ne_lng, sw_lat, sw_lng, zoom, filters):
		ne_segment_x, ne_segment_y, sw_segment_x, sw_segment_y = \
			cls.prepare_request_processing(ne_lat, ne_lng, sw_lat, sw_lng, zoom)


		# Помітки for_sale та for_rent ставляться лише для житлової нерухомості
		if 'for_sale' in filters:
			index = cls.sale_indexes[tid]
		elif 'for_rent' in filters:
			index = cls.rent_indexes[tid]
		else:
			# інакше — це точно комерційна нерухомість.
			index = cls.commercial_indexes[tid]


		# Підготувати SQL-запит на вибірку записів, попередньо відфільтрувавши за вхідними умовами.
		# Використовуєтсья спільний для обох методів (markers та estimate_count) спосіб обробки фільтрів
		# на основі django-ORM
		markers = index.apply_filters(filters, index.objects.all())
		markers_query = str(markers.query)

		# Далі, зі сформованого запиту виокремлюємо блок WHERE щоб вставити його в кастомний запит.
		# Django-ORM не дозволяє виконати запит такого типу,
		# а оскільки в ньому використовуються збережувані процедури та sql діалект,
		# то чистий sql в даному випадку є найбільш оптимальним рішенням по швидкодії/легкості імплементації.
		try:
			where = markers_query[markers_query.index('WHERE'):][5:]
		except ValueError:
			where = '' # no WHERE condition is found


		query = "SELECT count(publication_id), x, y FROM {index_table}" \
		        "   JOIN {segments_index_table} " \
		        "       ON zoom = '{zoom}' AND " \
		        "          (x >= {ne_segment_x} AND x <= {sw_segment_x}) AND " \
		        "          (y >= {ne_segment_y} AND y <= {sw_segment_y}) " \
		        "   WHERE publication_id = ANY(ids) {where_condition}" \
		        "   GROUP BY ids, x, y;"\
			.format(
				index_table = index._meta.db_table,
		        segments_index_table = cls._meta.db_table,
		        zoom = zoom,
		        ne_segment_x = ne_segment_x,
			    sw_segment_x = sw_segment_x,
			    ne_segment_y = ne_segment_y,
			    sw_segment_y = sw_segment_y,
		        where_condition = ' AND ' + where if where else '',
			)


		cursor = cls.cursor()
		cursor.execute(query)
		selected_data = cursor.fetchall()
		cursor.close()


		step_per_lat = cls.grid.step_on_lat(zoom)
		step_per_lng = cls.grid.step_on_lng(zoom)
		return {
			'{lat}:{lng}'.format(
				lat = y * step_per_lat + (step_per_lat / 2) - 90, # денормалізація широти
				lng = x * step_per_lng + (step_per_lng / 2) - 180, # денормалізація довготи
			) : count
		    for count, x ,y in selected_data
		}



	@classmethod
	def markers(cls, tid, ne_lat, ne_lng, sw_lat, sw_lng, filters):
		zoom = 14
		ne_segment_x, ne_segment_y, sw_segment_x, sw_segment_y = \
			cls.prepare_request_processing(ne_lat, ne_lng, sw_lat, sw_lng, zoom)


		query = "SELECT DISTINCT unnest(ids), id FROM {table} " \
		        "   WHERE tid={tid} AND zoom={zoom} AND " \
		        "      (x >= {ne_segment_x} AND x <= {sw_segment_x}) AND " \
		        "      (y >= {ne_segment_y} AND y <= {sw_segment_y});"\
			.format(
				table = cls._meta.db_table,
			    tid = tid,
			    zoom = zoom,
			    ne_segment_x = ne_segment_x,
			    sw_segment_x = sw_segment_x,
			    ne_segment_y = ne_segment_y,
			    sw_segment_y = sw_segment_y,
			)


		cursor = cls.cursor()
		cursor.execute(query)
		publications_ids = [id for id, _ in cursor.fetchall()]
		cursor.close()


		if not publications_ids:
			return {}

		# Фільтруєм і формуєм маркери.
		# (Помітки for_sale та for_rent ставляться лише для житлової нерухомості)
		if 'for_sale' in filters:
			index = cls.sale_indexes[tid]
		elif 'for_rent' in filters:
			index = cls.rent_indexes[tid]
		else:
			index = cls.commercial_indexes[tid]


		markers = index.min_queryset().filter(publication_id__in = publications_ids)
		return {
			'{lat}:{lng}'.format(
				lat=marker.lat,
				lng=marker.lng
			) : cls.brief(marker, filters)
			for marker in cls.apply_filters(filters, markers)
		}



	@classmethod
	def cursor(cls):
		"""
		NOTE: this method may be used to implement requests routing
			  in case when markers indexes are replicated to several hosts.
		:return: database cursor to table with markers indexes.
		"""
		return connections[cls.index_db_name].cursor()


	@staticmethod
	def record_lat_lng(record):
		return float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)), \
		       float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng))


	@classmethod
	def prepare_request_processing(cls, ne_lat, ne_lng, sw_lat, sw_lng, zoom):
		ne_lat, ne_lng = cls.grid.normalize_lat_lng(ne_lat, ne_lng)
		sw_lat, sw_lng = cls.grid.normalize_lat_lng(sw_lat, sw_lng)

		# Повертаємо координатний прямокутник таким чином, щоб ne точно був на своєму місці.
		# Таким чином уберігаємось від випадків, коли координати передані некоректно,
		# або в залежності від форми Землі сегмент деформується і набирає неправильної форми.
		if ne_lat < sw_lat:
			sw_lat, ne_lat = ne_lat, sw_lat

		if ne_lng > sw_lng:
			sw_lng, ne_lng = ne_lng, sw_lng


		ne_segment_x, ne_segment_y = cls.grid.segment_xy(ne_lat, ne_lng, zoom)
		sw_segment_x, sw_segment_y = cls.grid.segment_xy(sw_lat, sw_lng, zoom)


		# Заглушка від DDos
		lng_segments_count = sw_segment_x - ne_segment_x if sw_segment_x - ne_segment_x > 0 else 1
		lat_segments_count = ne_segment_y - sw_segment_y if ne_segment_y - sw_segment_y > 0 else 1
		total_segments_count = lat_segments_count * lng_segments_count
		if total_segments_count > 64:
			raise TooBigTransaction()


		return ne_segment_x, ne_segment_y, \
		       sw_segment_x, sw_segment_y