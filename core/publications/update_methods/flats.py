#coding=utf-8
from django.db import DatabaseError, IntegrityError
from collective.methods.formatters import format_text, format_title
from core.publications.constants import MARKET_TYPES, FLOOR_TYPES, OBJECT_CONDITIONS, HEATING_TYPES, INDIVIDUAL_HEATING_TYPES, CURRENCIES, LIVING_RENT_PERIODS, SALE_TRANSACTION_TYPES
from core.publications.models import FlatsHeads, FlatsBodies, FlatsRentTerms
from core.publications.objects_constants.flats import FLAT_BUILDING_TYPES, FLAT_ROOMS_PLANNINGS, FLAT_TYPES


# Оновлює інформацію про квартиру.
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
def update_flat(prefix, value, head_id=None, body_id=None, rent_id=None):
	try:
		# bool
		if prefix == 'for_sale':
			if value == 'true':
				h = FlatsHeads.by_id(head_id, only='for_sale')
				h.for_sale = True
				h.save(force_update=True)

			elif value == 'false':
				h = FlatsHeads.by_id(head_id, only='for_sale')
				h.for_sale = False
				h.save(force_update=True)

			else:
				raise ValueError()


		# bool
		elif prefix == 'for_rent':
			if value == 'true':
				h = FlatsHeads.by_id(head_id, only='for_rent')
				h.for_rent = True
				h.save(force_update=True)

			elif value == 'false':
				h = FlatsHeads.by_id(head_id, only='for_rent')
				h.for_rent = False
				h.save(force_update=True)

			else:
				raise ValueError()


		# blank or decimal
		elif prefix == 'price':
			if not value:
				b = FlatsBodies.by_id(body_id, only='price')
				b.price = None
				b.save(force_update=True)

			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError()


				b = FlatsBodies.by_id(body_id, only='price')
				b.price = value
				b.save(force_update=True)

				if int(value) == value:
					# Якщо після коми лише нулі - повернути ціле значення
					return "%.0f" % value
				else:
					# Інакше - округлити до 2х знаків після коми
					return "%.2f" % value


		# sid
		elif prefix == 's_trans_type':
			value = int(value)
			if value not in SALE_TRANSACTION_TYPES.values():
				raise ValueError()

			b = FlatsBodies.by_id(body_id, only='transaction_type_sid')
			b.transaction_type_sid = value
			b.save(force_update=True)


		# sid
		elif prefix == 'currency':
			value = int(value)
			if value not in CURRENCIES.values():
				raise ValueError()

			b = FlatsBodies.by_id(body_id, only='currency_sid')
			b.currency_sid = value
			b.save(force_update=True)


		# bool
		elif prefix == 'price_contract':
			if value == 'true':
				b = FlatsBodies.by_id(body_id, only='price_is_contract')
				b.price_is_contract = True
				b.save(force_update=True)

			elif value == 'false':
				b = FlatsBodies.by_id(body_id, only='price_is_contract')
				b.price_is_contract = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# text
		elif prefix == 'sale_add_terms':
			b = FlatsBodies.by_id(body_id, only='add_terms')
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
				raise ValueError()

			r = FlatsRentTerms.by_id(rent_id, only='period_sid')
			r.period_sid = value
			r.save(force_update=True)


		# blank or int
		elif prefix == 'rent_persons_count':
			if not value:
				r = FlatsRentTerms.by_id(rent_id, only='persons_count')
				r.persons_count = None
				r.save(force_update=True)

			else:
				value = int(value)
				if value <= 0:
					raise ValueError()

				r = FlatsRentTerms.by_id(rent_id, only='persons_count')
				r.persons_count = int(value)
				r.save(force_update=True)


		# blank or decimal
		elif prefix == 'rent_price':
			if not value:
				r = FlatsRentTerms.by_id(rent_id, only='price')
				r.price = None
				r.save(force_update=True)

			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError()

				r = FlatsRentTerms.by_id(rent_id, only='price')
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
				raise ValueError()

			r = FlatsRentTerms.by_id(rent_id, only='currency_sid')
			r.currency_sid = value
			r.save(force_update=True)
			return


		# boolean
		elif prefix == 'rent_price_contract':
			if value == 'true':
				r = FlatsRentTerms.by_id(rent_id, only='price_is_contract')
				r.price_is_contract = True
				r.save(force_update=True)

			elif value == 'false':
				r = FlatsRentTerms.by_id(rent_id, only='price_is_contract')
				r.price_is_contract = False
				r.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'rent_for_family':
			if value == 'true':
				r = FlatsRentTerms.by_id(rent_id, only='family')
				r.family = True
				r.save(force_update=True)

			elif value == 'false':
				r = FlatsRentTerms.by_id(rent_id, only='family')
				r.family = False
				r.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'rent_smoking':
			if value == 'true':
				r = FlatsRentTerms.by_id(rent_id, only='smoking')
				r.smoking = True
				r.save(force_update=True)

			elif value == 'false':
				r = FlatsRentTerms.by_id(rent_id, only='smoking')
				r.smoking = False
				r.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'rent_foreigners':
			if value == 'true':
				r = FlatsRentTerms.by_id(rent_id, only='foreigners')
				r.foreigners = True
				r.save(force_update=True)

			elif value == 'false':
				r = FlatsRentTerms.by_id(rent_id, only='foreigners')
				r.foreigners = False
				r.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'rent_pets':
			if value == 'true':
				r = FlatsRentTerms.by_id(rent_id, only='pets')
				r.pets = True
				r.save(force_update=True)

			elif value == 'false':
				r = FlatsRentTerms.by_id(rent_id, only='pets')
				r.pets = False
				r.save(force_update=True)

			else:
				raise ValueError()


		# text
		elif prefix == 'rent_add_terms':
			r = FlatsRentTerms.by_id(rent_id, only='add_terms')
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
			h = FlatsHeads.by_id(head_id, only='title')
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
			h = FlatsHeads.by_id(head_id, only='descr')
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
				raise ValueError()

			b = FlatsBodies.by_id(body_id, only='market_type_sid')
			b.market_type_sid = value
			b.save(force_update=True)


		# sid
		elif prefix == 'building_type':
			value = int(value)
			if value not in FLAT_BUILDING_TYPES.values():
				raise ValueError()

			b = FlatsBodies.by_id(body_id, only='building_type_sid')
			b.building_type_sid = value
			b.save(force_update=True)


		# text
		elif prefix == 'custom_building_type':
			b = FlatsBodies.by_id(body_id, only='custom_building_type')
			if not value:
				b.custom_building_type = None
				b.save(force_update=True)

			else:
				# fixme: додати форматування
				b.custom_building_type = value
				b.save(force_update=True)
				return value


		# blank or int
		elif prefix == 'build_year':
			if not value:
				b = FlatsBodies.by_id(body_id, only='build_year')
				b.build_year = None
				b.save(force_update=True)

			else:
				value = int(value)
				if value <= 0:
					raise ValueError()

				b = FlatsBodies.by_id(body_id, only='build_year')
				b.build_year = value
				b.save(force_update=True)


		# sid
		elif prefix == 'flat_type':
			value = int(value)
			if value not in FLAT_TYPES.values():
				raise ValueError()

			b = FlatsBodies.by_id(body_id, only='flat_type_sid')
			b.flat_type_sid = value
			b.save(force_update=True)


		# text
		elif prefix == 'custom_flat_type':
			b = FlatsBodies.by_id(body_id, only='custom_flat_type')
			if not value:
				b.custom_flat_type = None
				b.save(force_update=True)

			else:
				# fixme: додати форматування
				b.custom_flat_type = value
				b.save(force_update=True)
				return value


		# sid
		elif prefix == 'rooms_planing':
			value = int(value)
			if value not in FLAT_ROOMS_PLANNINGS.values():
				raise ValueError()

			b = FlatsBodies.by_id(body_id, only='rooms_planing_sid')
			b.rooms_planing_sid = value
			b.save(force_update=True)


		# sid
		elif prefix == 'condition':
			value = int(value)
			if value not in OBJECT_CONDITIONS.values():
				raise ValueError()

			b = FlatsBodies.by_id(body_id, only='condition_sid')
			b.condition_sid = value
			b.save(force_update=True)


		# blank or int
		elif prefix == 'floor':
			if not value:
				b = FlatsBodies.by_id(body_id, only='floor')
				b.floor = None
				b.save(force_update=True)

			else:
				value = int(value)
				b = FlatsBodies.by_id(body_id, only='floor')
				b.floor = value
				b.save(force_update=True)


		# sid
		elif prefix == 'floor_type':
			value = int(value)
			if value not in FLOOR_TYPES.values():
				raise ValueError()

			b = FlatsBodies.by_id(body_id, only='floor_type_sid')
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
				b = FlatsBodies.by_id(body_id, only='floors_count')
				b.floors_count = None
				b.save(force_update=True)
				return

			else:
				value = int(value)
				if value <= 0:
					raise ValueError()

				b = FlatsBodies.by_id(body_id, only='floors_count')
				b.floors_count = int(value)
				b.save(force_update=True)


		# blank or float
		elif prefix == 'total_area':
			if not value:
				b = FlatsBodies.by_id(body_id, only='total_area')
				b.total_area = None
				b.save(force_update=True)

			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError()

				b = FlatsBodies.by_id(body_id, only='total_area')
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
				b = FlatsBodies.by_id(body_id, only='living_area')
				b.living_area = None
				b.save(force_update=True)

			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError()

				b = FlatsBodies.by_id(body_id, only='living_area')
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
				b = FlatsBodies.by_id(body_id, only='kitchen_area')
				b.kitchen_area = None
				b.save(force_update=True)

			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError()

				b = FlatsBodies.by_id(body_id, only='kitchen_area')
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
				b = FlatsBodies.by_id(body_id, only='rooms_count')
				b.rooms_count = None
				b.save(force_update=True)

			else:
				value = int(value)
				b = FlatsBodies.by_id(body_id, only='rooms_count')
				b.rooms_count = value
				b.save(force_update=True)


		# blank or int
		elif prefix == 'bedrooms_count':
			if not value:
				b = FlatsBodies.by_id(body_id, only='bedrooms_count')
				b.bedrooms_count = None
				b.save(force_update=True)

			else:
				value = int(value)
				if value < 0:
					raise ValueError()

				b = FlatsBodies.by_id(body_id, only='bedrooms_count')
				b.bedrooms_count = value
				b.save(force_update=True)


		# blank or int
		elif prefix == 'vcs_count':
			if not value:
				b = FlatsBodies.by_id(body_id, only='vcs_count')
				b.vcs_count = None
				b.save(force_update=True)

			else:
				value = int(value)
				if value < 0:
					raise ValueError()

				b = FlatsBodies.by_id(body_id, only='vcs_count')
				b.vcs_count = value
				b.save(force_update=True)


		# blank or int
		elif prefix == 'balconies_count':
			if not value:
				b = FlatsBodies.by_id(body_id, only='balconies_count')
				b.balconies_count = None
				b.save(force_update=True)

			else:
				value = int(value)
				if value < 0:
					raise ValueError()

				b = FlatsBodies.by_id(body_id, only='balconies_count')
				b.balconies_count = value
				b.save(force_update=True)


		# blank or int
		elif prefix == 'loggias_count':
			if not value:
				b = FlatsBodies.by_id(body_id, only='loggias_count')
				b.loggias_count = None
				b.save(force_update=True)

			else:
				value = int(value)
				if value < 0:
					raise ValueError()

				b = FlatsBodies.by_id(body_id, only='loggias_count')
				b.loggias_count = value
				b.save(force_update=True)


		# blank or float
		elif prefix == 'ceiling_height':
			if not value:
				b = FlatsBodies.by_id(body_id, only='ceiling_height')
				b.ceiling_height = None
				b.save(force_update=True)

			else:
				value = round(float(value.replace(',', '.')), 2)

				if value <= 0:
					raise ValueError()

				b = FlatsBodies.by_id(body_id, only='ceiling_height')
				b.ceiling_height = value
				b.save(force_update=True)

				if int(value) == value:
					# Відсікти дробову частину, якщо після коми нулі
					return int(value)
				else:
					# скоротити / розширити до 2х цифр після коми
					return "%.2f" % value


		# sid
		elif prefix == 'heating_type':
			value = int(value)
			if value not in HEATING_TYPES.values():
				raise ValueError()

			b = FlatsBodies.by_id(body_id, only='heating_type_sid')
			b.heating_type_sid = value
			b.save(force_update=True)


		# text
		elif prefix == 'custom_heating_type':
			b = FlatsBodies.by_id(body_id, only='custom_heating_type')
			if not value:
				b.custom_heating_type = None
				b.save(force_update=True)

			else:
				# fixme: додати форматування
				b.custom_heating_type = value
				b.save(force_update=True)
				return value


		# sid
		elif prefix == 'ind_heating_type':
			value = int(value)
			if value not in INDIVIDUAL_HEATING_TYPES.values():
				raise ValueError()

			b = FlatsBodies.by_id(body_id, only='ind_heating_type_sid')
			b.ind_heating_type_sid = value
			b.save(force_update=True)


		# text
		elif prefix == 'custom_ind_heating_type':
			b = FlatsBodies.by_id(body_id, only='custom_ind_heating_type')
			if not value:
				b.custom_ind_heating_type = None
				b.save(force_update=True)

			else:
				# fixme: додати форматування
				b.custom_ind_heating_type = value
				b.save(force_update=True)
				return value


		# boolean
		elif prefix == 'electricity':
			if value == 'true':
				b = FlatsBodies.by_id(body_id, only='electricity')
				b.electricity = True
				b.save(force_update=True)

			elif value == 'false':
				b = FlatsBodies.by_id(body_id, only='electricity')
				b.electricity = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'gas':
			if value == 'true':
				b = FlatsBodies.by_id(body_id, only='gas')
				b.gas = True
				b.save(force_update=True)

			elif value == 'false':
				b = FlatsBodies.by_id(body_id, only='gas')
				b.gas = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'security_alarm':
			if value == 'true':
				b = FlatsBodies.by_id(body_id, only='security_alarm')
				b.security_alarm = True
				b.save(force_update=True)

			elif value == 'false':
				b = FlatsBodies.by_id(body_id, only='security_alarm')
				b.security_alarm = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid security alarm value')


		# boolean
		elif prefix == 'fire_alarm':
			if value == 'true':
				b = FlatsBodies.by_id(body_id, only='fire_alarm')
				b.fire_alarm = True
				b.save(force_update=True)

			elif value == 'false':
				b = FlatsBodies.by_id(body_id, only='fire_alarm')
				b.fire_alarm = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'hot_water':
			if value == 'true':
				b = FlatsBodies.by_id(body_id, only='hot_water')
				b.hot_water = True
				b.save(force_update=True)

			elif value == 'false':
				b = FlatsBodies.by_id(body_id, only='hot_water')
				b.hot_water = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'cold_water':
			if value == 'true':
				b = FlatsBodies.by_id(body_id, only='cold_water')
				b.cold_water = True
				b.save(force_update=True)

			elif value == 'false':
				b = FlatsBodies.by_id(body_id, only='cold_water')
				b.cold_water = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'lift':
			if value == 'true':
				b = FlatsBodies.by_id(body_id, only='lift')
				b.lift = True
				b.save(force_update=True)

			elif value == 'false':
				b = FlatsBodies.by_id(body_id, only='lift')
				b.lift = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'furniture':
			if value == 'true':
				r = FlatsRentTerms.by_id(rent_id, only='furniture')
				r.furniture = True
				r.save(force_update=True)

			elif value == 'false':
				r = FlatsRentTerms.by_id(rent_id, only='furniture')
				r.furniture = False
				r.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'washing_machine':
			if value == 'true':
				r = FlatsRentTerms.by_id(rent_id, only='washing_machine')
				r.washing_machine = True
				r.save(force_update=True)

			elif value == 'false':
				r = FlatsRentTerms.by_id(rent_id, only='washing_machine')
				r.washing_machine = False
				r.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'refrigerator':
			if value == 'true':
				r = FlatsRentTerms.by_id(rent_id, only='refrigerator')
				r.refrigerator = True
				r.save(force_update=True)

			elif value == 'false':
				r = FlatsRentTerms.by_id(rent_id, only='refrigerator')
				r.refrigerator = False
				r.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'conditioner':
			if value == 'true':
				r = FlatsRentTerms.by_id(rent_id, only='conditioner')
				r.conditioner = True
				r.save(force_update=True)

			elif value == 'false':
				r = FlatsRentTerms.by_id(rent_id, only='conditioner')
				r.conditioner = False
				r.save(force_update=True)

			else:
				raise ValueError('Invalid conditioner value')


		# boolean
		elif prefix == 'tv':
			if value == 'true':
				r = FlatsRentTerms.by_id(rent_id, only='tv')
				r.tv = True
				r.save(force_update=True)

			elif value == 'false':
				r = FlatsRentTerms.by_id(rent_id, only='tv')
				r.tv = False
				r.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'home_theater':
			if value == 'true':
				r = FlatsRentTerms.by_id(rent_id, only='home_theater')
				r.home_theater = True
				r.save(force_update=True)

			elif value == 'false':
				r = FlatsRentTerms.by_id(rent_id, only='home_theater')
				r.home_theater = False
				r.save(force_update=True)

			else:
				raise ValueError()


		# text
		elif prefix == 'add_facilities':
			b = FlatsBodies.by_id(body_id, only='add_facilities')
			if not value:
				b.add_facilities = None
				b.save(force_update=True)

			else:
				# fixme: додати форматування
				b.add_facilities = value
				b.save(force_update=True)
				return value


		# boolean
		elif prefix == 'phone':
			if value == 'true':
				b = FlatsBodies.by_id(body_id, only='phone')
				b.phone = True
				b.save(force_update=True)

			elif value == 'false':
				b = FlatsBodies.by_id(body_id, only='phone')
				b.phone = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'mobile_coverage':
			if value == 'true':
				b = FlatsBodies.by_id(body_id, only='mobile_coverage')
				b.mobile_coverage = True
				b.save(force_update=True)

			elif value == 'false':
				b = FlatsBodies.by_id(body_id, only='mobile_coverage')
				b.mobile_coverage = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'internet':
			if value == 'true':
				b = FlatsBodies.by_id(body_id, only='internet')
				b.internet = True
				b.save(force_update=True)

			elif value == 'false':
				b = FlatsBodies.by_id(body_id, only='internet')
				b.internet = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'cab_tv':
			if value == 'true':
				b = FlatsBodies.by_id(body_id, only='cable_tv')
				b.cable_tv = True
				b.save(force_update=True)

			elif value == 'false':
				b = FlatsBodies.by_id(body_id, only='cable_tv')
				b.cable_tv = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'garage':
			if value == 'true':
				b = FlatsBodies.by_id(body_id, only='garage')
				b.garage = True
				b.save(force_update=True)

			elif value == 'false':
				b = FlatsBodies.by_id(body_id, only='garage')
				b.garage = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'playground':
			if value == 'true':
				b = FlatsBodies.by_id(body_id, only='playground')
				b.playground = True
				b.save(force_update=True)

			elif value == 'false':
				b = FlatsBodies.by_id(body_id, only='playground')
				b.playground = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# text
		elif prefix == 'add_buildings':
			b = FlatsBodies.by_id(body_id, only='add_buildings')
			if not value:
				b.add_buildings= None
				b.save(force_update=True)

			else:
				# fixme: додати форматування
				b.add_buildings = value
				b.save(force_update=True)
				return value


		# boolean
		elif prefix == 'kindergarten':
			if value == 'true':
				b = FlatsBodies.by_id(body_id, only='kindergarten')
				b.kindergarten = True
				b.save(force_update=True)

			elif value == 'false':
				b = FlatsBodies.by_id(body_id, only='kindergarten')
				b.kindergarten = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'school':
			if value == 'true':
				b = FlatsBodies.by_id(body_id, only='school')
				b.school = True
				b.save(force_update=True)

			elif value == 'false':
				b = FlatsBodies.by_id(body_id, only='school')
				b.school = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'market':
			if value == 'true':
				b = FlatsBodies.by_id(body_id, only='market')
				b.market = True
				b.save(force_update=True)

			elif value == 'false':
				b = FlatsBodies.by_id(body_id, only='market')
				b.market = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'transport_stop':
			if value == 'true':
				b = FlatsBodies.by_id(body_id, only='transport_stop')
				b.transport_stop = True
				b.save(force_update=True)

			elif value == 'false':
				b = FlatsBodies.by_id(body_id, only='transport_stop')
				b.transport_stop = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'entertainment':
			if value == 'true':
				b = FlatsBodies.by_id(body_id, only='entertainment')
				b.entertainment = True
				b.save(force_update=True)

			elif value == 'false':
				b = FlatsBodies.by_id(body_id, only='entertainment')
				b.entertainment = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'sport_center':
			if value == 'true':
				b = FlatsBodies.by_id(body_id, only='sport_center')
				b.sport_center = True
				b.save(force_update=True)

			elif value == 'false':
				b = FlatsBodies.by_id(body_id, only='sport_center')
				b.sport_center = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'park':
			if value == 'true':
				b = FlatsBodies.by_id(body_id, only='park')
				b.park = True
				b.save(force_update=True)

			elif value == 'false':
				b = FlatsBodies.by_id(body_id, only='park')
				b.park = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'water':
			if value == 'true':
				b = FlatsBodies.by_id(body_id, only='water')
				b.water = True
				b.save(force_update=True)

			elif value == 'false':
				b = FlatsBodies.by_id(body_id, only='water')
				b.water = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'wood':
			if value == 'true':
				b = FlatsBodies.by_id(body_id, only='wood')
				b.wood = True
				b.save(force_update=True)

			elif value == 'false':
				b = FlatsBodies.by_id(body_id, only='wood')
				b.wood = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'sea':
			if value == 'true':
				b = FlatsBodies.by_id(body_id, only='sea')
				b.sea = True
				b.save(force_update=True)

			elif value == 'false':
				b = FlatsBodies.by_id(body_id, only='sea')
				b.sea = False
				b.save(force_update=True)

			else:
				raise ValueError('')


		# text
		elif prefix == 'add_showplaces':
			b = FlatsBodies.by_id(body_id, only='add_showplaces')
			if not value:
				b.add_showplaces= None
				b.save(force_update=True)

			else:
				# fixme: додати форматування
				b.add_showplaces = value
				b.save(force_update=True)
				return value

		# ...
		# other fields here
		# ...

		else:
			raise ValueError()

	except (DatabaseError, IntegrityError, ValueError):
		raise ValueError('Object type: flat. Prefix: {prefix}. Value = {value}'.format(
			prefix = unicode(prefix), value = unicode(value)
		))