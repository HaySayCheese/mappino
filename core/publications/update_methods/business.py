#coding=utf-8
from decimal import InvalidOperation
from django.db import DatabaseError, IntegrityError
from collective.exceptions import RecordDoesNotExists

from collective.methods.formatters import format_text, format_title
from core.dirtags import DirTags
from core.dirtags.models import PublicationAlreadyExists
from core.publications.constants import CURRENCIES, OBJECT_CONDITIONS, FLOOR_TYPES, HEATING_TYPES, INDIVIDUAL_HEATING_TYPES, COMMERCIAL_RENT_PERIODS, SALE_TRANSACTION_TYPES, RED_LINE_VALUES
from core.publications.models import BusinessesRentTerms, BusinessesBodies, BusinessesSaleTerms
from core.publications.objects_constants.trades import TRADE_BUILDING_TYPES



# Оновлює інформацію про готовий бізнес.
#
# Поле для оновлення відшукується за префіксом @field.
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

def update_business(h, field, value, tid):
	try:
		# bool
		if field == 'for_sale':
			if (value is True) or (value is False):
				h.for_sale = value
				h.save(force_update=True)
			else:
				raise ValueError()


		# blank or decimal
		elif field == 'sale_price':
			if not value:
				st = BusinessesSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
				st.price = None
				st.save(force_update=True)
				return
			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError()

				st = BusinessesSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
				st.price = value
				st.save(force_update=True)

				if int(value) == value:
					# Якщо після коми лише нулі - повернути ціле значення
					return "%.0f" % value
				else:
					# Інакше - округлити до 2х знаків після коми
					return "%.2f" % value


		# sid
		elif field == 'sale_transaction_sid':
			value = int(value)
			if value not in SALE_TRANSACTION_TYPES.values():
				raise ValueError()

			st = BusinessesSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
			st.transaction_sid = value
			st.save(force_update=True)
			return


		# sid
		elif field == 'sale_currency_sid':
			value = int(value)
			if value not in CURRENCIES.values():
				raise ValueError()

			st = BusinessesSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
			st.currency_sid = value
			st.save(force_update=True)
			return


		# bool
		elif field == 'sale_is_contract':
			if (value is True) or (value is False):
				st = BusinessesSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
				st.is_contract = value
				st.save(force_update=True)
				return
			else:
				raise ValueError()


		# text
		elif field == 'sale_add_terms':
			st = BusinessesSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
			if not value:
				st.add_terms = u''
				st.save(force_update=True)
				return
			else:
				value = format_text(value)
				st.add_terms = value
				st.save(force_update=True)
				return value


		# bool
		elif field == 'for_rent':
			if (value is True) or (value is False):
				h.for_rent = value
				h.save(force_update=True)
				return
			else:
				raise ValueError()


		# sid
		elif field == 'rent_period_sid':
			value = int(value)
			if value not in COMMERCIAL_RENT_PERIODS.values():
				raise ValueError()

			rt = BusinessesRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
			rt.period_sid = value
			rt.save(force_update=True)
			return


		# blank or decimal
		elif field == 'rent_price':
			if not value:
				rt = BusinessesRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
				rt.price = None
				rt.save(force_update=True)
				return
			else:
				value = round(float(value.replace(',','.')), 2)
				if value <= 0:
					raise ValueError()

				rt = BusinessesRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
				rt.price = value
				rt.save(force_update=True)

				if int(value) == value:
					# Якщо після коми лише нулі - повернути ціле значення
					return "%.0f" % value
				else:
					# Інакше - округлити до 2х знаків після коми
					return "%.2f" % value


		# sid
		elif field == 'rent_currency_sid':
			value = int(value)
			if value not in CURRENCIES.values():
				raise ValueError()

			rt = BusinessesRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
			rt.currency_sid = value
			rt.save(force_update=True)
			return


		# boolean
		elif field == 'rent_is_contract':
			if (value is True) or (value is False):
				rt = BusinessesRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
				rt.is_contract = value
				rt.save(force_update=True)
				return
			else:
				raise ValueError()


		# text
		elif field == 'rent_add_terms':
			rt = BusinessesRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
			if not value:
				rt.add_terms = u''
				rt.save(force_update=True)
				return
			else:
				value = format_text(value)
				rt.add_terms = value
				rt.save(force_update=True)
				return value


		# sid
		elif field == 'red_line_sid':
			value = int(value)
			if value not in RED_LINE_VALUES.values():
				raise ValueError()

			b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
			b.red_line = value
			b.save(force_update=True)
			return


		# text
		elif field == 'title':
			b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
			if not value:
				b.title = u''
				b.save(force_update=True)
				return
			else:
				value = format_title(value)
				b.title = value
				b.save(force_update=True)
				return value


		# text
		elif field == 'description':
			b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
			if not value:
				b.description = u''
				b.save(force_update=True)
				return
			else:
				value = format_text(value)
				b.description = value
				b.save(force_update=True)
				return value


		# blank or float
		elif field == 'age':
			if not value:
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.age = None
				b.save(force_update=True)
				return
			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError

				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.age = value
				b.save(force_update=True)

				if int(value) == value:
					# Відсікти дробову частину, якщо після коми нулі
					return "%.0f" % value


		# blank or int
		elif field == 'workers_count':
			if not value:
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.workers_count = None
				b.save(force_update=True)
				return
			else:
				value = int(value)
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.workers_count = value
				b.save(force_update=True)
				return


		# blank or decimal
		elif field == 'monthly_costs':
			if not value:
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.monthly_costs = None
				b.save(force_update=True)
				return
			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError

				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.monthly_costs = value
				b.save(force_update=True)

				if int(value) == float(value):
					# Якщо після коми лише нулі - повернути ціле значення
					return int(value)
				else:
					# Інакше - округлити до 2х знаків після коми
					return "%.2f" % float(value)


		# sid
		elif field == 'mc_currency_sid':
			value = int(value)
			if value not in CURRENCIES.values():
				raise ValueError

			b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
			b.mc_currency_sid = value
			b.save(force_update=True)
			return


		# blank or decimal
		elif field == 'annual_receipts':
			if not value:
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.annual_receipts = None
				b.save(force_update=True)
				return
			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError

				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.annual_receipts = value
				b.save(force_update=True)

				if int(value) == float(value):
					# Якщо після коми лише нулі - повернути ціле значення
					return "%.0f" % value
				else:
					# Інакше - округлити до 2х знаків після коми
					return "%.2f" % float(value)


		# sid
		elif field == 'ar_currency_sid':
			value = int(value)
			if value not in CURRENCIES.values():
				raise ValueError

			b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
			b.ar_currency_sid = value
			b.save(force_update=True)
			return


		# blank or decimal
		elif field == 'share':
			if not value:
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.share = None
				b.save(force_update=True)
				return
			else:
				# процент від бізнесу не можна округляти,
				# оскільки не відомо наскільки точною є градація акції в конкретному бізнесі
				value = float(value.replace(',', '.'))
				if value <= 0:
					raise ValueError
				if value > 100:
					value = 100

				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.share = value
				b.save(force_update=True)

				if int(value) == value:
					# Якщо після коми лише нулі - повернути ціле значення
					return "%.0f" % value


		# sid
		elif field == 'building_type_sid':
			value = int(value)
			if value not in TRADE_BUILDING_TYPES.values():
				raise ValueError

			b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
			b.building_type_sid = value
			b.save(force_update=True)
			return


		# blank or int
		elif field == 'build_year':
			if not value:
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.build_year = None
				b.save(force_update=True)
				return
			else:
				value = int(value)
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.build_year = value
				b.save(force_update=True)
				return


		# sid
		elif field == 'condition_sid':
			value = int(value)
			if value not in OBJECT_CONDITIONS.values():
				raise ValueError

			b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
			b.condition_sid = value
			b.save(force_update=True)
			return


		# blank or int
		elif field == 'floor':
			if not value:
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.floor = None
				b.save(force_update=True)
				return
			else:
				value = int(value)
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.floor = value
				b.save(force_update=True)
				return


		# sid
		elif field == 'floor_type_sid':
			value = int(value)
			if value not in FLOOR_TYPES.values():
				raise ValueError

			b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
			b.floor_type_sid = value

			# Якщо тип поверху "мансарда" або "цоколь", то ітак зрозуміло,
			# шо це або останній поверх, або нульовий/перший.
			# Немає необхідності зберігати додаткові дані.
			if value in [FLOOR_TYPES.mansard(), FLOOR_TYPES.ground()]:
				b.floor = None

			b.save(force_update=True)
			return


		# blank or int
		elif field == 'floors_count':
			if not value:
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.floors_count = None
				b.save(force_update=True)
				return
			else:
				value = int(value)
				if value <= 0:
					raise ValueError

				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.floors_count = int(value)
				b.save(force_update=True)
				return


		# boolean
		elif field == 'mansard':
			if (value is True) or (value is False):
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.mansard = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# boolean
		elif field == 'ground':
			if (value is True) or (value is False):
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.ground = value
				b.save(force_update=True)
			else:
				raise ValueError()


		# boolean
		elif field == 'lower_floor':
			if (value is True) or (value is False):
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.lower_floor = value
				b.save(force_update=True)
			else:
				raise ValueError()


		# blank or float
		elif field == 'halls_area':
			if not value:
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.halls_area = None
				b.save(force_update=True)
				return
			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError

				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.halls_area = value
				b.save(force_update=True)

				if int(value) == value:
					# Відсікти дробову частину, якщо після коми нулі
					return "%.0f" % value
				else:
					# Скоротити / розширити до 2х цифр після коми
					return "%.2f" % value


		# blank or float
		elif field == 'total_area':
			if not value:
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.total_area = None
				b.save(force_update=True)

			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError

				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.total_area = value
				b.save(force_update=True)

				if int(value) == value:
					# Відсікти дробову частину, якщо після коми нулі
					return "%.0f" % value
				else:
					# Скоротити / розширити до 2х цифр після коми
					return "%.2f" % value


		# boolean
		elif field == 'closed_area':
			if (value is True) or (value is False):
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.closed_area = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# blank or float
		elif field == 'plot_area':
			if not value:
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.plot_area = None
				b.save(force_update=True)
				return
			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError

				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.plot_area = value
				b.save(force_update=True)

				if int(value) == value:
					# Відсікти дробову частину, якщо після коми нулі
					return "%.0f" % value
				else:
					# Скоротити / розширити до 2х цифр після коми
					return "%.2f" % value


		# blank or int
		elif field == 'vcs_count':
			if not value:
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.vcs_count = None
				b.save(force_update=True)
				return
			else:
				value = int(value)
				if value < 0:
					raise ValueError

				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.vcs_count = value
				b.save(force_update=True)
				return


		# blank or float
		elif field == 'ceiling_height':
			if not value:
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.ceiling_height = None
				b.save(force_update=True)
				return
			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError

				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.ceiling_height = value
				b.save(force_update=True)

				if int(value) == value:
					# Відсікти дробову частину, якщо після коми нулі
					return "%.0f" % value
				else:
					# скоротити / розширити до 2х цифр після коми
					return "%.2f" % value


		# sid
		elif field == 'heating_type_sid':
			value = int(value)
			if value not in HEATING_TYPES.values():
				raise ValueError

			b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
			b.heating_type_sid = value
			b.save(force_update=True)
			return


		# text
		elif field == 'custom_heating_type':
			b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
			if not value:
				b.custom_heating_type = u''
				b.save(force_update=True)
				return
			else:
				# fixme: додати форматування
				b.custom_heating_type = value
				b.save(force_update=True)
				return


		# sid
		elif field == 'ind_heating_type_sid':
			value = int(value)
			if value not in INDIVIDUAL_HEATING_TYPES.values():
				raise ValueError()

			b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
			b.ind_heating_type_sid = value
			b.save(force_update=True)
			return


		# text
		elif field == 'custom_ind_heating_type':
			b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
			if not value:
				b.custom_ind_heating_type = u''
				b.save(force_update=True)
				return
			else:
				# fixme: додати форматування
				b.custom_ind_heating_type = value
				b.save(force_update=True)
				return value


		# boolean
		elif field == 'electricity':
			if (value is True) or (value is False):
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.electricity = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# boolean
		elif field == 'gas':
			if (value is True) or (value is False):
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.gas = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# boolean
		elif field == 'security_alarm':
			if (value is True) or (value is False):
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.security_alarm = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# boolean
		elif field == 'fire_alarm':
			if (value is True) or (value is False):
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.fire_alarm = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# boolean
		elif field == 'hot_water':
			if (value is True) or (value is False):
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.hot_water = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# boolean
		elif field == 'cold_water':
			if (value is True) or (value is False):
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.cold_water = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# boolean
		elif field == 'sewerage':
			if (value is True) or (value is False):
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.sewerage = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# boolean
		elif field == 'ventilation':
			if (value is True) or (value is False):
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.ventilation = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# boolean
		elif field == 'security':
			if (value is True) or (value is False):
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.security = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# text
		elif field == 'add_facilities':
			b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
			if not value:
				b.add_facilities = u''
				b.save(force_update=True)
				return
			else:
				# fixme: додати форматування
				b.add_facilities = value
				b.save(force_update=True)
				return


		# boolean
		elif field == 'phone':
			if (value is True) or (value is False):
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.phone = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# boolean
		elif field == 'mobile_coverage':
			if (value is True) or (value is False):
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.mobile_coverage = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# boolean
		elif field == 'internet':
			if (value is True) or (value is False):
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.internet = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# boolean
		elif field == 'cable_tv':
			if (value is True) or (value is False):
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.cable_tv = value
				b.save(force_update=True)
				return
			else:
				raise ValueError


		# boolean
		elif field == 'lan':
			if (value is True) or (value is False):
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.lan = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# blank or int
		elif field == 'phone_lines_count':
			if not value:
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.phone_lines_count = None
				b.save(force_update=True)
				return
			else:
				value = int(value)
				if value <= 0:
					raise ValueError()

				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.phone_lines_count = int(value)
				b.save(force_update=True)
				return


		# boolean
		elif field == 'parking':
			if (value is True) or (value is False):
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.parking = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# boolean
		elif field == 'open_air':
			if (value is True) or (value is False):
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.open_air = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		elif field == 'add_buildings':
			b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
			if not value:
				b.add_buildings = u''
				b.save(force_update=True)
				return
			else:
				# fixme: додати форматування
				b.add_buildings = value
				b.save(force_update=True)
				return value


		# boolean
		elif field == 'transport_stop':
			if (value is True) or (value is False):
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.transport_stop = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# boolean
		elif field == 'bank':
			if (value is True) or (value is False):
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.bank = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# boolean
		elif field == 'market':
			if (value is True) or (value is False):
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.market = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# boolean
		elif field == 'cash_machine':
			if (value is True) or (value is False):
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.cash_machine = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# boolean
		elif field == 'cafe':
			if (value is True) or (value is False):
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.cafe = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# boolean
		elif field == 'entertainment':
			if (value is True) or (value is False):
				b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
				b.entertainment = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# text
		elif field == 'add_showplaces':
			b = BusinessesBodies.objects.filter(id=h.body_id).only('id')[0]
			if not value:
				b.add_showplaces= u''
				b.save(force_update=True)
				return
			else:
				# fixme: додати форматування
				b.add_showplaces = value
				b.save(force_update=True)
				return


		# text
		elif field == 'lat_lng':
			h.set_lat_lng(value)
			return


		# text
		elif field == 'address':
			if not value:
				h.address = u''
				h.save(force_update=True)
				return
			else:
				# note: адреса не форматується, оскільки не можливо передбачити,
				# як саме користувач її введе.
				h.address = value
				h.save(force_update=True)
				return


		# text
		elif field == 'tag':
			if not value or ',' not in value:
				raise ValueError()

			tag_id, state = value.split(',')
			try:
				dirtag = DirTags.objects.filter(id=tag_id).only('id', 'pubs')[0]
			except (DatabaseError, IndexError):
				raise ValueError()

			try:
				if state == 'true':
					dirtag.add_publication(tid, h.id)
					return
				else:
					dirtag.rm_publication(tid, h.id)
					return
			except (PublicationAlreadyExists, RecordDoesNotExists):
				raise ValueError()


		# ...
		# other fields here
		# ...

		else:
			raise ValueError('invalid @field')

	except (DatabaseError, IntegrityError, InvalidOperation, ValueError):
		raise ValueError('Object type: apartments. Prefix: {field}. Value = {value}'.format(
			field = unicode(field), value = unicode(value)
		))