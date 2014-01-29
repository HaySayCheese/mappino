#coding=utf-8
from django.db import DatabaseError, IntegrityError
from collective.methods.formatters import format_text, format_title
from core.publications.constants import HEATING_TYPES, INDIVIDUAL_HEATING_TYPES, FLOOR_TYPES, OBJECT_CONDITIONS, MARKET_TYPES, CURRENCIES, COMMERCIAL_RENT_PERIODS, SALE_TRANSACTION_TYPES, RED_LINE_VALUES
from core.publications.models import CateringsHeads, CateringsBodies, CateringsRentTerms
from core.publications.objects_constants.trades import TRADE_BUILDING_TYPES

# Оновлює інформацію про об’єкт гром. харчування.
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

def update_catering(prefix, value, head_id=None, body_id=None, rent_id=None):
	try:
		# bool
		if prefix == 'for_sale':
			if value == 'true':
				h = CateringsHeads.by_id(head_id, head_id='for_sale')
				h.for_sale = True
				h.save(force_update=True)

			elif value == 'false':
				h = CateringsHeads.by_id(head_id, head_id='for_sale')
				h.for_sale = False
				h.save(force_update=True)

			else:
				raise ValueError()


		# bool
		elif prefix == 'for_rent':
			if value == 'true':
				h = CateringsHeads.by_id(head_id, head_id='for_rent')
				h.for_rent = True
				h.save(force_update=True)

			elif value == 'false':
				h = CateringsHeads.by_id(head_id, head_id='for_rent')
				h.for_rent = False
				h.save(force_update=True)

			else:
				raise ValueError()


		# sid
		elif prefix == 'red_line':
			value = int(value)
			if value not in RED_LINE_VALUES.values():
				raise ValueError()

			b = CateringsHeads.by_id(body_id, head_id='red_line')
			b.red_line = value
			b.save(force_update=True)


		# blank or decimal
		elif prefix == 'price':
			if not value:
				b = CateringsBodies.by_id(body_id, only='price')
				b.price = None
				b.save(force_update=True)

			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError()

				b = CateringsBodies.by_id(body_id, only='price')
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
				raise ValueError()

			b = CateringsBodies.by_id(body_id, only='transaction_type_sid')
			b.transaction_type_sid = value
			b.save(force_update=True)


		# sid
		elif prefix == 'currency':
			value = int(value)
			if value not in CURRENCIES.values():
				raise ValueError()

			b = CateringsBodies.by_id(body_id, only='currency_sid')
			b.currency_sid = value
			b.save(force_update=True)


		# bool
		elif prefix == 'price_contract':
			if value == 'true':
				b = CateringsBodies.by_id(body_id, only='price_is_contract')
				b.price_is_contract = True
				b.save(force_update=True)

			elif value == 'false':
				b = CateringsBodies.by_id(body_id, only='price_is_contract')
				b.price_is_contract = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# text
		elif prefix == 'sale_add_terms':
			b = CateringsBodies.by_id(body_id, only='add_terms')
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
			if value not in COMMERCIAL_RENT_PERIODS.values():
				raise ValueError()

			r = CateringsRentTerms.by_id(rent_id, only='period_sid')
			r.period_sid = value
			r.save(force_update=True)


		# blank or decimal
		elif prefix == 'rent_price':
			if not value:
				r = CateringsRentTerms.by_id(rent_id, only='price')
				r.price = None
				r.save(force_update=True)

			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError()

				r = CateringsRentTerms.by_id(rent_id, only='price')
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

			r = CateringsRentTerms.by_id(rent_id, only='currency_sid')
			r.currency_sid = value
			r.save(force_update=True)
			return


		# boolean
		elif prefix == 'rent_price_contract':
			if value == 'true':
				r = CateringsRentTerms.by_id(rent_id, only='price_is_contract')
				r.price_is_contract = True
				r.save(force_update=True)

			elif value == 'false':
				r = CateringsRentTerms.by_id(rent_id, only='price_is_contract')
				r.price_is_contract = False
				r.save(force_update=True)

			else:
				raise ValueError()


		# text
		elif prefix == 'rent_add_terms':
			r = CateringsRentTerms.by_id(rent_id, only='add_terms')
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
			h = CateringsHeads.by_id(head_id, head_id='title')
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
			h = CateringsHeads.by_id(head_id, head_id='descr')
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

			b = CateringsBodies.by_id(body_id, only='market_type_sid')
			b.market_type_sid = value
			b.save(force_update=True)


		# sid
		elif prefix == 'building_type':
			value = int(value)
			if value not in TRADE_BUILDING_TYPES.values():
				raise ValueError()

			b = CateringsBodies.by_id(body_id, only='building_type_sid')
			b.building_type_sid = value
			b.save(force_update=True)
			return


		# blank or int
		elif prefix == 'build_year':
			if not value:
				b = CateringsBodies.by_id(body_id, only='build_year')
				b.build_year = None
				b.save(force_update=True)

			else:
				value = int(value)
				b = CateringsBodies.by_id(body_id, only='build_year')
				b.build_year = value
				b.save(force_update=True)


		# sid
		elif prefix == 'condition':
			value = int(value)
			if value not in OBJECT_CONDITIONS.values():
				raise ValueError()

			b = CateringsBodies.by_id(body_id, only='condition_sid')
			b.condition_sid = value
			b.save(force_update=True)


		# blank or int
		elif prefix == 'floor':
			if not value:
				b = CateringsBodies.by_id(body_id, only='floor')
				b.floor = None
				b.save(force_update=True)

			else:
				value = int(value)
				b = CateringsBodies.by_id(body_id, only='floor')
				b.floor = value
				b.save(force_update=True)


		# sid
		elif prefix == 'floor_type':
			value = int(value)
			if value not in FLOOR_TYPES.values():
				raise ValueError()

			b = CateringsBodies.by_id(body_id, only='floor_type_sid')
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
				b = CateringsBodies.by_id(body_id, only='floors_count')
				b.floors_count = None
				b.save(force_update=True)
				return

			else:
				value = int(value)
				if value <= 0:
					raise ValueError()

				b = CateringsBodies.by_id(body_id, only='floors_count')
				b.floors_count = int(value)
				b.save(force_update=True)


		# boolean
		elif prefix == 'mansard':
			if value == 'true':
				b = CateringsBodies.by_id(body_id, only='mansard')
				b.mansard = True
				b.save(force_update=True)

			elif value == 'false':
				b = CateringsBodies.by_id(body_id, only='mansard')
				b.mansard = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'ground':
			if value == 'true':
				b = CateringsBodies.by_id(body_id, only='ground')
				b.ground = True
				b.save(force_update=True)

			elif value == 'false':
				b = CateringsBodies.by_id(body_id, only='ground')
				b.ground = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'lower_floor':
			if value == 'true':
				b = CateringsBodies.by_id(body_id, only='lower_floor')
				b.lower_floor = True
				b.save(force_update=True)

			elif value == 'false':
				b = CateringsBodies.by_id(body_id, only='lower_floor')
				b.lower_floor = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# blank or int
		elif prefix == 'halls_count':
			if not value:
				b = CateringsBodies.by_id(body_id, only='halls_count')
				b.halls_count = None
				b.save(force_update=True)

			else:
				value = int(value)
				if value < 0:
					raise ValueError()

				b = CateringsBodies.by_id(body_id, only='halls_count')
				b.halls_count = value
				b.save(force_update=True)


		# blank or float
		elif prefix == 'halls_area':
			if not value:
				b = CateringsBodies.by_id(body_id, only='halls_area')
				b.halls_area = None
				b.save(force_update=True)

			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError()

				b = CateringsBodies.by_id(body_id, only='halls_area')
				b.halls_area = value
				b.save(force_update=True)

				if int(value) == value:
					# Відсікти дробову частину, якщо після коми нулі
					return "%.0f" % value
				else:
					# Скоротити / розширити до 2х цифр після коми
					return "%.2f" % value


		# blank or float
		elif prefix == 'total_area':
			if not value:
				b = CateringsBodies.by_id(body_id, only='total_area')
				b.total_area = None
				b.save(force_update=True)

			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError()

				b = CateringsBodies.by_id(body_id, only='total_area')
				b.total_area = value
				b.save(force_update=True)

				if int(value) == value:
					# Відсікти дробову частину, якщо після коми нулі
					return "%.0f" % value
				else:
					# Скоротити / розширити до 2х цифр після коми
					return "%.2f" % value


		# boolean
		elif prefix == 'closed_area':
			if value == 'true':
				b = CateringsBodies.by_id(body_id, only='closed_area')
				b.closed_area = True
				b.save(force_update=True)

			elif value == 'false':
				b = CateringsBodies.by_id(body_id, only='closed_area')
				b.closed_area = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# blank or int
		elif prefix == 'vcs_count':
			if not value:
				b = CateringsBodies.by_id(body_id, only='vcs_count')
				b.vcs_count = None
				b.save(force_update=True)

			else:
				value = int(value)
				if value < 0:
					raise ValueError()

				b = CateringsBodies.by_id(body_id, only='vcs_count')
				b.vcs_count = value
				b.save(force_update=True)


		# blank or float
		elif prefix == 'ceiling_height':
			if not value:
				b = CateringsBodies.by_id(body_id, only='ceiling_height')
				b.ceiling_height = None
				b.save(force_update=True)

			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError()

				b = CateringsBodies.by_id(body_id, only='ceiling_height')
				b.ceiling_height = value
				b.save(force_update=True)

				if int(value) == value:
					# Відсікти дробову частину, якщо після коми нулі
					return "%.0f" % value
				else:
					# скоротити / розширити до 2х цифр після коми
					return "%.2f" % value


		# sid
		elif prefix == 'heating_type':
			value = int(value)
			if value not in HEATING_TYPES.values():
				raise ValueError()

			b = CateringsBodies.by_id(body_id, only='heating_type_sid')
			b.heating_type_sid = value
			b.save(force_update=True)


		# text
		elif prefix == 'custom_heating_type':
			b = CateringsBodies.by_id(body_id, only='custom_heating_type')
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

			b = CateringsBodies.by_id(body_id, only='ind_heating_type_sid')
			b.ind_heating_type_sid = value
			b.save(force_update=True)


		# text
		elif prefix == 'custom_ind_heating_type':
			b = CateringsBodies.by_id(body_id, only='custom_ind_heating_type')
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
				b = CateringsBodies.by_id(body_id, only='electricity')
				b.electricity = True
				b.save(force_update=True)

			elif value == 'false':
				b = CateringsBodies.by_id(body_id, only='electricity')
				b.electricity = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'gas':
			if value == 'true':
				b = CateringsBodies.by_id(body_id, only='gas')
				b.gas = True
				b.save(force_update=True)

			elif value == 'false':
				b = CateringsBodies.by_id(body_id, only='gas')
				b.gas = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'security_alarm':
			if value == 'true':
				b = CateringsBodies.by_id(body_id, only='security_alarm')
				b.security_alarm = True
				b.save(force_update=True)

			elif value == 'false':
				b = CateringsBodies.by_id(body_id, only='security_alarm')
				b.security_alarm = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'fire_alarm':
			if value == 'true':
				b = CateringsBodies.by_id(body_id, only='fire_alarm')
				b.fire_alarm = True
				b.save(force_update=True)

			elif value == 'false':
				b = CateringsBodies.by_id(body_id, only='fire_alarm')
				b.fire_alarm = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'hot_water':
			if value == 'true':
				b = CateringsBodies.by_id(body_id, only='hot_water')
				b.hot_water = True
				b.save(force_update=True)

			elif value == 'false':
				b = CateringsBodies.by_id(body_id, only='hot_water')
				b.hot_water = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'cold_water':
			if value == 'true':
				b = CateringsBodies.by_id(body_id, only='cold_water')
				b.cold_water = True
				b.save(force_update=True)

			elif value == 'false':
				b = CateringsBodies.by_id(body_id, only='cold_water')
				b.cold_water = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'canalisation':
			if value == 'true':
				b = CateringsBodies.by_id(body_id, only='canalisation')
				b.canalisation = True
				b.save(force_update=True)

			elif value == 'false':
				b = CateringsBodies.by_id(body_id, only='canalisation')
				b.canalisation = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'ventilation':
			if value == 'true':
				b = CateringsBodies.by_id(body_id, only='ventilation')
				b.ventilation = True
				b.save(force_update=True)

			elif value == 'false':
				b = CateringsBodies.by_id(body_id, only='ventilation')
				b.ventilation = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'security':
			if value == 'true':
				b = CateringsBodies.by_id(body_id, only='security')
				b.security = True
				b.save(force_update=True)

			elif value == 'false':
				b = CateringsBodies.by_id(body_id, only='security')
				b.security = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# text
		elif prefix == 'add_facilities':
			b = CateringsBodies.by_id(body_id, only='add_facilities')
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
				b = CateringsBodies.by_id(body_id, only='phone')
				b.phone = True
				b.save(force_update=True)

			elif value == 'false':
				b = CateringsBodies.by_id(body_id, only='phone')
				b.phone = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'mobile_coverage':
			if value == 'true':
				b = CateringsBodies.by_id(body_id, only='mobile_coverage')
				b.mobile_coverage = True
				b.save(force_update=True)

			elif value == 'false':
				b = CateringsBodies.by_id(body_id, only='mobile_coverage')
				b.mobile_coverage = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'internet':
			if value == 'true':
				b = CateringsBodies.by_id(body_id, only='internet')
				b.internet = True
				b.save(force_update=True)

			elif value == 'false':
				b = CateringsBodies.by_id(body_id, only='internet')
				b.internet = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'cab_tv':
			if value == 'true':
				b = CateringsBodies.by_id(body_id, only='cable_tv')
				b.cable_tv = True
				b.save(force_update=True)

			elif value == 'false':
				b = CateringsBodies.by_id(body_id, only='cable_tv')
				b.cable_tv = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'lan':
			if value == 'true':
				b = CateringsBodies.by_id(body_id, only='lan')
				b.lan = True
				b.save(force_update=True)

			elif value == 'false':
				b = CateringsBodies.by_id(body_id, only='lan')
				b.lan = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# blank or int
		elif prefix == 'tel_lines_count':
			if not value:
				b = CateringsBodies.by_id(body_id, only='phone_lines_count')
				b.phone_lines_count = None
				b.save(force_update=True)
				return

			else:
				value = int(value)
				if value <= 0:
					raise ValueError()

				b = CateringsBodies.by_id(body_id, only='phone_lines_count')
				b.phone_lines_count = int(value)
				b.save(force_update=True)


		# boolean
		elif prefix == 'parking':
			if value == 'true':
				b = CateringsBodies.by_id(body_id, only='parking')
				b.parking = True
				b.save(force_update=True)

			elif value == 'false':
				b = CateringsBodies.by_id(body_id, only='parking')
				b.parking = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'open_air':
			if value == 'true':
				b = CateringsBodies.by_id(body_id, only='open_air')
				b.open_air = True
				b.save(force_update=True)

			elif value == 'false':
				b = CateringsBodies.by_id(body_id, only='open_air')
				b.open_air = False
				b.save(force_update=True)

			else:
				raise ValueError()


		elif prefix == 'add_buildings':
			b = CateringsBodies.by_id(body_id, only='add_buildings')
			if not value:
				b.add_buildings= None
				b.save(force_update=True)

			else:
				# fixme: додати форматування
				b.add_buildings = value
				b.save(force_update=True)
				return value


		# boolean
		elif prefix == 'transport_stop':
			if value == 'true':
				b = CateringsBodies.by_id(body_id, only='transport_stop')
				b.transport_stop = True
				b.save(force_update=True)

			elif value == 'false':
				b = CateringsBodies.by_id(body_id, only='transport_stop')
				b.transport_stop = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'bank':
			if value == 'true':
				b = CateringsBodies.by_id(body_id, only='bank')
				b.bank = True
				b.save(force_update=True)

			elif value == 'false':
				b = CateringsBodies.by_id(body_id, only='bank')
				b.bank = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'market':
			if value == 'true':
				b = CateringsBodies.by_id(body_id, only='market')
				b.market = True
				b.save(force_update=True)

			elif value == 'false':
				b = CateringsBodies.by_id(body_id, only='market')
				b.market = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'cash_machine':
			if value == 'true':
				b = CateringsBodies.by_id(body_id, only='cash_machine')
				b.cash_machine = True
				b.save(force_update=True)

			elif value == 'false':
				b = CateringsBodies.by_id(body_id, only='cash_machine')
				b.cash_machine = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'cafe':
			if value == 'true':
				b = CateringsBodies.by_id(body_id, only='cafe')
				b.cafe = True
				b.save(force_update=True)

			elif value == 'false':
				b = CateringsBodies.by_id(body_id, only='cafe')
				b.cafe = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# boolean
		elif prefix == 'entertainment':
			if value == 'true':
				b = CateringsBodies.by_id(body_id, only='entertainment')
				b.entertainment = True
				b.save(force_update=True)

			elif value == 'false':
				b = CateringsBodies.by_id(body_id, only='entertainment')
				b.entertainment = False
				b.save(force_update=True)

			else:
				raise ValueError()


		# text
		elif prefix == 'add_showplaces':
			b = CateringsBodies.by_id(body_id, only='add_showplaces')
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
			raise ValueError('invalid @prefix')

	except (DatabaseError, IntegrityError, ValueError):
		raise ValueError('Object type: apartments. Prefix: {prefix}. Value = {value}'.format(
			prefix = unicode(prefix), value = unicode(value)
		))