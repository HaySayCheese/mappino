#coding=utf-8
from decimal import InvalidOperation

from django.db import DatabaseError, IntegrityError

from core.publications.update_methods.utils.formaters import format_text, format_title
from core.currencies.constants import CURRENCIES
from core.publications.constants import COMMERCIAL_RENT_PERIODS, SALE_TRANSACTION_TYPES, RED_LINE_VALUES
from core.publications.models import LandsBodies, LandsRentTerms, LandsSaleTerms
from core.publications.objects_constants.lands import LAND_DRIVEWAYS



# Оновлює інформацію про зем. ділянку.
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

def update_land(h, field, value, tid):
	try:
		# bool
		if field == 'for_sale':
			if (value is True) or (value is False):
				h.for_sale = value
				h.save(force_update=True)
				return
			else:
				raise ValueError()


		# blank or decimal
		elif field == 'sale_price':
			if not value:
				st = LandsSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
				st.price = None
				st.save(force_update=True)
				return
			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError()

				st = LandsSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
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

			st = LandsSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
			st.transaction_sid = value
			st.save(force_update=True)
			return


		# sid
		elif field == 'sale_currency_sid':
			value = int(value)
			if value not in CURRENCIES.values():
				raise ValueError()

			st = LandsSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
			st.currency_sid = value
			st.save(force_update=True)
			return


		# bool
		elif field == 'sale_is_contract':
			if (value is True) or (value is False):
				st = LandsSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
				st.is_contract = value
				st.save(force_update=True)
				return
			else:
				raise ValueError()


		# text
		elif field == 'sale_add_terms':
			st = LandsSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
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

			rt = LandsRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
			rt.period_sid = value
			rt.save(force_update=True)
			return


		# blank or decimal
		elif field == 'rent_price':
			if not value:
				rt = LandsRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
				rt.price = None
				rt.save(force_update=True)

			else:
				value = round(float(value.replace(',','.')), 2)
				if value <= 0:
					raise ValueError()

				rt = LandsRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
				rt.price = value
				rt.save(force_update=True)

				if int(value) == value:
					# Якщо після коми лише нулі - повернути ціле значення
					return "%.0f" % value
				else:
					# Інакше - округлити до 2х знаків після коми
					return "%.2f" % value


		# sid
		elif field == 'rent_currency':
			value = int(value)
			if value not in CURRENCIES.values():
				raise ValueError()

			rt = LandsRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
			rt.currency_sid = value
			rt.save(force_update=True)
			return


		# boolean
		elif field == 'rent_is_contract':
			if (value is True) or (value is False):
				rt = LandsRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
				rt.is_contract = True
				rt.save(force_update=True)
				return
			else:
				raise ValueError()


		# text
		elif field == 'rent_add_terms':
			rt = LandsRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
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
		elif field == 'red_line':
			value = int(value)
			if value not in RED_LINE_VALUES.values():
				raise ValueError()

			b = LandsBodies.by_id(h.body_id).only('id')
			b.red_line = value
			b.save(force_update=True)


		# text
		elif field == 'title':
			b = LandsBodies.objects.filter(id=h.body_id).only('id')[0]
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
			b = LandsBodies.objects.filter(id=h.body_id).only('id')[0]
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
		elif field == 'area':
			if not value:
				b = LandsBodies.objects.filter(id=h.body_id).only('id')[0]
				b.area = None
				b.save(force_update=True)
				return
			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError('Invalid halls area value.')

				b = LandsBodies.objects.filter(id=h.body_id).only('id')[0]
				b.area = value
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
				b = LandsBodies.objects.filter(id=h.body_id).only('id')[0]
				b.closed_area = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# sid
		elif field == 'driveways_sid':
			value = int(value)
			if value not in LAND_DRIVEWAYS.values():
				raise ValueError('Invalid driveways sid')

			b = LandsBodies.objects.filter(id=h.body_id).only('id')[0]
			b.driveways_sid = value
			b.save(force_update=True)
			return


		# boolean
		elif field == 'electricity':
			if (value is True) or (value is False):
				b = LandsBodies.objects.filter(id=h.body_id).only('id')[0]
				b.electricity = value
				b.save(force_update=True)
				return
			else:
				raise ValueError('Invalid electricity value.')


		# boolean
		elif field == 'gas':
			if (value is True) or (value is False):
				b = LandsBodies.objects.filter(id=h.body_id).only('id')[0]
				b.gas = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# boolean
		elif field == 'water':
			if (value is True) or (value is False):
				b = LandsBodies.objects.filter(id=h.body_id).only('id')[0]
				b.water = value
				b.save(force_update=True)
				return
			else:
				raise ValueError('Invalid water value.')


		# boolean
		elif field == 'sewerage':
			if (value is True) or (value is False):
				b = LandsBodies.objects.filter(id=h.body_id).only('id')[0]
				b.sewerage = value
				b.save(force_update=True)
				return
			else:
				raise ValueError('Invalid sewerage value.')


		# text
		elif field == 'add_facilities':
			b = LandsBodies.objects.filter(id=h.body_id).only('id')[0]
			if not value:
				b.add_facilities = u''
				b.save(force_update=True)
				return
			else:
				value = format_text(value)
				b.add_facilities = value
				b.save(force_update=True)
				return


		# boolean
		elif field == 'well':
			if (value is True) or (value is False):
				b = LandsBodies.objects.filter(id=h.body_id).only('id')[0]
				b.well = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()

			
		# text
		elif field == 'add_buildings':
			b = LandsBodies.objects.filter(id=h.body_id).only('id')[0]
			if not value:
				b.add_buildings= None
				b.save(force_update=True)
				return
			else:
				value = format_text(value)
				b.add_buildings = value
				b.save(force_update=True)
				return


		# boolean
		elif field == 'transport_stop':
			if (value is True) or (value is False):
				b = LandsBodies.objects.filter(id=h.body_id).only('id')[0]
				b.transport_stop = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# boolean
		elif field == 'bank':
			if (value is True) or (value is False):
				b = LandsBodies.objects.filter(id=h.body_id).only('id')[0]
				b.bank = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# boolean
		elif field == 'market':
			if (value is True) or (value is False):
				b = LandsBodies.objects.filter(id=h.body_id).only('id')[0]
				b.market = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# boolean
		elif field == 'cash_machine':
			if (value is True) or (value is False):
				b = LandsBodies.objects.filter(id=h.body_id).only('id')[0]
				b.cash_machine = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# boolean
		elif field == 'cafe':
			if (value is True) or (value is False):
				b = LandsBodies.objects.filter(id=h.body_id).only('id')[0]
				b.cafe = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# boolean
		elif field == 'entertainment':
			if (value is True) or (value is False):
				b = LandsBodies.objects.filter(id=h.body_id).only('id')[0]
				b.entertainment = value
				b.save(force_update=True)
				return
			else:
				raise ValueError()


		# text
		elif field == 'add_showplaces':
			b = LandsBodies.objects.filter(id=h.body_id).only('id')[0]
			if not value:
				b.add_showplaces= None
				b.save(force_update=True)

			else:
				value = format_text(value)
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


		# ...
		# other fields here
		# ...

		else:
			raise ValueError('invalid @field')

	except (DatabaseError, IntegrityError, InvalidOperation, ValueError), e:
		raise ValueError('Object type: flat. Message: {0} field: {1}. Value = {2}'.format(
			unicode(e), unicode(field), unicode(value))
		)