#coding=utf-8
from django.db import DatabaseError, IntegrityError
from collective.methods.formatters import format_text, format_title
from core.publications.constants import CURRENCIES, MARKET_TYPES, COMMERCIAL_RENT_PERIODS, SALE_TRANSACTION_TYPES
from core.publications.models import GaragesHeads, GaragesBodies, GaragesRentTerms
from core.publications.objects_constants.garages import GARAGE_DRIVE_WAYS

# Оновлює інформацію про гараж.
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

def update_garage(prefix, value, head_id=None, body_id=None, rent_id=None):
	try:
		# bool
		if prefix == 'for_sale':
			if value == 'true':
				h = GaragesHeads.by_id(head_id, only='for_sale')
				h.for_sale = True
				h.save(force_update=True)

			elif value == 'false':
				h = GaragesHeads.by_id(head_id, only='for_sale')
				h.for_sale = False
				h.save(force_update=True)

			else:
				raise ValueError('Invalid @for_sale value.')


		# bool
		elif prefix == 'for_rent':
			if value == 'true':
				h = GaragesHeads.by_id(head_id, only='for_rent')
				h.for_rent = True
				h.save(force_update=True)

			elif value == 'false':
				h = GaragesHeads.by_id(head_id, only='for_rent')
				h.for_rent = False
				h.save(force_update=True)

			else:
				raise ValueError('Invalid @for_rent value.')


		# blank or decimal
		elif prefix == 'price':
			if not value:
				b = GaragesBodies.by_id(body_id, only='price')
				b.price = None
				b.save(force_update=True)

			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError('Invalid price')

				b = GaragesBodies.by_id(body_id, only='price')
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

			b = GaragesBodies.by_id(body_id, only='transaction_type_sid')
			b.transaction_type_sid = value
			b.save(force_update=True)


		# sid
		elif prefix == 'currency':
			value = int(value)
			if value not in CURRENCIES.values():
				raise ValueError('Invalid currency sid')

			b = GaragesBodies.by_id(body_id, only='currency_sid')
			b.currency_sid = value
			b.save(force_update=True)


		# bool
		elif prefix == 'price_contract':
			if value == 'true':
				b = GaragesBodies.by_id(body_id, only='price_is_contract')
				b.price_is_contract = True
				b.save(force_update=True)

			elif value == 'false':
				b = GaragesBodies.by_id(body_id, only='price_is_contract')
				b.price_is_contract = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid @price_is_contract value.')


		# text
		elif prefix == 'sale_add_terms':
			b = GaragesBodies.by_id(body_id, only='add_terms')
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

			r = GaragesRentTerms.by_id(rent_id, only='period_sid')
			r.period_sid = value
			r.save(force_update=True)


		# blank or decimal
		elif prefix == 'rent_price':
			if not value:
				r = GaragesRentTerms.by_id(rent_id, only='price')
				r.price = None
				r.save(force_update=True)

			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError('Invalid rent price')

				r = GaragesRentTerms.by_id(rent_id, only='price')
				r.price = value
				r.save(force_update=True)

				if int(value) == value:
					# Якщо після коми лише нулі - повернути ціле значення
					return "%.0f" % value

				else:
					# Інакше - округлити до 2х знаків після коми
					return "%.2f" % float(value)


		# sid
		elif prefix == 'rent_currency':
			value = int(value)
			if value not in CURRENCIES.values():
				raise ValueError('Invalid rent currency')

			r = GaragesRentTerms.by_id(rent_id, only='currency_sid')
			r.currency_sid = value
			r.save(force_update=True)
			return


		# boolean
		elif prefix == 'rent_price_contract':
			if value == 'true':
				r = GaragesRentTerms.by_id(rent_id, only='price_is_contract')
				r.price_is_contract = True
				r.save(force_update=True)

			elif value == 'false':
				r = GaragesRentTerms.by_id(rent_id, only='price_is_contract')
				r.price_is_contract = False
				r.save(force_update=True)

			else:
				raise ValueError('Invalid rent @price_is_contract')


		# text
		elif prefix == 'rent_add_terms':
			r = GaragesRentTerms.by_id(rent_id, only='add_terms')
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
			h = GaragesHeads.by_id(head_id, only='title')
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
			h = GaragesHeads.by_id(head_id, only='descr')
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

			b = GaragesBodies.by_id(body_id, only='market_type_sid')
			b.market_type_sid = value
			b.save(force_update=True)


		# blank or float
		elif prefix == 'area':
			if not value:
				b = GaragesBodies.by_id(body_id, only='area')
				b.area = None
				b.save(force_update=True)

			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError('Invalid halls area value.')

				b = GaragesBodies.by_id(body_id, only='area')
				b.area = value
				b.save(force_update=True)

				if int(value) == value:
					# Відсікти дробову частину, якщо після коми нулі
					return "%.0f" % value
				else:
					# Скоротити / розширити до 2х цифр після коми
					return "%.2f" % value


		# blank or float
		elif prefix == 'ceiling_height':
			if not value:
				b = GaragesBodies.by_id(body_id, only='ceiling_height')
				b.ceiling_height = None
				b.save(force_update=True)

			else:
				value = round(float(value.replace(',', '.')), 2)
				if value <= 0:
					raise ValueError('Invalid ceiling height value.')

				b = GaragesBodies.by_id(body_id, only='ceiling_height')
				b.ceiling_height = value
				b.save(force_update=True)

				if int(value) == value:
					# Відсікти дробову частину, якщо після коми нулі
					return "%.0f" % value
				else:
					# скоротити / розширити до 2х цифр після коми
					return "%.2f" % value


		# boolean
		elif prefix == 'pit':
			if value == 'true':
				b = GaragesBodies.by_id(body_id, only='pit')
				b.pit = True
				b.save(force_update=True)

			elif value == 'false':
				b = GaragesBodies.by_id(body_id, only='pit')
				b.pit = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid pit value.')


		# sid
		elif prefix == 'driveways':
			value = int(value)
			if value not in GARAGE_DRIVE_WAYS.values():
				raise ValueError('Invalid driveways sid')

			b = GaragesBodies.by_id(body_id, only='driveways_sid')
			b.driveways_sid = value
			b.save(force_update=True)


		# boolean
		elif prefix == 'electricity':
			if value == 'true':
				b = GaragesBodies.by_id(body_id, only='electricity')
				b.electricity = True
				b.save(force_update=True)

			elif value == 'false':
				b = GaragesBodies.by_id(body_id, only='electricity')
				b.electricity = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid electricity value.')


		# boolean
		elif prefix == 'gas':
			if value == 'true':
				b = GaragesBodies.by_id(body_id, only='gas')
				b.gas = True
				b.save(force_update=True)

			elif value == 'false':
				b = GaragesBodies.by_id(body_id, only='gas')
				b.gas = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid gas value.')


		# boolean
		elif prefix == 'security_alarm':
			if value == 'true':
				b = GaragesBodies.by_id(body_id, only='security_alarm')
				b.security_alarm = True
				b.save(force_update=True)

			elif value == 'false':
				b = GaragesBodies.by_id(body_id, only='security_alarm')
				b.security_alarm = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid security alarm value.')


		# boolean
		elif prefix == 'fire_alarm':
			if value == 'true':
				b = GaragesBodies.by_id(body_id, only='fire_alarm')
				b.fire_alarm = True
				b.save(force_update=True)

			elif value == 'false':
				b = GaragesBodies.by_id(body_id, only='fire_alarm')
				b.fire_alarm = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid fire alarm value.')


		# boolean
		elif prefix == 'hot_water':
			if value == 'true':
				b = GaragesBodies.by_id(body_id, only='hot_water')
				b.hot_water = True
				b.save(force_update=True)

			elif value == 'false':
				b = GaragesBodies.by_id(body_id, only='hot_water')
				b.hot_water = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid fire alarm value.')


		# boolean
		elif prefix == 'cold_water':
			if value == 'true':
				b = GaragesBodies.by_id(body_id, only='cold_water')
				b.cold_water = True
				b.save(force_update=True)

			elif value == 'false':
				b = GaragesBodies.by_id(body_id, only='cold_water')
				b.cold_water = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid cold water value.')


		# boolean
		elif prefix == 'ventilation':
			if value == 'true':
				b = GaragesBodies.by_id(body_id, only='ventilation')
				b.ventilation = True
				b.save(force_update=True)

			elif value == 'false':
				b = GaragesBodies.by_id(body_id, only='ventilation')
				b.ventilation = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid ventilation value.')


		# boolean
		elif prefix == 'security':
			if value == 'true':
				b = GaragesBodies.by_id(body_id, only='security')
				b.security = True
				b.save(force_update=True)

			elif value == 'false':
				b = GaragesBodies.by_id(body_id, only='security')
				b.security = False
				b.save(force_update=True)

			else:
				raise ValueError('Invalid security value.')


		# text
		elif prefix == 'add_facilities':
			b = GaragesBodies.by_id(body_id, only='add_facilities')
			if not value:
				b.add_facilities = None
				b.save(force_update=True)

			else:
				# fixme: додати форматування
				b.add_facilities = value
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