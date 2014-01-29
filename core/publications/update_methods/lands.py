#coding=utf-8
from django.db import DatabaseError, IntegrityError
from collective.methods.formatters import format_text, format_title
from core.publications.constants import CURRENCIES, COMMERCIAL_RENT_PERIODS, SALE_TRANSACTION_TYPES
from core.publications.models import LandsHeads, LandsBodies, LandsRentTerms
from core.publications.objects_constants.lands import LAND_DRIVEWAYS

# Оновлює інформацію про зем. ділянку.
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

def update_land(prefix, value, head_id=None, body_id=None, rent_id=None):
	try:
		# bool
		if prefix == 'for_sale':
			if value == 'true':
				h = LandsHeads.by_id(head_id, head_id='for_sale')
				h.for_sale = True
				h.save(force_update=True)

			elif value == 'false':
				h = LandsHeads.by_id(head_id, head_id='for_sale')
				h.for_sale = False
				h.save(force_update=True)

			else:
				raise ValueError('Invalid @for_sale value.')


		# bool
		elif prefix == 'for_rent':
			if value == 'true':
				h = LandsHeads.by_id(head_id, head_id='for_rent')
				h.for_rent = True
				h.save(force_update=True)

			elif value == 'false':
				h = LandsHeads.by_id(head_id, head_id='for_rent')
				h.for_rent = False
				h.save(force_update=True)

			else:
				raise ValueError('Invalid @for_rent value.')


		# blank or decimal
		elif prefix == 'price':
			if not value:
				b = LandsBodies.by_id(body_id, only='price')
				b.price = None
				b.save(force_update=True)

			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError('Invalid price')

				b = LandsBodies.by_id(body_id, only='price')
				b.price = value
				b.save(force_update=True)

				if int(value) == value:
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

			b = LandsBodies.by_id(body_id, only='transaction_type_sid')
			b.transaction_type_sid = value
			b.save(force_update=True)


		# sid
		elif prefix == 'currency':
			value = int(value)
			if value not in CURRENCIES.values():
				raise ValueError('Invalid currency sid')

			b = LandsBodies.by_id(body_id, only='currency_sid')
			b.currency_sid = value
			b.save(force_update=True)


		# bool
		elif prefix == 'price_contract':
			if value == 'true':
				b = LandsBodies.by_id(body_id, only='price_is_contract')
				b.price_is_contract = True
				b.save(force_update=True)

			elif value == 'false':
				b = LandsBodies.by_id(body_id, only='price_is_contract')
				b.price_is_contract = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid @price_is_contract value.')


		# text
		elif prefix == 'sale_add_terms':
			b = LandsBodies.by_id(body_id, only='add_terms')
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
				raise ValueError('Invalid rent period value.')

			r = LandsRentTerms.by_id(rent_id, only='period_sid')
			r.period_sid = value
			r.save(force_update=True)


		# blank or decimal
		elif prefix == 'rent_price':
			if not value:
				r = LandsRentTerms.by_id(rent_id, only='price')
				r.price = None
				r.save(force_update=True)

			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError('Invalid rent price')

				r = LandsRentTerms.by_id(rent_id, only='price')
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

			r = LandsRentTerms.by_id(rent_id, only='currency_sid')
			r.currency_sid = value
			r.save(force_update=True)
			return


		# boolean
		elif prefix == 'rent_price_contract':
			if value == 'true':
				r = LandsRentTerms.by_id(rent_id, only='price_is_contract')
				r.price_is_contract = True
				r.save(force_update=True)

			elif value == 'false':
				r = LandsRentTerms.by_id(rent_id, only='price_is_contract')
				r.price_is_contract = False
				r.save(force_update=True)

			else:
				raise ValueError('Invalid rent @price_is_contract')


		# text
		elif prefix == 'rent_add_terms':
			r = LandsRentTerms.by_id(rent_id, only='add_terms')
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
			h = LandsHeads.by_id(head_id, head_id='title')
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
			h = LandsHeads.by_id(head_id, head_id='descr')
			if not value:
				h.descr = None
				h.save(force_update=True)
				return

			else:
				value = format_text(value)
				h.descr = value
				h.save(force_update=True)
				return value


		# blank or float
		elif prefix == 'area':
			if not value:
				b = LandsBodies.by_id(body_id, only='area')
				b.area = None
				b.save(force_update=True)

			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError('Invalid halls area value.')

				b = LandsBodies.by_id(body_id, only='area')
				b.area = value
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
				b = LandsBodies.by_id(body_id, only='closed_area')
				b.closed_area = True
				b.save(force_update=True)

			elif value == 'false':
				b = LandsBodies.by_id(body_id, only='closed_area')
				b.closed_area = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid closed_area value.')


		# sid
		elif prefix == 'driveways':
			value = int(value)
			if value not in LAND_DRIVEWAYS.values():
				raise ValueError('Invalid driveways sid')

			b = LandsBodies.by_id(body_id, only='driveways_sid')
			b.driveways_sid = value
			b.save(force_update=True)


		# boolean
		elif prefix == 'electricity':
			if value == 'true':
				b = LandsBodies.by_id(body_id, only='electricity')
				b.electricity = True
				b.save(force_update=True)

			elif value == 'false':
				b = LandsBodies.by_id(body_id, only='electricity')
				b.electricity = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid electricity value.')


		# boolean
		elif prefix == 'gas':
			if value == 'true':
				b = LandsBodies.by_id(body_id, only='gas')
				b.gas = True
				b.save(force_update=True)

			elif value == 'false':
				b = LandsBodies.by_id(body_id, only='gas')
				b.gas = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid gas value.')


		# boolean
		elif prefix == 'water':
			if value == 'true':
				b = LandsBodies.by_id(body_id, only='water')
				b.water = True
				b.save(force_update=True)

			elif value == 'false':
				b = LandsBodies.by_id(body_id, only='water')
				b.water = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid water value.')


		# boolean
		elif prefix == 'canalisation':
			if value == 'true':
				b = LandsBodies.by_id(body_id, only='canalisation')
				b.canalisation = True
				b.save(force_update=True)

			elif value == 'false':
				b = LandsBodies.by_id(body_id, only='canalisation')
				b.canalisation = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid canalisation value.')


		# text
		elif prefix == 'add_facilities':
			b = LandsBodies.by_id(body_id, only='add_facilities')
			if not value:
				b.add_facilities = None
				b.save(force_update=True)

			else:
				# fixme: додати форматування
				b.add_facilities = value
				b.save(force_update=True)
				return value


		# boolean
		elif prefix == 'well':
			if value == 'true':
				b = LandsBodies.by_id(body_id, only='well')
				b.well = True
				b.save(force_update=True)

			elif value == 'false':
				b = LandsBodies.by_id(body_id, only='well')
				b.well = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid well value.')

			
		elif prefix == 'add_buildings':
			b = LandsBodies.by_id(body_id, only='add_buildings')
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
				b = LandsBodies.by_id(body_id, only='transport_stop')
				b.transport_stop = True
				b.save(force_update=True)

			elif value == 'false':
				b = LandsBodies.by_id(body_id, only='transport_stop')
				b.transport_stop = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid transport_stop value.')


		# boolean
		elif prefix == 'bank':
			if value == 'true':
				b = LandsBodies.by_id(body_id, only='bank')
				b.bank = True
				b.save(force_update=True)

			elif value == 'false':
				b = LandsBodies.by_id(body_id, only='bank')
				b.bank = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid bank value.')


		# boolean
		elif prefix == 'market':
			if value == 'true':
				b = LandsBodies.by_id(body_id, only='market')
				b.market = True
				b.save(force_update=True)

			elif value == 'false':
				b = LandsBodies.by_id(body_id, only='market')
				b.market = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid market value.')


		# boolean
		elif prefix == 'cash_machine':
			if value == 'true':
				b = LandsBodies.by_id(body_id, only='cash_machine')
				b.cash_machine = True
				b.save(force_update=True)

			elif value == 'false':
				b = LandsBodies.by_id(body_id, only='cash_machine')
				b.cash_machine = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid cash machine value.')


		# boolean
		elif prefix == 'cafe':
			if value == 'true':
				b = LandsBodies.by_id(body_id, only='cafe')
				b.cafe = True
				b.save(force_update=True)

			elif value == 'false':
				b = LandsBodies.by_id(body_id, only='cafe')
				b.cafe = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid cafe value.')


		# boolean
		elif prefix == 'entertainment':
			if value == 'true':
				b = LandsBodies.by_id(body_id, only='entertainment')
				b.entertainment = True
				b.save(force_update=True)

			elif value == 'false':
				b = LandsBodies.by_id(body_id, only='entertainment')
				b.entertainment = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid entertainment value.')


		# text
		elif prefix == 'add_showplaces':
			b = LandsBodies.by_id(body_id, only='add_showplaces')
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

	except (DatabaseError, IntegrityError), e:
		raise ValueError('Object type: flat. Message: {0} Prefix: {1}. Value = {2}'.format(
			unicode(e), unicode(prefix), unicode(value))
		)