#coding=utf-8
from django.db import DatabaseError, IntegrityError
from collective.methods.formatters import format_text, format_title
from core.publications.constants import CURRENCIES, SALE_TRANSACTION_TYPES, LIVING_RENT_PERIODS, MARKET_TYPES, OBJECT_CONDITIONS, HEATING_TYPES, INDIVIDUAL_HEATING_TYPES, FLOOR_TYPES
from core.publications.models import RoomsHeads, RoomsBodies, RoomsRentTerms
from core.publications.objects_constants.flats import FLAT_BUILDING_TYPES, FLAT_ROOMS_PLANNINGS

# Оновлює інформацію про кімнату.
#
# Поле для оновлення відшукується за префіксом @prefix.
# Значення, що онволюється (@value) перевіряється лише на коректність з точки зору БД та системи:
# (недопустимі, умисно некоректні значення, такі, що можуть призвести до збоїв системи)
#
# Жодних перевірок щодо правдивості та консистентності введеного значення не здійснюється,
# оскільки, на момет вводу, система може не володіти достатнім контекстом,
# а для його отримання часто необхідно виконати один або декілька додаткових запитів до БД,
# що відобразиться на продуктивності системи в цілому.
#
# Крім цього, користувач може вводити дані не послідовно, пропускаючи деякі поля,
# (напр. завідомо плануючи залишити оголошення в чернетках на деякий термін)
# тоді як перевірка певних полів може залежати від значень інших, пропущених полів.
#
# Перевірку консистентності даних слід виконувати на етапі підготовки оголошення до публікації.

def update_room(prefix, value, head_id=None, body_id=None, rent_id=None):
	try:
		# bool
		if prefix == 'for_sale':
			if value == 'true':
				h = RoomsHeads.by_id(head_id, head_id='for_sale')
				h.for_sale = True
				h.save(force_update=True)

			elif value == 'false':
				h = RoomsHeads.by_id(head_id, head_id='for_sale')
				h.for_sale = False
				h.save(force_update=True)

			else:
				raise ValueError('Invalid @for_sale value.')


		# bool
		elif prefix == 'for_rent':
			if value == 'true':
				h = RoomsHeads.by_id(head_id, head_id='for_rent')
				h.for_rent = True
				h.save(force_update=True)

			elif value == 'false':
				h = RoomsHeads.by_id(head_id, head_id='for_rent')
				h.for_rent = False
				h.save(force_update=True)

			else:
				raise ValueError('Invalid @for_rent value.')


		# blank or decimal
		elif prefix == 'price':
			if not value:
				b = RoomsBodies.by_id(body_id, only='price')
				b.price = None
				b.save(force_update=True)

			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError('Invalid price')

				b = RoomsBodies.by_id(body_id, only='price')
				b.price = value
				b.save(force_update=True)

				if int(value) == float(value):
					# Якщо після коми лише нулі - повернути ціле значення
					return "%.0f" % value
				else:
					# Інакше - округлити до 2х знаків після коми
					return "%.2f" % value


		# sid
		elif prefix == 'transaction_type':
			value = int(value)
			if value not in SALE_TRANSACTION_TYPES.values():
				raise ValueError('Invalid transaction type sid')

			b = RoomsBodies.by_id(body_id, only='transaction_type_sid')
			b.transaction_type_sid = value
			b.save(force_update=True)


		# sid
		elif prefix == 'currency':
			value = int(value)
			if value not in CURRENCIES.values():
				raise ValueError('Invalid currency sid')

			b = RoomsBodies.by_id(body_id, only='currency_sid')
			b.currency_sid = value
			b.save(force_update=True)


		# bool
		elif prefix == 'price_contract':
			if value == 'true':
				b = RoomsBodies.by_id(body_id, only='price_is_contract')
				b.price_is_contract = True
				b.save(force_update=True)

			elif value == 'false':
				b = RoomsBodies.by_id(body_id, only='price_is_contract')
				b.price_is_contract = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid @price_is_contract value.')


		# text
		elif prefix == 'sale_add_terms':
			b = RoomsBodies.by_id(body_id, only='add_terms')
			if not value:
				b.add_terms = None
				b.save(force_update=True)

			else:
				value = format_text(value)
				b.add_terms = value
				b.save(force_update=True)
				return value


		# sid
		elif prefix == 'rent_period':
			value = int(value)
			if value not in LIVING_RENT_PERIODS.values():
				raise ValueError('Invalid rent period value.')

			r = RoomsRentTerms.by_id(rent_id, only='period_sid')
			r.period_sid = value
			r.save(force_update=True)


		# blank or int
		elif prefix == 'rent_persons_count':
			if not value:
				r = RoomsRentTerms.by_id(rent_id, only='persons_count')
				r.persons_count = None
				r.save(force_update=True)

			else:
				value = int(value)
				if value <= 0:
					raise ValueError('Invalid persons count')

				r = RoomsRentTerms.by_id(rent_id, only='persons_count')
				r.persons_count = int(value)
				r.save(force_update=True)


		# blank or decimal
		elif prefix == 'rent_price':
			if not value:
				r = RoomsRentTerms.by_id(rent_id, only='price')
				r.price = None
				r.save(force_update=True)

			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError('Invalid rent price')

				r = RoomsRentTerms.by_id(rent_id, only='price')
				r.price = value
				r.save(force_update=True)

				if int(value) == value:
					# Якщо після коми лише нулі - повернути ціле значення
					return "%.0f" % value

				else:
					# Інакше - округлити до 2х знаків після коми
					return "%.2f" % value


		# sid
		elif prefix == 'rent_currency':
			value = int(value)
			if value not in CURRENCIES.values():
				raise ValueError('Invalid rent currency')

			r = RoomsRentTerms.by_id(rent_id, only='currency_sid')
			r.currency_sid = value
			r.save(force_update=True)
			return


		# boolean
		elif prefix == 'rent_price_contract':
			if value == 'true':
				r = RoomsRentTerms.by_id(rent_id, only='price_is_contract')
				r.price_is_contract = True
				r.save(force_update=True)

			elif value == 'false':
				r = RoomsRentTerms.by_id(rent_id, only='price_is_contract')
				r.price_is_contract = False
				r.save(force_update=True)

			else:
				raise ValueError('Invalid rent @price_is_contract')


		# boolean
		elif prefix == 'rent_for_family':
			if value == 'true':
				r = RoomsRentTerms.by_id(rent_id, only='family')
				r.family = True
				r.save(force_update=True)

			elif value == 'false':
				r = RoomsRentTerms.by_id(rent_id, only='family')
				r.family = False
				r.save(force_update=True)

			else:
				raise ValueError('Invalid @rent_for_family.')


		# boolean
		elif prefix == 'rent_smoking':
			if value == 'true':
				r = RoomsRentTerms.by_id(rent_id, only='smoking')
				r.smoking = True
				r.save(force_update=True)

			elif value == 'false':
				r = RoomsRentTerms.by_id(rent_id, only='smoking')
				r.smoking = False
				r.save(force_update=True)

			else:
				raise ValueError('Invalid @rent_smoking.')


		# boolean
		elif prefix == 'rent_foreigners':
			if value == 'true':
				r = RoomsRentTerms.by_id(rent_id, only='foreigners')
				r.foreigners = True
				r.save(force_update=True)

			elif value == 'false':
				r = RoomsRentTerms.by_id(rent_id, only='foreigners')
				r.foreigners = False
				r.save(force_update=True)

			else:
				raise ValueError('Invalid @rent_foreigners.')


		# boolean
		elif prefix == 'rent_pets':
			if value == 'true':
				r = RoomsRentTerms.by_id(rent_id, only='pets')
				r.pets = True
				r.save(force_update=True)

			elif value == 'false':
				r = RoomsRentTerms.by_id(rent_id, only='pets')
				r.pets = False
				r.save(force_update=True)

			else:
				raise ValueError('Invalid @rent_pets.')


		# text
		elif prefix == 'rent_add_terms':
			r = RoomsRentTerms.by_id(rent_id, only='add_terms')
			if not value:
				r.add_terms = None
				r.save(force_update=True)

			else:
				value = format_text(value)
				r.add_terms = value
				r.save(force_update=True)
				return value


		# text
		elif prefix == 'title':
			h = RoomsHeads.by_id(head_id, head_id='title')
			if not value:
				h.title = None
				h.save(force_update=True)

			else:
				value = format_title(value)
				h.title = value
				h.save(force_update=True)
				return value


		# text
		elif prefix == 'description':
			h = RoomsHeads.by_id(head_id, head_id='descr')
			if not value:
				h.descr = None
				h.save(force_update=True)
				return

			else:
				value = format_text(value)
				h.descr = value
				h.save(force_update=True)
				return value


		# sid
		elif prefix == 'market_type':
			value = int(value)
			if value not in MARKET_TYPES.values():
				raise ValueError('Invalid market type sid')

			b = RoomsBodies.by_id(body_id, only='market_type_sid')
			b.market_type_sid = value
			b.save(force_update=True)


		# sid
		elif prefix == 'building_type':
			value = int(value)
			if value not in FLAT_BUILDING_TYPES.values():
				raise ValueError('Invalid building type id')

			b = RoomsBodies.by_id(body_id, only='building_type_sid')
			b.building_type_sid = value
			b.save(force_update=True)
			return


		# text
		elif prefix == 'custom_building_type':
			b = RoomsBodies.by_id(body_id, only='custom_building_type')
			if not value:
				b.custom_building_type = None
				b.save(force_update=True)

			else:
				# ... форматування тут ...
				b.custom_building_type = value
				b.save(force_update=True)
				return value


		# blank or int
		elif prefix == 'build_year':
			if not value:
				b = RoomsBodies.by_id(body_id, only='build_year')
				b.build_year = None
				b.save(force_update=True)

			else:
				value = int(value)
				if value < 0:
					raise ValueError('Invalid build year.')

				b = RoomsBodies.by_id(body_id, only='build_year')
				b.build_year = value
				b.save(force_update=True)


		# sid
		elif prefix == 'rooms_planing':
			value = int(value)
			if value not in FLAT_ROOMS_PLANNINGS.values():
				raise ValueError('Invalid rooms planing sid.')

			b = RoomsBodies.by_id(body_id, only='rooms_planing_sid')
			b.rooms_planing_sid = value
			b.save(force_update=True)


		# sid
		elif prefix == 'condition':
			value = int(value)
			if value not in OBJECT_CONDITIONS.values():
				raise ValueError('Invalid condition id.')

			b = RoomsBodies.by_id(body_id, only='condition_sid')
			b.condition_sid = value
			b.save(force_update=True)


		# blank or int
		elif prefix == 'floor':
			if not value:
				b = RoomsBodies.by_id(body_id, only='floor')
				b.floor = None
				b.save(force_update=True)

			else:
				value = int(value)
				b = RoomsBodies.by_id(body_id, only='floor')
				b.floor = value
				b.save(force_update=True)


		# sid
		elif prefix == 'floor_type':
			value = int(value)
			if value not in FLOOR_TYPES.values():
				raise ValueError('Invalid floor type sid.')

			b = RoomsBodies.by_id(body_id, only='floor_type_sid')
			b.floor_type_sid = value

			# Якщо тип поверху "мансарда" або "цоколь", то ітак зрозуміло,
			# шо це або останній поверх, або нульовий/перший.
			# Немає необхідності зберігати додаткові дані.
			if value in [FLOOR_TYPES.mansard(), FLOOR_TYPES.ground()]:
				b.floor = None

			b.save(force_update=True)


		# blank or int
		elif prefix == 'floors_count':
			if not value:
				b = RoomsBodies.by_id(body_id, only='floors_count')
				b.floors_count = None
				b.save(force_update=True)
				return

			else:
				value = int(value)
				if value <= 0:
					raise ValueError('Invalid floors count.')

				b = RoomsBodies.by_id(body_id, only='floors_count')
				b.floors_count = int(value)
				b.save(force_update=True)


		# blank or float
		elif prefix == 'total_area':
			if not value:
				b = RoomsBodies.by_id(body_id, only='total_area')
				b.total_area = None
				b.save(force_update=True)

			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError('Invalid total area value.')

				b = RoomsBodies.by_id(body_id, only='total_area')
				b.total_area = value
				b.save(force_update=True)

				if int(value) == value:
					# Відсікти дробову частину, якщо після коми нулі
					return "%.0f" % value
				else:
					# Скоротити / розширити до 2х цифр після коми
					return "%.2f" % value


		# blank or float
		elif prefix == 'living_area':
			if not value:
				b = RoomsBodies.by_id(body_id, only='living_area')
				b.living_area = None
				b.save(force_update=True)

			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError('Invalid living area value.')

				b = RoomsBodies.by_id(body_id, only='living_area')
				b.living_area = value
				b.save(force_update=True)

				if int(value) == value:
					# Відсікти дробову частину, якщо після коми нулі
					return "%.0f" % value
				else:
					# скоротити / розширити до 2х цифр після коми
					return "%.2f" % value


		# blank or float
		elif prefix == 'kitchen_area':
			if not value:
				b = RoomsBodies.by_id(body_id, only='kitchen_area')
				b.kitchen_area = None
				b.save(force_update=True)

			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError('Invalid kitchen area value.')

				b = RoomsBodies.by_id(body_id, only='kitchen_area')
				b.kitchen_area = value
				b.save(force_update=True)

				if int(value) == value:
					# Відсікти дробову частину, якщо після коми нулі
					return "%.0f" % value
				else:
					# скоротити / розширити до 2х цифр після коми
					return "%.2f" % value


		# blank or int
		elif prefix == 'rooms_count':
			if not value:
				b = RoomsBodies.by_id(body_id, only='rooms_count')
				b.rooms_count = None
				b.save(force_update=True)

			else:
				value = int(value)
				if value < 0:
					raise ValueError('Invalid rooms count value.')

				b = RoomsBodies.by_id(body_id, only='rooms_count')
				b.rooms_count = value
				b.save(force_update=True)


		# todo: РОЗІБРАТИСЬ ІЗ ЦИМ ПОЛЕМ
		## sid
		#elif prefix == 'vc_loc':
		#	value = int(value)
		#	if value not in ROOMS_WC_LOCATIONS.values():
		#		raise ValueError('Invalid vc location sid.')
		#
		#	b = RoomsBodies.by_id(body_id, only='vc_loc_sid')
		#	b.vc_loc_sid = value
		#	b.save(force_update=True)


		# sid
		elif prefix == 'heating_type':
			value = int(value)
			if value not in HEATING_TYPES.values():
				raise ValueError('Invalid heating id.')

			b = RoomsBodies.by_id(body_id, only='heating_type_sid')
			b.heating_type_sid = value
			b.save(force_update=True)


		# text
		elif prefix == 'custom_heating_type':
			b = RoomsBodies.by_id(body_id, only='custom_heating_type')
			if not value:
				b.custom_heating_type = None
				b.save(force_update=True)

			else:
				# ... форматування тут ...
				b.custom_heating_type = value
				b.save(force_update=True)
				return value


		# sid
		elif prefix == 'ind_heating_type':
			value = int(value)
			if value not in INDIVIDUAL_HEATING_TYPES.values():
				raise ValueError('Invalid individual heating id.')

			b = RoomsBodies.by_id(body_id, only='ind_heating_type_sid')
			b.ind_heating_type_sid = value
			b.save(force_update=True)


		# text
		elif prefix == 'custom_ind_heating_type':
			b = RoomsBodies.by_id(body_id, only='custom_ind_heating_type')
			if not value:
				b.custom_ind_heating_type = None
				b.save(force_update=True)

			else:
				# ... форматування тут ...
				b.custom_ind_heating_type = value
				b.save(force_update=True)
				return value


		# boolean
		elif prefix == 'electricity':
			if value == 'true':
				b = RoomsBodies.by_id(body_id, only='electricity')
				b.electricity = True
				b.save(force_update=True)

			elif value == 'false':
				b = RoomsBodies.by_id(body_id, only='electricity')
				b.electricity = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid electricity value.')


		# boolean
		elif prefix == 'gas':
			if value == 'true':
				b = RoomsBodies.by_id(body_id, only='gas')
				b.gas = True
				b.save(force_update=True)

			elif value == 'false':
				b = RoomsBodies.by_id(body_id, only='gas')
				b.gas = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid gas value.')


		# boolean
		elif prefix == 'security_alarm':
			if value == 'true':
				b = RoomsBodies.by_id(body_id, only='security_alarm')
				b.security_alarm = True
				b.save(force_update=True)

			elif value == 'false':
				b = RoomsBodies.by_id(body_id, only='security_alarm')
				b.security_alarm = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid security alarm value.')


		# boolean
		elif prefix == 'fire_alarm':
			if value == 'true':
				b = RoomsBodies.by_id(body_id, only='fire_alarm')
				b.fire_alarm = True
				b.save(force_update=True)

			elif value == 'false':
				b = RoomsBodies.by_id(body_id, only='fire_alarm')
				b.fire_alarm = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid fire alarm value.')


		# boolean
		elif prefix == 'hot_water':
			if value == 'true':
				b = RoomsBodies.by_id(body_id, only='hot_water')
				b.hot_water = True
				b.save(force_update=True)

			elif value == 'false':
				b = RoomsBodies.by_id(body_id, only='hot_water')
				b.hot_water = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid fire alarm value.')


		# boolean
		elif prefix == 'cold_water':
			if value == 'true':
				b = RoomsBodies.by_id(body_id, only='cold_water')
				b.cold_water = True
				b.save(force_update=True)

			elif value == 'false':
				b = RoomsBodies.by_id(body_id, only='cold_water')
				b.cold_water = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid cold water value.')


		# boolean
		elif prefix == 'lift':
			if value == 'true':
				b = RoomsBodies.by_id(body_id, only='lift')
				b.lift = True
				b.save(force_update=True)

			elif value == 'false':
				b = RoomsBodies.by_id(body_id, only='lift')
				b.lift = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid lift value.')


		# boolean
		elif prefix == 'furniture':
			if value == 'true':
				r = RoomsRentTerms.by_id(rent_id, only='furniture')
				r.furniture = True
				r.save(force_update=True)

			elif value == 'false':
				r = RoomsRentTerms.by_id(rent_id, only='furniture')
				r.furniture = False
				r.save(force_update=True)

			else:
				raise ValueError('Invalid furniture value.')


		# boolean
		elif prefix == 'washing_machine':
			if value == 'true':
				r = RoomsRentTerms.by_id(rent_id, only='washing_machine')
				r.washing_machine = True
				r.save(force_update=True)

			elif value == 'false':
				r = RoomsRentTerms.by_id(rent_id, only='washing_machine')
				r.washing_machine = False
				r.save(force_update=True)

			else:
				raise ValueError('Invalid washing machine value.')


		# boolean
		elif prefix == 'refrigerator':
			if value == 'true':
				r = RoomsRentTerms.by_id(rent_id, only='refrigerator')
				r.refrigerator = True
				r.save(force_update=True)

			elif value == 'false':
				r = RoomsRentTerms.by_id(rent_id, only='refrigerator')
				r.refrigerator = False
				r.save(force_update=True)

			else:
				raise ValueError('Invalid refrigerator value.')


		# boolean
		elif prefix == 'conditioner':
			if value == 'true':
				r = RoomsRentTerms.by_id(rent_id, only='conditioner')
				r.conditioner = True
				r.save(force_update=True)

			elif value == 'false':
				r = RoomsRentTerms.by_id(rent_id, only='conditioner')
				r.conditioner = False
				r.save(force_update=True)

			else:
				raise ValueError('Invalid conditioner value.')


		# boolean
		elif prefix == 'tv':
			if value == 'true':
				r = RoomsRentTerms.by_id(rent_id, only='tv')
				r.tv = True
				r.save(force_update=True)

			elif value == 'false':
				r = RoomsRentTerms.by_id(rent_id, only='tv')
				r.tv = False
				r.save(force_update=True)

			else:
				raise ValueError('Invalid tv value.')


		# boolean
		elif prefix == 'home_theater':
			if value == 'true':
				r = RoomsRentTerms.by_id(rent_id, only='home_theater')
				r.home_theater = True
				r.save(force_update=True)

			elif value == 'false':
				r = RoomsRentTerms.by_id(rent_id, only='home_theater')
				r.home_theater = False
				r.save(force_update=True)

			else:
				raise ValueError('Invalid home theater value.')


		# text
		elif prefix == 'add_facilities':
			b = RoomsBodies.by_id(body_id, only='add_facilities')
			if not value:
				b.add_facilities = None
				b.save(force_update=True)

			else:
				# ... форматування тут ...
				b.add_facilities = value
				b.save(force_update=True)
				return value


		# boolean
		elif prefix == 'phone':
			if value == 'true':
				b = RoomsBodies.by_id(body_id, only='phone')
				b.phone = True
				b.save(force_update=True)

			elif value == 'false':
				b = RoomsBodies.by_id(body_id, only='phone')
				b.phone = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid phone value.')


		# boolean
		elif prefix == 'mobile_coverage':
			if value == 'true':
				b = RoomsBodies.by_id(body_id, only='mobile_coverage')
				b.mobile_coverage = True
				b.save(force_update=True)

			elif value == 'false':
				b = RoomsBodies.by_id(body_id, only='mobile_coverage')
				b.mobile_coverage = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid mobile coverage value.')


		# boolean
		elif prefix == 'internet':
			if value == 'true':
				b = RoomsBodies.by_id(body_id, only='internet')
				b.internet = True
				b.save(force_update=True)

			elif value == 'false':
				b = RoomsBodies.by_id(body_id, only='internet')
				b.internet = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid internet value.')


		# boolean
		elif prefix == 'cab_tv':
			if value == 'true':
				b = RoomsBodies.by_id(body_id, only='cable_tv')
				b.cable_tv = True
				b.save(force_update=True)

			elif value == 'false':
				b = RoomsBodies.by_id(body_id, only='cable_tv')
				b.cable_tv = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid cab tv value.')


		# boolean
		elif prefix == 'garage':
			if value == 'true':
				b = RoomsBodies.by_id(body_id, only='garage')
				b.garage = True
				b.save(force_update=True)

			elif value == 'false':
				b = RoomsBodies.by_id(body_id, only='garage')
				b.garage = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid garage value.')


		# boolean
		elif prefix == 'playground':
			if value == 'true':
				b = RoomsBodies.by_id(body_id, only='playground')
				b.playground = True
				b.save(force_update=True)

			elif value == 'false':
				b = RoomsBodies.by_id(body_id, only='playground')
				b.playground = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid playground value.')


		# text
		elif prefix == 'add_buildings':
			b = RoomsBodies.by_id(body_id, only='add_buildings')
			if not value:
				b.add_buildings= None
				b.save(force_update=True)

			else:
				# ... форматування тут ...
				b.add_buildings = value
				b.save(force_update=True)
				return value


		# boolean
		elif prefix == 'kindergarten':
			if value == 'true':
				b = RoomsBodies.by_id(body_id, only='kindergarten')
				b.kindergarten = True
				b.save(force_update=True)

			elif value == 'false':
				b = RoomsBodies.by_id(body_id, only='kindergarten')
				b.kindergarten = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid kindergarten value.')


		# boolean
		elif prefix == 'school':
			if value == 'true':
				b = RoomsBodies.by_id(body_id, only='school')
				b.school = True
				b.save(force_update=True)

			elif value == 'false':
				b = RoomsBodies.by_id(body_id, only='school')
				b.school = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid school value.')


		# boolean
		elif prefix == 'market':
			if value == 'true':
				b = RoomsBodies.by_id(body_id, only='market')
				b.market = True
				b.save(force_update=True)

			elif value == 'false':
				b = RoomsBodies.by_id(body_id, only='market')
				b.market = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid market value.')


		# boolean
		elif prefix == 'transport_stop':
			if value == 'true':
				b = RoomsBodies.by_id(body_id, only='transport_stop')
				b.transport_stop = True
				b.save(force_update=True)

			elif value == 'false':
				b = RoomsBodies.by_id(body_id, only='transport_stop')
				b.transport_stop = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid transport_stop value.')


		# boolean
		elif prefix == 'entertainment':
			if value == 'true':
				b = RoomsBodies.by_id(body_id, only='entertainment')
				b.entertainment = True
				b.save(force_update=True)

			elif value == 'false':
				b = RoomsBodies.by_id(body_id, only='entertainment')
				b.entertainment = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid entertainment value.')


		# boolean
		elif prefix == 'sport_center':
			if value == 'true':
				b = RoomsBodies.by_id(body_id, only='sport_center')
				b.sport_center = True
				b.save(force_update=True)

			elif value == 'false':
				b = RoomsBodies.by_id(body_id, only='sport_center')
				b.sport_center = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid sport_center value.')


		# boolean
		elif prefix == 'park':
			if value == 'true':
				b = RoomsBodies.by_id(body_id, only='park')
				b.park = True
				b.save(force_update=True)

			elif value == 'false':
				b = RoomsBodies.by_id(body_id, only='park')
				b.park = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid park value.')


		# boolean
		elif prefix == 'water':
			if value == 'true':
				b = RoomsBodies.by_id(body_id, only='water')
				b.water = True
				b.save(force_update=True)

			elif value == 'false':
				b = RoomsBodies.by_id(body_id, only='water')
				b.water = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid water value.')


		# boolean
		elif prefix == 'wood':
			if value == 'true':
				b = RoomsBodies.by_id(body_id, only='wood')
				b.wood = True
				b.save(force_update=True)

			elif value == 'false':
				b = RoomsBodies.by_id(body_id, only='wood')
				b.wood = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid wood value.')


		# boolean
		elif prefix == 'sea':
			if value == 'true':
				b = RoomsBodies.by_id(body_id, only='sea')
				b.sea = True
				b.save(force_update=True)

			elif value == 'false':
				b = RoomsBodies.by_id(body_id, only='sea')
				b.sea = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid sea value.')


		# text
		elif prefix == 'add_showplaces':
			b = RoomsBodies.by_id(body_id, only='add_showplaces')
			if not value:
				b.add_showplaces= None
				b.save(force_update=True)

			else:
				# ... форматування тут ...
				b.add_showplaces = value
				b.save(force_update=True)
				return value

		# ...
		# other fields here
		# ...

		else:
			raise ValueError('invalid @prefix')

	except (DatabaseError, IntegrityError, ValueError):
		raise ValueError('Object type: apartments. Prefix: {prefix}. Value = {value}'.format(
			prefix = unicode(prefix), value = unicode(value)
		))