#coding=utf-8
import copy
import json
import mmh3

import abc
from django.core.exceptions import SuspiciousOperation

from collective.exceptions import InvalidArgument, RuntimeException
from core.currencies.constants import CURRENCIES
from core.currencies.currencies_manager import convert as convert_currency
from core.markers_servers.classes import DegreeSegmentPoint, Point, SegmentPoint, DegreePoint
from core.publications.constants import OBJECTS_TYPES, HEAD_MODELS, MARKET_TYPES, LIVING_RENT_PERIODS, \
	HEATING_TYPES, OBJECT_STATES, FLOOR_TYPES
from core.publications.objects_constants.flats import FLAT_ROOMS_PLANNINGS
from core.publications.objects_constants.trades import TRADE_BUILDING_TYPES
from mappino.wsgi import redis_connections


class BaseMarkersManager(object):
	"""
	Відповідає за збереження та видачу інформації про маркери в redis.
	Для ефективної вибірки на мапу умовно накладено координутну сітку, одна комірка якої зветься сегментом.
	Припустімо є координати виду 20.1234567 та 40.1234567. Тут 20 та 40 — градуси,
	1234567 — мінути в десятковому представленні.

	Сегменти утворено шляхом поділу мінут градуса від 0 до 99 з кроком в 2.
	Наприклад: 00;00, 02;00, 04;00 і т.д. Таким чином отримуємо 50*50 = 2500 сегментів в межах одного градуса.
	Крок сегмента підібрано експерементально. Як правило, у вибірку потрапляє від 4х сегментів одночасно.
	"""
	class TooBigTransaction(SuspiciousOperation): pass
	class SerializationError(BaseException): pass
	class DeserializationError(BaseException): pass


	__metaclass__ = abc.ABCMeta
	def __init__(self, tid):
		if tid not in OBJECTS_TYPES.values():
			raise InvalidArgument('Incorrect tid.')
		self.tid = tid
		self.model = HEAD_MODELS[tid]

		self.redis = redis_connections['steady']
		self.segments_hashes_prefix = 'segments_hashes'
		self.separator = ';'
		self.digest_separator = ':'


	def add_publication(self, hid):
		"""
		Запитає з БД оголошення з id=hid та мінімальним набором даних необхідних для формування маркера.
		tid не передається, оскільки кожен клас прив’язаний до окремої моделі на рівні коду,
		і передбачається за замовчуванням.

		Сериалізує отримані дані у формат для збереження в індексі redis та
		оновить сегмент в який потрапляє маркер даного оголошення, в тому числі і хеш сегменту.
		"""
		if hid is None:
			raise InvalidArgument('head id can not be None.')

		try:
			queryset = self.record_min_queryset(hid)
			record = queryset[0]
		except IndexError:
			raise InvalidArgument('Object with such hid does not exist.')

		degree = DegreePoint(record.degree_lat, record.degree_lng)
		segment = SegmentPoint(record.segment_lat, record.segment_lng)
		seg_digest = self.__segment_digest(degree, segment)

		sector = Point(record.segment_lat, record.segment_lng)
		position = Point(record.pos_lat, record.pos_lng)
		pos_digest = self.__position_digest(sector, position)
		data = self.serialize_publication(record)

		self.redis.hset(seg_digest, pos_digest, data)
		self.__update_segment_hash(seg_digest, hid)


	def remove_publication(self, hid):
		"""
		Removes marker of publication with id = @hid from the redis cache.

		:param hid: id of the head-record of the publication.
		:raises
			InvalidArgument: hid == None
			InvalidArgument: head record does not exist.

		"""
		if hid is None:
			raise InvalidArgument('head id can not be None.')

		try:
			queryset = self.record_min_queryset(hid)
			record = queryset[0]
		except IndexError:
			raise InvalidArgument('Object with such hid does not exist.')


		if not record.is_published():
			# unpublished records does not have coordinates,
			# so they can not be deleted from index
			return

		degree = DegreePoint(record.degree_lat, record.degree_lng)
		segment = SegmentPoint(record.segment_lat, record.segment_lng)
		seg_digest = self.__segment_digest(degree, segment)

		sector = Point(record.segment_lat, record.segment_lng)
		position = Point(record.pos_lat, record.pos_lng)
		pos_digest = self.__position_digest(sector, position)


		self.redis.hdel(seg_digest, pos_digest)
		self.__update_segment_hash(seg_digest, hid)


	def markers(self, ne, sw, conditions=None):
		"""
		Повертає список маркерів, що потрапляють у в’юпорт з координатами North East (ne) та South West (sw).
		В деяких випадках у видачу можуть додтково потрапити маркери суміжніх сегментів.
		Це пов’язано із особливістю будови внутршіньої сітки в пам’яті redis в якій розкладено макери.
		Якщо переданий в’юпорт знаходиться на перехресті 4х або більше сегментів —
		у видачу потраплять всі маркери з цих сегментів.

		Якщо conditions не None — список маркерів буде попередньо профільтровано.

		Для опису формату в якому зберігаються дані в redis — див. документацію до add_publication()

		Args:
			ne: (North East) Point з координатами північно-західного кута в’юпорта.
			sw: (South West) Point з координатами південно-східного кута в’юпорта.
			conditions: словник з інформаціює про фільтри, які слід застосувати до вибірки.
		"""
		if (ne is None) or (sw is None):
			raise InvalidArgument('Invalid coordinates.')


		result = {}
		for digest in self.__segments_digests(ne, sw):
			degrees = self.__degrees_from_digest(digest)

			pipe = self.redis.pipeline()
			minutes = self.redis.hkeys(digest)
			for minute in minutes:
				pipe.hget(digest, minute)

			raw_markers_data = pipe.execute()
			if not raw_markers_data:
				continue

			if degrees not in result:
				result[degrees] = {}

			# Інформація в redis для економії пам’яті зберігається в стиснутому вигляді.
			# Для аналізу і фільтрування даних їх слід десериалізувати.
			markers_data = [self.deserialize_marker_data(marker) for marker in raw_markers_data]

			# Зводимо маркери з координатами
			markers_data = zip(minutes, markers_data)

			# Фільтруємо і упаковуємо у формат для видачі
			for marker in self.filter(markers_data, conditions):
				minutes = marker[0]
				data = marker[1]
				brief = self.marker_brief(data, conditions)
				result[degrees][minutes] = brief
		return result


	def markers_of_realtor(self, realtor):
		model = HEAD_MODELS[self.tid]
		publications = model.objects.filter(
			owner = realtor,
			state_sid = OBJECT_STATES.published()
		)


		result = {}
		for record in publications:
			degree = DegreePoint(record.degree_lat, record.degree_lng)
			degree_digest = '{lat};{lng}'.format(lat=degree.lat, lng=degree.lng)

			position = Point(record.pos_lat, record.pos_lng)
			position_digest = '{lat}:{lng}'.format(lat=position.lat, lng=position.lng)

			# todo: брифи маркерів формуються через виклик функції сериалізаії/десериалізації,
			# тоді як можна було б обійтись
			data = self.marker_brief(self.deserialize_marker_data(self.serialize_publication(record)))


			if not degree_digest in result:
				result[degree_digest] = {}
			result[degree_digest][position_digest] = data

		return result


	def viewport_hash(self, ne, sw):
		"""
		Підраховує та повертає хеш сегментів (див. док. __segment_digest),
		які потрапляють у в’юпорт North East (ne) та South West (sw).
		Загальний хеш вираховується як hash(хеш 1-го сегменту + хеш 2-го сегменту + ... + хеш N-го сегменту).

		Для підрахунку хешу використовується MurmurHash3,
		як один з найшвидших хеш-алгоритмів.(див. док. __update_segment_hash)
		УВАГА: Даний алгоритм не є криптостійким!

		Args:
			ne: (North East) Point з координатами північно-західного кута в’юпорта.
		 	sw: (South West) Point з координатами південно-східного кута в’юпорта.
		"""

		pipe = self.redis.pipeline()
		for digest in self.__segments_digests(ne, sw):
			pipe.hget(self.segments_hashes_prefix, digest)

		key = ''
		for segment_data in pipe.execute():
			if segment_data is not None:
				key += mmh3.hash(segment_data)
		return str(mmh3.hash(key))


	def __segments_digests(self, ne, sw):
		"""
		Повертає список дайджестів сегментів (див. док. __segment_digest),
		які потрапляють у в’юпорт North East (ne) та South West (sw).

		Args:
			ne: (North East) Point з координатами північно-західного кута в’юпорта.
			sw: (South West) Point з координатами південно-східного кута в’юпорта.
		"""
		start = DegreeSegmentPoint(ne.lat, ne.lng)
		stop = DegreeSegmentPoint(sw.lat, sw.lng)

		# Мапи google деколи повертають координати так, що stop опиняється перед start,
		# і тоді алгоритм починає пробіг по всьому глобусу і падає на перевірці розміру транзакції.
		# Дані перетворення видозмінюють координати так, щоб start завжди був перед stop,
		# і неважливо в якому порядку вони прийдуть.
		if start.degree.lng > stop.degree.lng:
			start.degree.lng, stop.degree.lng = stop.degree.lng, start.degree.lng
		elif start.segment.lng > stop.segment.lng:
			start.segment.lng, stop.segment.lng = stop.segment.lng, start.segment.lng

		if start.degree.lat < stop.degree.lat:
			start.degree.lat, stop.degree.lat = stop.degree.lat, start.degree.lat
		elif start.segment.lat < stop.segment.lat:
			start.segment.lat, stop.segment.lat = stop.segment.lat, start.segment.lat


		# Умисно розширити запит на 1 сегмент вліво і вгору, щоб прихопити також і ті оголошення,
		# які, можливо, знаходяться поряд із в’юпортом, або навіть і в’юпорті, але не потрапляють
		# у стартовий сегмент
		start.inc_segment_lat()
		start.dec_segment_lng()


		digests = []
		current = copy.deepcopy(start)
		while True:
			current.degree.lng = start.degree.lng
			current.segment.lng = start.segment.lng

			while True:
				digests.append(self.__segment_digest(current.degree, current.segment))

				# Заборонити одночасну вибірку маркерів з великої к-сті сегментів.
				# Таким чином можна уберегтись від занадто великих транзакцій (ddos),
				# накопичування занадто великих обсягів даних в пам’яті та
				# занадто великої к-сті запитів від інших користувачів в черзі на обробку.
				if len(digests) > 25:
					raise self.TooBigTransaction()

				if (current.degree.lng == stop.degree.lng) and (current.segment.lng == stop.segment.lng):
					break
				current.inc_segment_lng()

			if (current.degree.lat == stop.degree.lat) and (current.segment.lat == stop.segment.lat):
				break
			current.dec_segment_lat()
		return digests


	def __segment_digest(self, degree, segment):
		"""
		Повертає digest сегмента (для формату див. код.)
		"""
		return  str(self.tid) + self.digest_separator + \
		        str(degree.lat) + self.digest_separator + \
		        str(degree.lng) + self.digest_separator + \
		        str(segment.lat) + self.digest_separator + \
		        str(segment.lng)


	def __position_digest(self, segment, position):
		"""
		Повертає digest координат маркера (для формату див. код.)
		"""
		return  str(segment.lat) + str(position.lat) + self.digest_separator + \
		        str(segment.lng) + str(position.lng)


	def __degrees_from_digest(self, digest):
		"""
		Поверне градус сегмента у форматі "lat;lng".
		Відомості про градус беруться з дайджеста сегмента.
		"""
		index = digest.find(self.digest_separator)
		if index < 0:
			raise RuntimeException('Invalid digest.')

		coordinates = digest[index+1:].split(self.digest_separator)
		if ('' in coordinates) or (None in coordinates):
			raise RuntimeError('Invalid digest.')

		return coordinates[0] + ';' + coordinates[1]


	def __update_segment_hash(self, digest, record_id):
		"""
		Кожен сегмент маркерів має власний хеш.
		Він використовується, наприклад, як etag для запитів на отримання маркерів.
		Даний метод оновить хеш для сегменту з дайджестом digest.

		Для хешування використовується MurmurHash3,
		оскільки він дуже швидкий і видає короткі дайджести,
		а криптостійкість в даному випадку не важлива.

		Новий хеш вираховується за формулою h = hash(попередній хеш + record_id)
		"""

		current_hash = self.redis.hget(self.segments_hashes_prefix, digest)
		if current_hash is None:
			current_hash = ''

		segment_hash = mmh3.hash(current_hash + str(record_id))
		self.redis.hset(self.segments_hashes_prefix, digest, segment_hash)


	@staticmethod
	def format_price(price, base_currency, destination_currency):
		"""
		Поверне рядок з ціною price сконвертованою з валюти base_currency у валюту destination_currency.
		Якщо валюти base_currency та destination_currency відмінні — перед результатом буде додано "≈",
		як індикатор того, що ціна в отриманій валюті приблизна.
		"""
		result = u''
		if base_currency != destination_currency:
			result += u'≈'

		converted_price = convert_currency(price, base_currency, destination_currency)
		converted_price = int('{0}'.format(converted_price).split('.')[0]) # копійок в кінці ціни нам не потрібно
		return result + u'{0}'.format(converted_price).replace(',',' ')


	@staticmethod
	def format_currency(currency):
		if currency == CURRENCIES.dol():
			return u'дол.'
		elif currency == CURRENCIES.uah():
			return u'грн.'
		elif currency == CURRENCIES.eur():
			return u'евро'
		else:
			raise InvalidArgument('Invalid currency.')


	@abc.abstractmethod
	def serialize_publication(self, record):
		return None


	@abc.abstractmethod
	def deserialize_marker_data(self, record):
		return None


	@abc.abstractmethod
	def marker_brief(self, data, condition=None):
		return None


	@abc.abstractmethod
	def record_min_queryset(self, hid):
		"""
		Повертає head-запис лише з тими полями моделі,
		які прийматимуть участь у формуванні брифу маркеру і фільтрів.
		"""
		return self.model.objects(id=hid)


	@abc.abstractmethod
	def filter(self, publications, conditions):
		return publications



class FlatsMarkersManager(BaseMarkersManager):
	def __init__(self):
		super(FlatsMarkersManager, self).__init__(OBJECTS_TYPES.flat())


	def record_min_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'hash_id',
			'for_sale', 'for_rent',
			'sale_terms__price', 'sale_terms__currency_sid',

			'rent_terms__price', 'rent_terms__currency_sid', 'rent_terms__period_sid',
		    'rent_terms__persons_count', 'rent_terms__family', 'rent_terms__foreigners',

			'body__electricity', 'body__gas', 'body__hot_water', 'body__cold_water', 'body__lift',
			'body__market_type_sid', 'body__heating_type_sid', 'body__rooms_planning_sid',
			'body__rooms_count', 'body__total_area', 'body__floor_type_sid', 'body__floor', 'body__floors_count')


	def serialize_publication(self, record):
		if True not in (record.for_sale, record.for_rent):
			raise self.SerializationError('Object must be "for sale", "for rent", or both. Nothing selected.')

		if record.body.rooms_count is None:
			raise self.SerializationError('rooms_count is required but absent.')

		if record.body.total_area is None:
			raise self.SerializationError('total_area is required but absent.')


		data = [
			record.hash_id,
			record.for_sale,
		    record.for_rent,

			record.body.rooms_count,
			float(record.body.total_area), # json can't handle decimal

			record.body.electricity,
		    record.body.gas,
		    record.body.hot_water,
		    record.body.cold_water,
		    record.body.lift,

		    record.body.market_type_sid,
		    record.body.heating_type_sid,
		    record.body.rooms_planning_sid,
			record.body.floor_type_sid,
		]

		# Поле поверху може бути пустим, якщо тип поверху вибрано як "мансарда" чи "цоколь".
		# Якщо воно пусте — немає змісту його сериалізувати.
		if record.body.floor_type_sid == FLOOR_TYPES.floor():
			data.append(record.body.floor)


		if record.for_sale:
			if record.sale_terms.price is None:
				raise self.SerializationError('sale_price is required but absent.')

			data.extend([
		        float(record.sale_terms.price), # json can't handle decimal
			    record.sale_terms.currency_sid,
			])


		if record.for_rent:
			data.extend([
				float(record.rent_terms.price), # json can't handle decimal
			    record.rent_terms.currency_sid,
				record.rent_terms.period_sid,
			    record.rent_terms.persons_count, # WARN: необов’язкове поле

			    record.rent_terms.family,
			    record.rent_terms.foreigners,
			])


		digest = json.dumps(data).replace('true', 't').replace('false', 'f').replace(' ', '')
		return digest


	def deserialize_marker_data(self, data):
		data = json.loads(data.replace('t', 'true').replace('f', 'false'))

		index = iter(xrange(0, len(data)))
		deserialized_data = {
			'hash_id':              data[next(index)],
			'for_sale':             data[next(index)],
		    'for_rent':             data[next(index)],

			'rooms_count':          data[next(index)],
		    'total_area':           data[next(index)],

			'electricity':          data[next(index)],
		    'gas':                  data[next(index)],
		    'hot_water':            data[next(index)],
		    'cold_water':           data[next(index)],
		    'lift':                 data[next(index)],

			'market_type_sid':      data[next(index)],
			'heating_type_sid':     data[next(index)],
			'rooms_planning_sid':   data[next(index)],
			'floor_type_sid':       data[next(index)],
		}
		if deserialized_data['floor_type_sid'] == FLOOR_TYPES.floor():
			deserialized_data['floor'] = data[next(index)]


		if deserialized_data['for_sale']:
			deserialized_data.update({
				'sale_price': data[next(index)],
				'sale_currency_sid': data[next(index)],
			})


		if deserialized_data['for_rent']:
			deserialized_data.update({
				'rent_price': data[next(index)],
				'rent_currency_sid': data[next(index)],
				'rent_period_sid': data[next(index)],
			    'persons_count': data[next(index)],

				'family': data[next(index)],
				'foreigners': data[next(index)],
			})


		return deserialized_data


	def marker_brief(self, marker, filters=None):
		"""
		Сформує бриф для маркеру на основі даних, переданих у фільтрі.
		(В даний момент враховується лише валюта запиту)
		"""

		# todo: додати зміну видачі в залежності від фільтрів.
		# Наприклад, якщо задано к-сть кімнат від 1 до 1 - нема змісту показувати в брифі к-сть кімнат,
		# ітак ясно, що їх буде не більше одної.

		result = {
			'id': marker['hash_id']
		}

		# Гривня як базова валюта обирається згідно з чинним законодавством,
		# але якщо у фільтрі вказана інша - переформатувати бриф на неї.
		if filters is None:
			currency = CURRENCIES.uah()
		else:
			currency = filters.get('currency_sid', CURRENCIES.uah())


		if marker.get('for_sale', False):
			sale_price = self.format_price(marker['sale_price'], marker['sale_currency_sid'], currency)
			result.update({
				'd0': u'Комнат: {0}'.format(marker.get('rooms_count')) \
						if marker.get('rooms_count') else 'Комнат: не указано',
				'd1': u'{0} {1}'.format(sale_price, self.format_currency(currency)),
			})
			return result

		elif marker.get('for_rent', False):
			rent_price = self.format_price(marker['rent_price'], marker['rent_currency_sid'], currency)
			result.update({
				'd0': u'Мест: {0}'.format(marker.get('persons_count')) \
						if marker.get('persons_count') else u'Мест: не указано',
				'd1': u'{0} {1}'.format(rent_price, self.format_currency(currency)),
			})
			return result

		raise RuntimeException('Marker is not for sale and not for rent.')


	def filter(self, publications, filters):
		# WARNING:
		#   дана функція для економії часу виконання не виконує deepcopy над publications

		if filters is None:
			return publications

		operation_sid = filters.get('operation_sid')
		if operation_sid is None:
			raise InvalidArgument('Invalid conditions. Operation_sid is absent.')


		# Перед фільтруванням оголошень слід перевірити цілісність і коректність об’єкту умов.
		# На даному етапі виконується перевірка всіх обов’язкових полів filters.
		# Дану перевірку винесено за цикл фільтрування щоб підвищити швидкодію,
		# оскільки об’єкт filters не змінюється в ході фільтрування і достатньо перевіріити його лише раз.
		currency_sid = filters.get('currency_sid')
		if currency_sid is None:
			# Перевіряти фільтри цін має зміст лише тоді, коли задано валюту фільтру,
			# інакше неможливо привести валюту ціни з фільтра до валюти з оголошення.
			# На фронтенді валюта повинна бути задана за замовчуванням.
			raise InvalidArgument('sale_currency_sid is absent.')
		elif currency_sid not in CURRENCIES.values():
			raise InvalidArgument('currency_sid is invalid.')

		if operation_sid == 1: # rent
			rent_period_sid = filters.get('period_sid')
			if rent_period_sid is None:
				raise InvalidArgument('Rent period sid is absent.')


		# Для відбору елементів зі списку publications, використовується список statuses.
		# Кість елементів цього списку відповідає к-сті елементів publications.
		# На початку фільтрування всі елементи statuses встановлені в True.
		# Під час фільтрування деякі з них будуть встановлені в False.
		# На завершальному етапі зі списку publications будуть відібрані лише ті елементи,
		# відповідний елемент statuses яких встановлений в True.
		#
		# Додатковий список використовується для підвищення швидкодії фільтрування,
		# оскільки зміна True/False відбуваєтсья в рази швидше, ніж вилучення елементів зі списку
		# з повторною його перебудовою на кожній перевірці та ітерації.
		statuses = [True] * len(publications)


		# sale filters
		if operation_sid == 0:
			for i in range(len(statuses)):
				# Якщо даний запис вже позначений як виключений — не аналізувати його.
				if not statuses[i]:
					continue

				marker = publications[i][1]

				if not marker.get('for_sale', False):
					statuses[i] = False
					continue

				# sale price
				price_min = filters.get('price_from')
				price_max = filters.get('price_to')
				if price_min is not None:
					price_min = convert_currency(price_min, currency_sid, marker['sale_currency_sid'])
				if price_max is not None:
					price_max = convert_currency(price_max, currency_sid, marker['sale_currency_sid'])


				if (price_max is not None) and (price_min is not None):
					if not price_min <= marker['sale_price'] <= price_max:
						statuses[i] = False
						continue

				elif price_min is not None:
					if not price_min <= marker['sale_price']:
						statuses[i] = False
						continue

				elif price_max is not None:
					if not marker['sale_price'] <= price_max:
						statuses[i] = False
						continue


				# market type
				if ('new_buildings' in filters) and ('secondary_market' in filters):
					# Немає змісту фільтрувати.
					# Під дані умови потрапляють всі об’єкти.
					pass

				elif 'new_buildings' in filters:
					statuses[i] = (marker['market_type_sid'] == MARKET_TYPES.new_building())
				elif 'new_buildings' in filters:
					statuses[i] = (marker['market_type_sid'] == MARKET_TYPES.secondary_market())


				# rooms count
				rooms_count_min = filters.get('rooms_count_from')
				rooms_count_max = filters.get('rooms_count_to')
				rooms_count = marker.get('rooms_count')

				if (rooms_count_max is not None) or (rooms_count_min is not None):
					# Поле "к-сть кімнат" не обов’язкове.
					# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
					# відхилити запис через неможливість аналізу.
					if rooms_count is None:
						statuses[i] = False
						continue


				if (rooms_count_max is not None) and (rooms_count_min is not None):
					if not rooms_count_min <= rooms_count <= rooms_count_max:
						statuses[i] = False
						continue

				elif rooms_count_min is not None:
					if not rooms_count_min <= rooms_count:
						statuses[i] = False
						continue

				elif rooms_count_max is not None:
					if not rooms_count <= rooms_count_max:
						statuses[i] = False
						continue


				# total area
				total_area_min = filters.get('total_area_from')
				total_area_max = filters.get('total_area_to')
				total_area = marker.get('total_area')

				if (total_area_max is not None) or (total_area_min is not None):
					# Поле "загальна площа" може бути не обов’язковим.
					# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
					# відхилити запис через неможливість аналізу.
					if total_area is None:
						statuses[i] = False
						continue


				if (total_area_max is not None) and (total_area_min is not None):
					if not total_area_min <= total_area <= total_area_max:
						statuses[i] = False
						continue

				elif total_area_min is not None:
					if not total_area_min <= total_area:
						statuses[i] = False
						continue

				elif total_area_max is not None:
					if not total_area <= total_area_max:
						statuses[i] = False
						continue


				# floor
				floor_min = filters.get('floor_from')
				floor_max = filters.get('floor_to')
				floor = marker.get('floor')

				if (floor_max is not None) or (floor_max is not None):
					# Поле "к-сть поверхів" не обов’язкове.
					# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
					# відхилити запис через неможливість аналізу.
					if floor is None:
						statuses[i] = False
						continue


				if (floor_min is not None) and (floor_max is not None):
					if not floor_min <= floor <= floor_max:
						statuses[i] = False
						continue

				elif floor_min is not None:
					if not floor_min <= floor:
						statuses[i] = False
						continue

				elif floor_max is not None:
					if not floor <= floor_max:
						statuses[i] = False
						continue


				# rooms planning
				rooms_planning_sid = filters.get('rooms_planning_sid')
				if rooms_planning_sid is not None:
					if rooms_planning_sid == 1: # свободная планировка
						if marker['rooms_planning_sid'] != FLAT_ROOMS_PLANNINGS.free():
							statuses[i] = False
							continue

					elif rooms_planning_sid == 2: # предварительная
						if marker['rooms_planning_sid'] == FLAT_ROOMS_PLANNINGS.free():
							statuses[i] = False
							continue


				# electricity
				if 'electricity' in filters:
					if (not 'electricity' in marker) or (not marker['electricity']):
						statuses[i] = False
						continue

				# gas
				if  'gas' in filters:
					if (not 'gas' in marker) or (not marker['gas']):
						statuses[i] = False
						continue

				# hot water
				if 'hot_water' in filters:
					if (not 'hot_water' in marker) or (not marker['hot_water']):
						statuses[i] = False
						continue

				# cold water
				if  'cold_water' in filters:
					if (not 'cold_water' in marker) or (not marker['cold_water']):
						statuses[i] = False
						continue

				# lift
				if 'lift' in filters:
					if (not 'lift' in marker) or (not marker['lift']):
						statuses[i] = False
						continue


				# heating type
				heating_type_sid = filters.get('heating_type_sid')
				if heating_type_sid is not None:
					# Поле "тип опалення" може бути не обов’язковим.
					# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
					# відхилити запис через неможливість аналізу.
					if 'heating_type_sid' not in marker:
						statuses[i] = False
						continue

					if heating_type_sid == 1: # центральне
						if marker['heating_type_sid'] != HEATING_TYPES.central():
							statuses[i] = False
							continue

					elif heating_type_sid == 2: # індивідуальне
						if marker['heating_type_sid'] != HEATING_TYPES.individual():
							statuses[i] = False
							continue

					elif heating_type_sid == 3: # відсутнє
						if marker['heating_type_sid'] != HEATING_TYPES.none():
							statuses[i] = False
							continue


		# rent filters
		elif operation_sid == 1:
			for i in range(len(publications)):
				# Якщо даний маркер вже позначений як виключений — не аналізувати його.
				if not statuses[i]:
					continue

				marker = publications[i][1]

				# operation type
				if not marker.get('for_rent', False):
					statuses[i] = False
					continue


				# rent price
				price_min = filters.get('price_from')
				price_max = filters.get('price_to')
				if price_min is not None:
					price_min = convert_currency(price_min, currency_sid, marker['rent_currency_sid'])
				if price_max is not None:
					price_max = convert_currency(price_max, currency_sid, marker['rent_currency_sid'])


				if (price_max is not None) and (price_min is not None):
					if not price_min <= marker['rent_price'] <= price_max:
						statuses[i] = False
						continue

				elif price_min is not None:
					if not price_min <= marker['rent_price']:
						statuses[i] = False
						continue

				elif price_max is not None:
					if not marker['rent_price'] <= price_max:
						statuses[i] = False
						continue


				# rent period
				if not 'rent_period_sid' in marker:
					statuses[i] = False
					continue

				if rent_period_sid == 1:
					# посуточно
					if marker['rent_period_sid'] != LIVING_RENT_PERIODS.daily():
						statuses[i] = False
						continue

				elif rent_period_sid == 2:
					# помісячно і довгострокова оренда
					if (marker['rent_period_sid'] != LIVING_RENT_PERIODS.monthly()) or \
							(marker['rent_period_sid'] != LIVING_RENT_PERIODS.long_period()):
						statuses[i] = False
						continue


				# persons_count
				persons_count_min = filters.get('persons_count_from')
				persons_count_max = filters.get('persons_count_to')
				persons_count = marker.get('persons_count')

				if (persons_count_min is not None) or (persons_count_max is not None):
					# Поле "к-сть місць"може бути не обов’язковим.
					# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
					# відхилити запис через неможливість аналізу.
					if persons_count is None:
						statuses[i] = False
						continue


				if (persons_count_min is not None) and (persons_count_max is not None):
					if not persons_count_min <= persons_count <= persons_count_max:
						statuses[i] = False
						continue

				elif persons_count_min is not None:
					if not persons_count_min <= persons_count:
						statuses[i] = False
						continue

				elif persons_count_max is not None:
					if not persons_count <= persons_count_max:
						statuses[i] = False
						continue


				# for family
				if 'family' in filters:
					if (not 'for_family' in marker) or (not marker['for_family']):
						statuses[i] = False
						continue

				# foreigners
				if 'foreigners' in filters:
					if (not 'foreigners' in marker) or (not marker['foreigners']):
						statuses[i] = False
						continue

				# electricity
				if 'electricity' in filters:
					if (not 'electricity' in marker) or (not marker['electricity']):
						statuses[i] = False
						continue

				# gas
				if  'gas' in filters:
					if (not 'gas' in marker) or (not marker['gas']):
						statuses[i] = False
						continue

				# hot water
				if 'hot_water' in filters:
					if (not 'hot_water' in marker) or (not marker['hot_water']):
						statuses[i] = False
						continue

				# cold water
				if  'cold_water' in filters:
					if (not 'cold_water' in marker) or (not marker['cold_water']):
						statuses[i] = False
						continue

				# lift
				if 'lift' in filters:
					if (not 'lift' in marker) or (not marker['lift']):
						statuses[i] = False
						continue

		else:
			raise InvalidArgument('Invalid conditions. Operation_sid is unexpected.')

		result = []
		for i in range(len(statuses)):
			if statuses[i]:
				result.append(publications[i])
		return result



class ApartmentsMarkersManager(BaseMarkersManager):
	def __init__(self):
		super(ApartmentsMarkersManager, self).__init__(OBJECTS_TYPES.apartments())


	def record_min_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'hash_id',
			'for_sale', 'for_rent',
			'sale_terms__price', 'sale_terms__currency_sid',

			'rent_terms__price', 'rent_terms__currency_sid', 'rent_terms__period_sid',
		    'rent_terms__persons_count', 'rent_terms__family', 'rent_terms__foreigners',

			'body__electricity', 'body__gas', 'body__hot_water', 'body__cold_water', 'body__lift',
			'body__market_type_sid', 'body__heating_type_sid', 'body__rooms_planning_sid',
			'body__rooms_count', 'body__total_area', 'body__floors_count')


	def serialize_publication(self, record):
		if True not in (record.for_sale, record.for_rent):
			raise self.SerializationError('Object must be "for sale", "for rent", or both. Nothing selected.')

		if record.body.rooms_count is None:
			raise self.SerializationError('rooms_count is required but absent.')

		if record.body.total_area is None:
			raise self.SerializationError('total_area is required but absent.')


		data = [
			record.hash_id,
			record.for_sale,
		    record.for_rent,

			record.body.rooms_count,
			float(record.body.total_area), # json can't handle decimal

			record.body.electricity,
		    record.body.gas,
		    record.body.hot_water,
		    record.body.cold_water,
		    record.body.lift,

		    record.body.market_type_sid,
		    record.body.heating_type_sid,
		    record.body.rooms_planning_sid,
			record.body.floor_type_sid,
		]

		# Поле поверху може бути пустим, якщо тип поверху вибрано як "мансарда" чи "цоколь".
		# Якщо воно пусте — немає змісту його сериалізувати.
		if record.body.floor_type_sid == FLOOR_TYPES.floor():
			data.append(record.body.floor)


		if record.for_sale:
			if record.sale_terms.price is None:
				raise self.SerializationError('sale_price is required but absent.')

			data.extend([
		        float(record.sale_terms.price), # json can't handle decimal
			    record.sale_terms.currency_sid,
			])


		if record.for_rent:
			data.extend([
				float(record.rent_terms.price), # json can't handle decimal
			    record.rent_terms.currency_sid,
				record.rent_terms.period_sid,
			    record.rent_terms.persons_count, # WARN: необов’язкове поле

			    record.rent_terms.family,
			    record.rent_terms.foreigners,
			])


		digest = json.dumps(data).replace('true', 't').replace('false', 'f').replace(' ', '')
		return digest


	def deserialize_marker_data(self, data):
		data = json.loads(data.replace('t', 'true').replace('f', 'false'))

		index = iter(xrange(0, len(data)))
		deserialized_data = {
			'hash_id':              data[next(index)],
			'for_sale':             data[next(index)],
		    'for_rent':             data[next(index)],

			'rooms_count':          data[next(index)],
		    'total_area':           data[next(index)],

			'electricity':          data[next(index)],
		    'gas':                  data[next(index)],
		    'hot_water':            data[next(index)],
		    'cold_water':           data[next(index)],
		    'lift':                 data[next(index)],

			'market_type_sid':      data[next(index)],
			'heating_type_sid':     data[next(index)],
			'rooms_planning_sid':   data[next(index)],
			'floor_type_sid':       data[next(index)],
		}
		if deserialized_data['floor_type_sid'] == FLOOR_TYPES.floor():
			deserialized_data['floor'] = data[next(index)]


		if deserialized_data['for_sale']:
			deserialized_data.update({
				'sale_price': data[next(index)],
				'sale_currency_sid': data[next(index)],
			})


		if deserialized_data['for_rent']:
			deserialized_data.update({
				'rent_price': data[next(index)],
				'rent_currency_sid': data[next(index)],
				'rent_period_sid': data[next(index)],
			    'persons_count': data[next(index)],

				'family': data[next(index)],
				'foreigners': data[next(index)],
			})


		return deserialized_data


	def marker_brief(self, marker, filters=None):
		"""
		Сформує бриф для маркеру на основі даних, переданих у фільтрі.
		(В даний момент враховується лише валюта запиту)
		"""

		# todo: додати зміну видачі в залежності від фільтрів.
		# Наприклад, якщо задано к-сть кімнат від 1 до 1 - нема змісту показувати в брифі к-сть кімнат,
		# ітак ясно, що їх буде не більше одної.

		result = {
			'id': marker['hash_id']
		}

		# Гривня як базова валюта обирається згідно з чинним законодавством,
		# але якщо у фільтрі вказана інша - переформатувати бриф на неї.
		if filters is None:
			currency = CURRENCIES.uah()
		else:
			currency = filters.get('currency_sid', CURRENCIES.uah())


		if marker.get('for_sale', False):
			sale_price = self.format_price(marker['sale_price'], marker['sale_currency_sid'], currency)
			result.update({
				'd0': u'Комнат: {0}'.format(marker.get('rooms_count')) \
						if marker.get('rooms_count') else 'Комнат: не указано',
				'd1': u'{0} {1}'.format(sale_price, self.format_currency(currency)),
			})
			return result

		elif marker.get('for_rent', False):
			rent_price = self.format_price(marker['rent_price'], marker['rent_currency_sid'], currency)
			result.update({
				'd0': u'Мест: {0}'.format(marker.get('persons_count')) \
						if marker.get('persons_count') else u'Мест: не указано',
				'd1': u'{0} {1}'.format(rent_price, self.format_currency(currency)),
			})
			return result

		raise RuntimeException('Marker is not for sale and not for rent.')


	def filter(self, publications, filters):
		# WARNING:
		# дана функція для економії часу виконання не виконує deepcopy над publications

		if filters is None:
			return publications

		operation_sid = filters.get('operation_sid')
		if operation_sid is None:
			raise InvalidArgument('Invalid conditions. Operation_sid is absent.')


		# Перед фільтруванням оголошень слід перевірити цілісність і коректність об’єкту умов.
		# На даному етапі виконується перевірка всіх обов’язкових полів filters.
		# Дану перевірку винесено за цикл фільтрування щоб підвищити швидкодію,
		# оскільки об’єкт filters не змінюється в ході фільтрування і достатньо перевіріити його лише раз.
		currency_sid = filters.get('currency_sid')
		if currency_sid is None:
			# Перевіряти фільтри цін має зміст лише тоді, коли задано валюту фільтру,
			# інакше неможливо привести валюту ціни з фільтра до валюти з оголошення.
			# На фронтенді валюта повинна бути задана за замовчуванням.
			raise InvalidArgument('sale_currency_sid is absent.')
		elif currency_sid not in CURRENCIES.values():
			raise InvalidArgument('currency_sid is invalid.')

		if operation_sid == 1: # rent
			rent_period_sid = filters.get('period_sid')
			if rent_period_sid is None:
				raise InvalidArgument('Rent period sid is absent.')


		# Для відбору елементів зі списку publications, використовується список statuses.
		# Кість елементів цього списку відповідає к-сті елементів publications.
		# На початку фільтрування всі елементи statuses встановлені в True.
		# Під час фільтрування деякі з них будуть встановлені в False.
		# На завершальному етапі зі списку publications будуть відібрані лише ті елементи,
		# відповідний елемент statuses яких встановлений в True.
		#
		# Додатковий список використовується для підвищення швидкодії фільтрування,
		# оскільки зміна True/False відбуваєтсья в рази швидше, ніж вилучення елементів зі списку
		# з повторною його перебудовою на кожній перевірці та ітерації.
		statuses = [True] * len(publications)


		# sale filters
		if operation_sid == 0:
			for i in range(len(statuses)):
				# Якщо даний запис вже позначений як виключений — не аналізувати його.
				if not statuses[i]:
					continue

				marker = publications[i][1]

				# operation type
				if not marker.get('for_sale', False):
					statuses[i] = False
					continue


				# sale price
				price_min = filters.get('price_from')
				price_max = filters.get('price_to')
				if price_min is not None:
					price_min = convert_currency(price_min, currency_sid, marker['sale_currency_sid'])
				if price_max is not None:
					price_max = convert_currency(price_max, currency_sid, marker['sale_currency_sid'])


				if (price_max is not None) and (price_min is not None):
					if not price_min <= marker['sale_price'] <= price_max:
						statuses[i] = False
						continue

				elif price_min is not None:
					if not price_min <= marker['sale_price']:
						statuses[i] = False
						continue

				elif price_max is not None:
					if not marker['sale_price'] <= price_max:
						statuses[i] = False
						continue


				# market type
				if ('new_buildings' in filters) and ('secondary_market' in filters):
					# Немає змісту фільтрувати.
					# Під дані умови потрапляють всі об’єкти.
					pass

				elif 'new_buildings' in filters:
					statuses[i] = (marker['market_type_sid'] == MARKET_TYPES.new_building())
				elif 'new_buildings' in filters:
					statuses[i] = (marker['market_type_sid'] == MARKET_TYPES.secondary_market())


				# rooms count
				rooms_count_min = filters.get('rooms_count_from')
				rooms_count_max = filters.get('rooms_count_to')
				rooms_count = marker.get('rooms_count')

				if (rooms_count_max is not None) or (rooms_count_min is not None):
					# Поле "к-сть кімнат" не обов’язкове.
					# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
					# відхилити запис через неможливість аналізу.
					if rooms_count is None:
						statuses[i] = False
						continue


				if (rooms_count_max is not None) and (rooms_count_min is not None):
					if not rooms_count_min <= rooms_count <= rooms_count_max:
						statuses[i] = False
						continue

				elif rooms_count_min is not None:
					if not rooms_count_min <= rooms_count:
						statuses[i] = False
						continue

				elif rooms_count_max is not None:
					if not rooms_count <= rooms_count_max:
						statuses[i] = False
						continue


				# total area
				total_area_min = filters.get('total_area_from')
				total_area_max = filters.get('total_area_to')
				total_area = marker.get('total_area')

				if (total_area_max is not None) or (total_area_min is not None):
					# Поле "загальна площа" може бути не обов’язковим.
					# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
					# відхилити запис через неможливість аналізу.
					if total_area is None:
						statuses[i] = False
						continue


				if (total_area_max is not None) and (total_area_min is not None):
					if not total_area_min <= total_area <= total_area_max:
						statuses[i] = False
						continue

				elif total_area_min is not None:
					if not total_area_min <= total_area:
						statuses[i] = False
						continue

				elif total_area_max is not None:
					if not total_area <= total_area_max:
						statuses[i] = False
						continue


				# floor
				floor_min = filters.get('floor_from')
				floor_max = filters.get('floor_to')
				floor = marker.get('floor')

				if (floor_max is not None) or (floor_max is not None):
					# Поле "к-сть поверхів" не обов’язкове.
					# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
					# відхилити запис через неможливість аналізу.
					if floor is None:
						statuses[i] = False
						continue


				if (floor_min is not None) and (floor_max is not None):
					if not floor_min <= floor <= floor_max:
						statuses[i] = False
						continue

				elif floor_min is not None:
					if not floor_min <= floor:
						statuses[i] = False
						continue

				elif floor_max is not None:
					if not floor <= floor_max:
						statuses[i] = False
						continue


				# rooms planning
				rooms_planning_sid = filters.get('rooms_planning_sid')
				if rooms_planning_sid is not None:
					if rooms_planning_sid == 1: # свободная планировка
						if marker['rooms_planning_sid'] != FLAT_ROOMS_PLANNINGS.free():
							statuses[i] = False
							continue

					elif rooms_planning_sid == 2: # предварительная
						if marker['rooms_planning_sid'] == FLAT_ROOMS_PLANNINGS.free():
							statuses[i] = False
							continue


				# electricity
				if 'electricity' in filters:
					if (not 'electricity' in marker) or (not marker['electricity']):
						statuses[i] = False
						continue

				# gas
				if  'gas' in filters:
					if (not 'gas' in marker) or (not marker['gas']):
						statuses[i] = False
						continue

				# hot water
				if 'hot_water' in filters:
					if (not 'hot_water' in marker) or (not marker['hot_water']):
						statuses[i] = False
						continue

				# cold water
				if  'cold_water' in filters:
					if (not 'cold_water' in marker) or (not marker['cold_water']):
						statuses[i] = False
						continue

				# lift
				if 'lift' in filters:
					if (not 'lift' in marker) or (not marker['lift']):
						statuses[i] = False
						continue


				# heating type
				heating_type_sid = filters.get('heating_type_sid')
				if heating_type_sid is not None:
					# Поле "тип опалення" може бути не обов’язковим.
					# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
					# відхилити запис через неможливість аналізу.
					if 'heating_type_sid' not in marker:
						statuses[i] = False
						continue

					if heating_type_sid == 1: # центральне
						if marker['heating_type_sid'] != HEATING_TYPES.central():
							statuses[i] = False
							continue

					elif heating_type_sid == 2: # індивідуальне
						if marker['heating_type_sid'] != HEATING_TYPES.individual():
							statuses[i] = False
							continue

					elif heating_type_sid == 3: # відсутнє
						if marker['heating_type_sid'] != HEATING_TYPES.none():
							statuses[i] = False
							continue


		# rent filters
		elif operation_sid == 1:
			for i in range(len(publications)):
				# Якщо даний маркер вже позначений як виключений — не аналізувати його.
				if not statuses[i]:
					continue

				marker = publications[i][1]


				# operation type
				if not marker.get('for_rent', False):
					statuses[i] = False
					continue


				# rent price
				price_min = filters.get('price_from')
				price_max = filters.get('price_to')
				if price_min is not None:
					price_min = convert_currency(price_min, currency_sid, marker['rent_currency_sid'])
				if price_max is not None:
					price_max = convert_currency(price_max, currency_sid, marker['rent_currency_sid'])


				if (price_max is not None) and (price_min is not None):
					if not price_min <= marker['rent_price'] <= price_max:
						statuses[i] = False
						continue

				elif price_min is not None:
					if not price_min <= marker['rent_price']:
						statuses[i] = False
						continue

				elif price_max is not None:
					if not marker['rent_price'] <= price_max:
						statuses[i] = False
						continue


				# rent period
				if not 'rent_period_sid' in marker:
					statuses[i] = False
					continue

				if rent_period_sid == 1:
					# посуточно
					if marker['rent_period_sid'] != LIVING_RENT_PERIODS.daily():
						statuses[i] = False
						continue

				elif rent_period_sid == 2:
					# помісячно і довгострокова оренда
					if (marker['rent_period_sid'] != LIVING_RENT_PERIODS.monthly()) or \
							(marker['rent_period_sid'] != LIVING_RENT_PERIODS.long_period()):
						statuses[i] = False
						continue


				# persons_count
				persons_count_min = filters.get('persons_count_from')
				persons_count_max = filters.get('persons_count_to')
				persons_count = marker.get('persons_count')

				if (persons_count_min is not None) or (persons_count_max is not None):
					# Поле "к-сть місць"може бути не обов’язковим.
					# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
					# відхилити запис через неможливість аналізу.
					if persons_count is None:
						statuses[i] = False
						continue


				if (persons_count_min is not None) and (persons_count_max is not None):
					if not persons_count_min <= persons_count <= persons_count_max:
						statuses[i] = False
						continue

				elif persons_count_min is not None:
					if not persons_count_min <= persons_count:
						statuses[i] = False
						continue

				elif persons_count_max is not None:
					if not persons_count <= persons_count_max:
						statuses[i] = False
						continue


				# for family
				if 'family' in filters:
					if (not 'for_family' in marker) or (not marker['for_family']):
						statuses[i] = False
						continue

				# foreigners
				if 'foreigners' in filters:
					if (not 'foreigners' in marker) or (not marker['foreigners']):
						statuses[i] = False
						continue

				# electricity
				if 'electricity' in filters:
					if (not 'electricity' in marker) or (not marker['electricity']):
						statuses[i] = False
						continue

				# gas
				if  'gas' in filters:
					if (not 'gas' in marker) or (not marker['gas']):
						statuses[i] = False
						continue

				# hot water
				if 'hot_water' in filters:
					if (not 'hot_water' in marker) or (not marker['hot_water']):
						statuses[i] = False
						continue

				# cold water
				if  'cold_water' in filters:
					if (not 'cold_water' in marker) or (not marker['cold_water']):
						statuses[i] = False
						continue

				# lift
				if 'lift' in filters:
					if (not 'lift' in marker) or (not marker['lift']):
						statuses[i] = False
						continue

		else:
			raise InvalidArgument('Invalid conditions. Operation_sid is unexpected.')

		result = []
		for i in range(len(statuses)):
			if statuses[i]:
				result.append(publications[i])
		return result



class HousesMarkersManager(BaseMarkersManager):
	def __init__(self):
		super(HousesMarkersManager, self).__init__(OBJECTS_TYPES.house())


	def record_min_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'hash_id',
			'for_sale', 'for_rent',
			'sale_terms__price', 'sale_terms__currency_sid',

			'rent_terms__price', 'rent_terms__currency_sid', 'rent_terms__period_sid',
		    'rent_terms__persons_count', 'rent_terms__family', 'rent_terms__foreigners',

			'body__electricity', 'body__gas', 'body__sewerage', 'body__hot_water', 'body__cold_water',
			'body__market_type_sid', 'body__heating_type_sid',
			'body__rooms_count', 'body__floors_count')


	def serialize_publication(self, record):
		if True not in (record.for_sale, record.for_rent):
			raise self.SerializationError('Object must be "for sale", "for rent", or both. Nothing selected.')

		if record.body.rooms_count is None:
			raise self.SerializationError('rooms_count is required but absent.')

		if record.body.total_area is None:
			raise self.SerializationError('total_area is required but absent.')


		data = [
			record.hash_id,
			record.for_sale,
		    record.for_rent,

			record.body.rooms_count,
		    record.body.floors_count,
			float(record.body.total_area), # json can't handle decimal


			record.body.electricity,
		    record.body.gas,
		    record.body.sewerage,
		    record.body.hot_water,
		    record.body.cold_water,

		    record.body.market_type_sid,
		    record.body.heating_type_sid,
		]

		# Поле поверху може бути пустим, якщо тип поверху вибрано як "мансарда" чи "цоколь".
		# Якщо воно пусте — немає змісту його сериалізувати.
		if record.body.floor_type_sid == FLOOR_TYPES.floor():
			data.append(record.body.floor)


		if record.for_sale:
			if record.sale_terms.price is None:
				raise self.SerializationError('sale_price is required but absent.')

			data.extend([
		        float(record.sale_terms.price), # json can't handle decimal
			    record.sale_terms.currency_sid,
			])


		if record.for_rent:
			data.extend([
				float(record.rent_terms.price), # json can't handle decimal
			    record.rent_terms.currency_sid,
				record.rent_terms.period_sid,
			    record.rent_terms.persons_count, # WARN: необов’язкове поле

			    record.rent_terms.family,
			    record.rent_terms.foreigners,
			])


		digest = json.dumps(data).replace('true', 't').replace('false', 'f').replace(' ', '')
		return digest


	def deserialize_marker_data(self, data):
		data = json.loads(data.replace('t', 'true').replace('f', 'false'))

		index = iter(xrange(0, len(data)))
		deserialized_data = {
			'hash_id':              data[next(index)],
			'for_sale':             data[next(index)],
		    'for_rent':             data[next(index)],

			'rooms_count':          data[next(index)],
		    'floors_count':         data[next(index)],
		    'total_area':           data[next(index)],

			'electricity':          data[next(index)],
		    'gas':                  data[next(index)],
		    'sewerage':             data[next(index)],
		    'hot_water':            data[next(index)],
		    'cold_water':           data[next(index)],

			'market_type_sid':      data[next(index)],
			'heating_type_sid':     data[next(index)],
		}


		if deserialized_data['for_sale']:
			deserialized_data.update({
				'sale_price': data[next(index)],
				'sale_currency_sid': data[next(index)],
			})


		if deserialized_data['for_rent']:
			deserialized_data.update({
				'rent_price': data[next(index)],
				'rent_currency_sid': data[next(index)],
				'rent_period_sid': data[next(index)],
			    'persons_count': data[next(index)],

				'family': data[next(index)],
				'foreigners': data[next(index)],
			})


		return deserialized_data


	def marker_brief(self, marker, filters=None):
		"""
		Сформує бриф для маркеру на основі даних, переданих у фільтрі.
		(В даний момент враховується лише валюта запиту)
		"""

		# todo: додати зміну видачі в залежності від фільтрів.
		# Наприклад, якщо задано к-сть кімнат від 1 до 1 - нема змісту показувати в брифі к-сть кімнат,
		# ітак ясно, що їх буде не більше одної.

		result = {
			'id': marker['hash_id']
		}

		# Гривня як базова валюта обирається згідно з чинним законодавством,
		# але якщо у фільтрі вказана інша - переформатувати бриф на неї.
		if filters is None:
			currency = CURRENCIES.uah()
		else:
			currency = filters.get('currency_sid', CURRENCIES.uah())


		if marker.get('for_sale', False):
			total_area = '{0}'.format(marker.get('total_area')).rstrip('0').rstrip('.')
			sale_price = self.format_price(marker['sale_price'], marker['sale_currency_sid'], currency)
			result.update({
				'd0': u'{0} м²'.format(total_area),
				'd1': u'{0} {1}'.format(sale_price, self.format_currency(currency)),
			})
			return result

		elif marker.get('for_rent', False):
			rent_price = self.format_price(marker['rent_price'], marker['rent_currency_sid'], currency)
			result.update({
				'd0': u'Мест: {0}'.format(marker.get('persons_count')) \
						if marker.get('persons_count') else u'Мест: не указано',
				'd1': u'{0} {1}'.format(rent_price, self.format_currency(currency)),
			})
			return result

		raise RuntimeException('Marker is not for sale and not for rent.')


	def filter(self, publications, filters):
		# WARNING:
		# дана функція для економії часу виконання не виконує deepcopy над publications

		if filters is None:
			return publications

		operation_sid = filters.get('operation_sid')
		if operation_sid is None:
			raise InvalidArgument('Invalid conditions. Operation_sid is absent.')


		# Перед фільтруванням оголошень слід перевірити цілісність і коректність об’єкту умов.
		# На даному етапі виконується перевірка всіх обов’язкових полів filters.
		# Дану перевірку винесено за цикл фільтрування щоб підвищити швидкодію,
		# оскільки об’єкт filters не змінюється в ході фільтрування і достатньо перевіріити його лише раз.
		currency_sid = filters.get('currency_sid')
		if currency_sid is None:
			# Перевіряти фільтри цін має зміст лише тоді, коли задано валюту фільтру,
			# інакше неможливо привести валюту ціни з фільтра до валюти з оголошення.
			# На фронтенді валюта повинна бути задана за замовчуванням.
			raise InvalidArgument('sale_currency_sid is absent.')
		elif currency_sid not in CURRENCIES.values():
			raise InvalidArgument('currency_sid is invalid.')

		if operation_sid == 1: # rent
			rent_period_sid = filters.get('period_sid')
			if rent_period_sid is None:
				raise InvalidArgument('Rent period sid is absent.')
			else:
				rent_period_sid = int(rent_period_sid)



		# Для відбору елементів зі списку publications, використовується список statuses.
		# Кість елементів цього списку відповідає к-сті елементів publications.
		# На початку фільтрування всі елементи statuses встановлені в True.
		# Під час фільтрування деякі з них будуть встановлені в False.
		# На завершальному етапі зі списку publications будуть відібрані лише ті елементи,
		# відповідний елемент statuses яких встановлений в True.
		#
		# Додатковий список використовується для підвищення швидкодії фільтрування,
		# оскільки зміна True/False відбуваєтсья в рази швидше, ніж вилучення елементів зі списку
		# з повторною його перебудовою на кожній перевірці та ітерації.
		statuses = [True] * len(publications)


		# sale filters
		if operation_sid == 0:
			for i in range(len(statuses)):
				# Якщо даний запис вже позначений як виключений — не аналізувати його.
				if not statuses[i]:
					continue

				marker = publications[i][1]

				# operation type
				if not marker.get('for_sale', False):
					statuses[i] = False
					continue

				# sale price
				price_min = filters.get('price_from')
				price_max = filters.get('price_to')
				if price_min is not None:
					price_min = convert_currency(price_min, currency_sid, marker['sale_currency_sid'])
				if price_max is not None:
					price_max = convert_currency(price_max, currency_sid, marker['sale_currency_sid'])


				if (price_max is not None) and (price_min is not None):
					if not price_min <= marker['sale_price'] <= price_max:
						statuses[i] = False
						continue

				elif price_min is not None:
					if not price_min <= marker['sale_price']:
						statuses[i] = False
						continue

				elif price_max is not None:
					if not marker['sale_price'] <= price_max:
						statuses[i] = False
						continue


				# market type
				if ('new_buildings' in filters) and ('secondary_market' in filters):
					# Немає змісту фільтрувати.
					# Під дані умови потрапляють всі об’єкти.
					pass

				elif 'new_buildings' in filters:
					statuses[i] = (marker['market_type_sid'] == MARKET_TYPES.new_building())
				elif 'new_buildings' in filters:
					statuses[i] = (marker['market_type_sid'] == MARKET_TYPES.secondary_market())


				# rooms count
				rooms_count_min = filters.get('rooms_count_from')
				rooms_count_max = filters.get('rooms_count_to')
				rooms_count = marker.get('rooms_count')

				if (rooms_count_max is not None) or (rooms_count_min is not None):
					# Поле "к-сть кімнат" не обов’язкове.
					# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
					# відхилити запис через неможливість аналізу.
					if rooms_count is None:
						statuses[i] = False
						continue


				if (rooms_count_max is not None) and (rooms_count_min is not None):
					if not rooms_count_min <= rooms_count <= rooms_count_max:
						statuses[i] = False
						continue

				elif rooms_count_min is not None:
					if not rooms_count_min <= rooms_count:
						statuses[i] = False
						continue

				elif rooms_count_max is not None:
					if not rooms_count <= rooms_count_max:
						statuses[i] = False
						continue


				# floors count
				floors_count_min = filters.get('floors_count_from')
				floors_count_max = filters.get('floors_count_to')
				floors_count = marker.get('floors_count')

				if (floors_count_max is not None) or (floors_count_max is not None):
					# Поле "к-сть поверхів" не обов’язкове.
					# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
					# відхилити запис через неможливість аналізу.
					if floors_count is None:
						statuses[i] = False
						continue


				if (floors_count_min is not None) and (floors_count_max is not None):
					if not floors_count_min <= floors_count <= floors_count_max:
						statuses[i] = False
						continue

				elif floors_count_min is not None:
					if not floors_count_min <= floors_count:
						statuses[i] = False
						continue

				elif floors_count_max is not None:
					if not floors_count <= floors_count_max:
						statuses[i] = False
						continue


				# electricity
				if 'electricity' in filters:
					if (not 'electricity' in marker) or (not marker['electricity']):
						statuses[i] = False
						continue

				# gas
				if  'gas' in filters:
					if (not 'gas' in marker) or (not marker['gas']):
						statuses[i] = False
						continue

				# hot water
				if 'hot_water' in filters:
					if (not 'hot_water' in marker) or (not marker['hot_water']):
						statuses[i] = False
						continue

				# cold water
				if  'cold_water' in filters:
					if (not 'cold_water' in marker) or (not marker['cold_water']):
						statuses[i] = False
						continue

				# sewerage
				if 'sewerage' in filters:
					if (not 'sewerage' in marker) or (not marker['sewerage']):
						statuses[i] = False
						continue


				# heating type
				heating_type_sid = filters.get('heating_type_sid')
				if heating_type_sid is not None:
					# Поле "тип опалення" може бути не обов’язковим.
					# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
					# відхилити запис через неможливість аналізу.
					if 'heating_type_sid' not in marker:
						statuses[i] = False
						continue

					if heating_type_sid == 1:
						# пристунє
						if marker['heating_type_sid'] not in [HEATING_TYPES.central(), HEATING_TYPES.individual()]:
							statuses[i] = False
							continue

					elif heating_type_sid == 2:
						# вісдутнє
						if marker['heating_type_sid'] != HEATING_TYPES.none():
							statuses[i] = False
							continue


		# rent filters
		elif operation_sid == 1:
			for i in range(len(publications)):
				# Якщо даний маркер вже позначений як виключений — не аналізувати його.
				if not statuses[i]:
					continue

				marker = publications[i][1]


				# operation type
				if not marker.get('for_rent', False):
					statuses[i] = False
					continue


				# rent price
				price_min = filters.get('price_from')
				price_max = filters.get('price_to')
				if price_min is not None:
					price_min = convert_currency(price_min, currency_sid, marker['rent_currency_sid'])
				if price_max is not None:
					price_max = convert_currency(price_max, currency_sid, marker['rent_currency_sid'])


				if (price_max is not None) and (price_min is not None):
					if not price_min <= marker['rent_price'] <= price_max:
						statuses[i] = False
						continue

				elif price_min is not None:
					if not price_min <= marker['rent_price']:
						statuses[i] = False
						continue

				elif price_max is not None:
					if not marker['rent_price'] <= price_max:
						statuses[i] = False
						continue


				# rent period
				if not 'rent_period_sid' in marker:
					statuses[i] = False
					continue

				if rent_period_sid == 1:
					# посуточно
					if marker['rent_period_sid'] != LIVING_RENT_PERIODS.daily():
						statuses[i] = False
						continue

				elif rent_period_sid == 2:
					# помісячно і довгострокова оренда
					if (marker['rent_period_sid'] != LIVING_RENT_PERIODS.monthly()) or \
							(marker['rent_period_sid'] != LIVING_RENT_PERIODS.long_period()):
						statuses[i] = False
						continue


				# persons_count
				persons_count_min = filters.get('persons_count_from')
				persons_count_max = filters.get('persons_count_to')
				persons_count = marker.get('persons_count')

				if (persons_count_min is not None) or (persons_count_max is not None):
					# Поле "к-сть місць"може бути не обов’язковим.
					# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
					# відхилити запис через неможливість аналізу.
					if persons_count is None:
						statuses[i] = False
						continue


				if (persons_count_min is not None) and (persons_count_max is not None):
					if not persons_count_min <= persons_count <= persons_count_max:
						statuses[i] = False
						continue

				elif persons_count_min is not None:
					if not persons_count_min <= persons_count:
						statuses[i] = False
						continue

				elif persons_count_max is not None:
					if not persons_count <= persons_count_max:
						statuses[i] = False
						continue


				# for family
				if 'family' in filters:
					if (not 'for_family' in marker) or (not marker['for_family']):
						statuses[i] = False
						continue

				# foreigners
				if 'foreigners' in filters:
					if (not 'foreigners' in marker) or (not marker['foreigners']):
						statuses[i] = False
						continue

				# electricity
				if 'electricity' in filters:
					if (not 'electricity' in marker) or (not marker['electricity']):
						statuses[i] = False
						continue

				# gas
				if  'gas' in filters:
					if (not 'gas' in marker) or (not marker['gas']):
						statuses[i] = False
						continue

				# hot water
				if 'hot_water' in filters:
					if (not 'hot_water' in marker) or (not marker['hot_water']):
						statuses[i] = False
						continue

				# cold water
				if  'cold_water' in filters:
					if (not 'cold_water' in marker) or (not marker['cold_water']):
						statuses[i] = False
						continue

		else:
			raise InvalidArgument('Invalid conditions. Operation_sid is unexpected.')

		result = []
		for i in range(len(statuses)):
			if statuses[i]:
				result.append(publications[i])
		return result



class CottagesMarkersManager(BaseMarkersManager):
	def __init__(self):
		super(CottagesMarkersManager, self).__init__(OBJECTS_TYPES.cottage())


	def record_min_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'hash_id',
			'for_sale', 'for_rent',
			'sale_terms__price', 'sale_terms__currency_sid',

			'rent_terms__price', 'rent_terms__currency_sid', 'rent_terms__period_sid',
		    'rent_terms__persons_count', 'rent_terms__family', 'rent_terms__foreigners',

			'body__electricity', 'body__gas', 'body__sewerage', 'body__hot_water', 'body__cold_water',
			'body__market_type_sid', 'body__heating_type_sid',
			'body__rooms_count', 'body__floors_count')


	def serialize_publication(self, record):
		if True not in (record.for_sale, record.for_rent):
			raise self.SerializationError('Object must be "for sale", "for rent", or both. Nothing selected.')

		if record.body.rooms_count is None:
			raise self.SerializationError('rooms_count is required but absent.')

		if record.body.total_area is None:
			raise self.SerializationError('total_area is required but absent.')


		data = [
			record.hash_id,
			record.for_sale,
		    record.for_rent,

			record.body.rooms_count,
		    record.body.floors_count,
			float(record.body.total_area), # json can't handle decimal


			record.body.electricity,
		    record.body.gas,
		    record.body.sewerage,
		    record.body.hot_water,
		    record.body.cold_water,

		    record.body.market_type_sid,
		    record.body.heating_type_sid,
		]

		# Поле поверху може бути пустим, якщо тип поверху вибрано як "мансарда" чи "цоколь".
		# Якщо воно пусте — немає змісту його сериалізувати.
		if record.body.floor_type_sid == FLOOR_TYPES.floor():
			data.append(record.body.floor)


		if record.for_sale:
			if record.sale_terms.price is None:
				raise self.SerializationError('sale_price is required but absent.')

			data.extend([
		        float(record.sale_terms.price), # json can't handle decimal
			    record.sale_terms.currency_sid,
			])


		if record.for_rent:
			data.extend([
				float(record.rent_terms.price), # json can't handle decimal
			    record.rent_terms.currency_sid,
				record.rent_terms.period_sid,
			    record.rent_terms.persons_count, # WARN: необов’язкове поле

			    record.rent_terms.family,
			    record.rent_terms.foreigners,
			])


		digest = json.dumps(data).replace('true', 't').replace('false', 'f').replace(' ', '')
		return digest


	def deserialize_marker_data(self, data):
		data = json.loads(data.replace('t', 'true').replace('f', 'false'))

		index = iter(xrange(0, len(data)))
		deserialized_data = {
			'hash_id':              data[next(index)],
			'for_sale':             data[next(index)],
		    'for_rent':             data[next(index)],

			'rooms_count':          data[next(index)],
		    'floors_count':         data[next(index)],
		    'total_area':           data[next(index)],

			'electricity':          data[next(index)],
		    'gas':                  data[next(index)],
		    'sewerage':             data[next(index)],
		    'hot_water':            data[next(index)],
		    'cold_water':           data[next(index)],

			'market_type_sid':      data[next(index)],
			'heating_type_sid':     data[next(index)],
		}


		if deserialized_data['for_sale']:
			deserialized_data.update({
				'sale_price': data[next(index)],
				'sale_currency_sid': data[next(index)],
			})


		if deserialized_data['for_rent']:
			deserialized_data.update({
				'rent_price': data[next(index)],
				'rent_currency_sid': data[next(index)],
				'rent_period_sid': data[next(index)],
			    'persons_count': data[next(index)],

				'family': data[next(index)],
				'foreigners': data[next(index)],
			})


		return deserialized_data


	def marker_brief(self, marker, filters=None):
		"""
		Сформує бриф для маркеру на основі даних, переданих у фільтрі.
		(В даний момент враховується лише валюта запиту)
		"""

		# todo: додати зміну видачі в залежності від фільтрів.
		# Наприклад, якщо задано к-сть кімнат від 1 до 1 - нема змісту показувати в брифі к-сть кімнат,
		# ітак ясно, що їх буде не більше одної.

		result = {
			'id': marker['hash_id']
		}

		# Гривня як базова валюта обирається згідно з чинним законодавством,
		# але якщо у фільтрі вказана інша - переформатувати бриф на неї.
		if filters is None:
			currency = CURRENCIES.uah()
		else:
			currency = filters.get('currency_sid', CURRENCIES.uah())


		if marker.get('for_sale', False):
			sale_price = self.format_price(marker['sale_price'], marker['sale_currency_sid'], currency)
			result.update({
				'd0': u'Комнат: {0}'.format(marker.get('rooms_count')) \
						if marker.get('rooms_count') else 'Комнат: не указано',
				'd1': u'{0} {1}'.format(sale_price, self.format_currency(currency)),
			})
			return result

		elif marker.get('for_rent', False):
			rent_price = self.format_price(marker['rent_price'], marker['rent_currency_sid'], currency)
			result.update({
				'd0': u'Мест: {0}'.format(marker.get('persons_count')) \
						if marker.get('persons_count') else u'Мест: не указано',
				'd1': u'{0} {1}'.format(rent_price, self.format_currency(currency)),
			})
			return result

		raise RuntimeException('Marker is not for sale and not for rent.')


	def filter(self, publications, filters):
		# WARNING:
		# дана функція для економії часу виконання не виконує deepcopy над publications

		if filters is None:
			return publications

		operation_sid = filters.get('operation_sid')
		if operation_sid is None:
			raise InvalidArgument('Invalid conditions. Operation_sid is absent.')


		# Перед фільтруванням оголошень слід перевірити цілісність і коректність об’єкту умов.
		# На даному етапі виконується перевірка всіх обов’язкових полів filters.
		# Дану перевірку винесено за цикл фільтрування щоб підвищити швидкодію,
		# оскільки об’єкт filters не змінюється в ході фільтрування і достатньо перевіріити його лише раз.
		currency_sid = filters.get('currency_sid')
		if currency_sid is None:
			# Перевіряти фільтри цін має зміст лише тоді, коли задано валюту фільтру,
			# інакше неможливо привести валюту ціни з фільтра до валюти з оголошення.
			# На фронтенді валюта повинна бути задана за замовчуванням.
			raise InvalidArgument('sale_currency_sid is absent.')
		elif currency_sid not in CURRENCIES.values():
			raise InvalidArgument('currency_sid is invalid.')

		if operation_sid == 1: # rent
			rent_period_sid = filters.get('period_sid')
			if rent_period_sid is None:
				raise InvalidArgument('Rent period sid is absent.')
			else:
				rent_period_sid = int(rent_period_sid)



		# Для відбору елементів зі списку publications, використовується список statuses.
		# Кість елементів цього списку відповідає к-сті елементів publications.
		# На початку фільтрування всі елементи statuses встановлені в True.
		# Під час фільтрування деякі з них будуть встановлені в False.
		# На завершальному етапі зі списку publications будуть відібрані лише ті елементи,
		# відповідний елемент statuses яких встановлений в True.
		#
		# Додатковий список використовується для підвищення швидкодії фільтрування,
		# оскільки зміна True/False відбуваєтсья в рази швидше, ніж вилучення елементів зі списку
		# з повторною його перебудовою на кожній перевірці та ітерації.
		statuses = [True] * len(publications)


		# sale filters
		if operation_sid == 0:
			for i in range(len(statuses)):
				# Якщо даний запис вже позначений як виключений — не аналізувати його.
				if not statuses[i]:
					continue

				marker = publications[i][1]

				# operation type
				if not marker.get('for_sale', False):
					statuses[i] = False
					continue


				# sale price
				price_min = filters.get('price_from')
				price_max = filters.get('price_to')
				if price_min is not None:
					price_min = convert_currency(price_min, currency_sid, marker['sale_currency_sid'])
				if price_max is not None:
					price_max = convert_currency(price_max, currency_sid, marker['sale_currency_sid'])


				if (price_max is not None) and (price_min is not None):
					if not price_min <= marker['sale_price'] <= price_max:
						statuses[i] = False
						continue

				elif price_min is not None:
					if not price_min <= marker['sale_price']:
						statuses[i] = False
						continue

				elif price_max is not None:
					if not marker['sale_price'] <= price_max:
						statuses[i] = False
						continue


				# market type
				if ('new_buildings' in filters) and ('secondary_market' in filters):
					# Немає змісту фільтрувати.
					# Під дані умови потрапляють всі об’єкти.
					pass

				elif 'new_buildings' in filters:
					statuses[i] = (marker['market_type_sid'] == MARKET_TYPES.new_building())
				elif 'new_buildings' in filters:
					statuses[i] = (marker['market_type_sid'] == MARKET_TYPES.secondary_market())


				# rooms count
				rooms_count_min = filters.get('rooms_count_from')
				rooms_count_max = filters.get('rooms_count_to')
				rooms_count = marker.get('rooms_count')

				if (rooms_count_max is not None) or (rooms_count_min is not None):
					# Поле "к-сть кімнат" не обов’язкове.
					# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
					# відхилити запис через неможливість аналізу.
					if rooms_count is None:
						statuses[i] = False
						continue


				if (rooms_count_max is not None) and (rooms_count_min is not None):
					if not rooms_count_min <= rooms_count <= rooms_count_max:
						statuses[i] = False
						continue

				elif rooms_count_min is not None:
					if not rooms_count_min <= rooms_count:
						statuses[i] = False
						continue

				elif rooms_count_max is not None:
					if not rooms_count <= rooms_count_max:
						statuses[i] = False
						continue


				# floors count
				floors_count_min = filters.get('floors_count_from')
				floors_count_max = filters.get('floors_count_to')
				floors_count = marker.get('floors_count')

				if (floors_count_max is not None) or (floors_count_max is not None):
					# Поле "к-сть поверхів" не обов’язкове.
					# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
					# відхилити запис через неможливість аналізу.
					if floors_count is None:
						statuses[i] = False
						continue


				if (floors_count_min is not None) and (floors_count_max is not None):
					if not floors_count_min <= floors_count <= floors_count_max:
						statuses[i] = False
						continue

				elif floors_count_min is not None:
					if not floors_count_min <= floors_count:
						statuses[i] = False
						continue

				elif floors_count_max is not None:
					if not floors_count <= floors_count_max:
						statuses[i] = False
						continue


				# electricity
				if 'electricity' in filters:
					if (not 'electricity' in marker) or (not marker['electricity']):
						statuses[i] = False
						continue

				# gas
				if  'gas' in filters:
					if (not 'gas' in marker) or (not marker['gas']):
						statuses[i] = False
						continue

				# hot water
				if 'hot_water' in filters:
					if (not 'hot_water' in marker) or (not marker['hot_water']):
						statuses[i] = False
						continue

				# cold water
				if  'cold_water' in filters:
					if (not 'cold_water' in marker) or (not marker['cold_water']):
						statuses[i] = False
						continue

				# sewerage
				if 'sewerage' in filters:
					if (not 'sewerage' in marker) or (not marker['sewerage']):
						statuses[i] = False
						continue


				# heating type
				heating_type_sid = filters.get('heating_type_sid')
				if heating_type_sid is not None:
					# Поле "тип опалення" може бути не обов’язковим.
					# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
					# відхилити запис через неможливість аналізу.
					if 'heating_type_sid' not in marker:
						statuses[i] = False
						continue

					if heating_type_sid == 1:
						# пристунє
						if marker['heating_type_sid'] not in [HEATING_TYPES.central(), HEATING_TYPES.individual()]:
							statuses[i] = False
							continue

					elif heating_type_sid == 2:
						# вісдутнє
						if marker['heating_type_sid'] != HEATING_TYPES.none():
							statuses[i] = False
							continue


		# rent filters
		elif operation_sid == 1:
			for i in range(len(publications)):
				# Якщо даний маркер вже позначений як виключений — не аналізувати його.
				if not statuses[i]:
					continue

				marker = publications[i][1]


				# operation type
				if not marker.get('for_rent', False):
					statuses[i] = False
					continue


				# rent price
				price_min = filters.get('price_from')
				price_max = filters.get('price_to')
				if price_min is not None:
					price_min = convert_currency(price_min, currency_sid, marker['rent_currency_sid'])
				if price_max is not None:
					price_max = convert_currency(price_max, currency_sid, marker['rent_currency_sid'])


				if (price_max is not None) and (price_min is not None):
					if not price_min <= marker['rent_price'] <= price_max:
						statuses[i] = False
						continue

				elif price_min is not None:
					if not price_min <= marker['rent_price']:
						statuses[i] = False
						continue

				elif price_max is not None:
					if not marker['rent_price'] <= price_max:
						statuses[i] = False
						continue


				# rent period
				if not 'rent_period_sid' in marker:
					statuses[i] = False
					continue

				if rent_period_sid == 1:
					# посуточно
					if marker['rent_period_sid'] != LIVING_RENT_PERIODS.daily():
						statuses[i] = False
						continue

				elif rent_period_sid == 2:
					# помісячно і довгострокова оренда
					if (marker['rent_period_sid'] != LIVING_RENT_PERIODS.monthly()) or \
							(marker['rent_period_sid'] != LIVING_RENT_PERIODS.long_period()):
						statuses[i] = False
						continue


				# persons_count
				persons_count_min = filters.get('persons_count_from')
				persons_count_max = filters.get('persons_count_to')
				persons_count = marker.get('persons_count')

				if (persons_count_min is not None) or (persons_count_max is not None):
					# Поле "к-сть місць"може бути не обов’язковим.
					# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
					# відхилити запис через неможливість аналізу.
					if persons_count is None:
						statuses[i] = False
						continue


				if (persons_count_min is not None) and (persons_count_max is not None):
					if not persons_count_min <= persons_count <= persons_count_max:
						statuses[i] = False
						continue

				elif persons_count_min is not None:
					if not persons_count_min <= persons_count:
						statuses[i] = False
						continue

				elif persons_count_max is not None:
					if not persons_count <= persons_count_max:
						statuses[i] = False
						continue


				# for family
				if 'family' in filters:
					if (not 'for_family' in marker) or (not marker['for_family']):
						statuses[i] = False
						continue

				# foreigners
				if 'foreigners' in filters:
					if (not 'foreigners' in marker) or (not marker['foreigners']):
						statuses[i] = False
						continue

				# electricity
				if 'electricity' in filters:
					if (not 'electricity' in marker) or (not marker['electricity']):
						statuses[i] = False
						continue

				# gas
				if  'gas' in filters:
					if (not 'gas' in marker) or (not marker['gas']):
						statuses[i] = False
						continue

				# hot water
				if 'hot_water' in filters:
					if (not 'hot_water' in marker) or (not marker['hot_water']):
						statuses[i] = False
						continue

				# cold water
				if  'cold_water' in filters:
					if (not 'cold_water' in marker) or (not marker['cold_water']):
						statuses[i] = False
						continue

		else:
			raise InvalidArgument('Invalid conditions. Operation_sid is unexpected.')

		result = []
		for i in range(len(statuses)):
			if statuses[i]:
				result.append(publications[i])
		return result



class RoomsMarkersManager(BaseMarkersManager):
	def __init__(self):
		super(RoomsMarkersManager, self).__init__(OBJECTS_TYPES.room())


	def record_min_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'hash_id',
			'for_sale', 'for_rent',
			'sale_terms__price', 'sale_terms__currency_sid',

			'rent_terms__price', 'rent_terms__currency_sid', 'rent_terms__period_sid',
		    'rent_terms__persons_count', 'rent_terms__family', 'rent_terms__foreigners',

			'body__electricity', 'body__gas', 'body__hot_water', 'body__cold_water', 'body__lift',
			'body__market_type_sid', 'body__heating_type_sid', 'body__rooms_planning_sid',
			'body__rooms_count', 'body__total_area', 'body__floor')


	def serialize_publication(self, record):
		if True not in (record.for_sale, record.for_rent):
			raise self.SerializationError('Object must be "for sale", "for rent", or both. Nothing selected.')

		if record.body.rooms_count is None:
			raise self.SerializationError('rooms_count is required but absent.')

		if record.body.total_area is None:
			raise self.SerializationError('total_area is required but absent.')


		data = [
			record.hash_id,
			record.for_sale,
		    record.for_rent,

			record.body.rooms_count,
			float(record.body.total_area), # json can't handle decimal

			record.body.electricity,
		    record.body.gas,
		    record.body.hot_water,
		    record.body.cold_water,
		    record.body.lift,

		    record.body.market_type_sid,
		    record.body.heating_type_sid,
			record.body.floor_type_sid,
		]

		# Поле поверху може бути пустим, якщо тип поверху вибрано як "мансарда" чи "цоколь".
		# Якщо воно пусте — немає змісту його сериалізувати.
		if record.body.floor_type_sid == FLOOR_TYPES.floor():
			data.append(record.body.floor)


		if record.for_sale:
			if record.sale_terms.price is None:
				raise self.SerializationError('sale_price is required but absent.')

			data.extend([
		        float(record.sale_terms.price), # json can't handle decimal
			    record.sale_terms.currency_sid,
			])


		if record.for_rent:
			data.extend([
				float(record.rent_terms.price), # json can't handle decimal
			    record.rent_terms.currency_sid,
				record.rent_terms.period_sid,
			    record.rent_terms.persons_count, # WARN: необов’язкове поле

			    record.rent_terms.family,
			    record.rent_terms.foreigners,
			])


		digest = json.dumps(data).replace('true', 't').replace('false', 'f').replace(' ', '')
		return digest


	def deserialize_marker_data(self, data):
		data = json.loads(data.replace('t', 'true').replace('f', 'false'))

		index = iter(xrange(0, len(data)))
		deserialized_data = {
			'hash_id':              data[next(index)],
			'for_sale':             data[next(index)],
		    'for_rent':             data[next(index)],

			'rooms_count':          data[next(index)],
		    'total_area':           data[next(index)],

			'electricity':          data[next(index)],
		    'gas':                  data[next(index)],
		    'hot_water':            data[next(index)],
		    'cold_water':           data[next(index)],
		    'lift':                 data[next(index)],

			'market_type_sid':      data[next(index)],
			'heating_type_sid':     data[next(index)],
			'floor_type_sid':       data[next(index)],
		}
		if deserialized_data['floor_type_sid'] == FLOOR_TYPES.floor():
			deserialized_data['floor'] = data[next(index)]


		if deserialized_data['for_sale']:
			deserialized_data.update({
				'sale_price': data[next(index)],
				'sale_currency_sid': data[next(index)],
			})


		if deserialized_data['for_rent']:
			deserialized_data.update({
				'rent_price': data[next(index)],
				'rent_currency_sid': data[next(index)],
				'rent_period_sid': data[next(index)],
			    'persons_count': data[next(index)],

				'family': data[next(index)],
				'foreigners': data[next(index)],
			})


		return deserialized_data


	def marker_brief(self, marker, filters=None):
		"""
		Сформує бриф для маркеру на основі даних, переданих у фільтрі.
		(В даний момент враховується лише валюта запиту)
		"""

		# todo: додати зміну видачі в залежності від фільтрів.
		# Наприклад, якщо задано к-сть кімнат від 1 до 1 - нема змісту показувати в брифі к-сть кімнат,
		# ітак ясно, що їх буде не більше одної.

		result = {
			'id': marker['hash_id']
		}

		# Гривня як базова валюта обирається згідно з чинним законодавством,
		# але якщо у фільтрі вказана інша - переформатувати бриф на неї.
		if filters is None:
			currency = CURRENCIES.uah()
		else:
			currency = filters.get('currency_sid', CURRENCIES.uah())


		if marker.get('for_sale', False):
			total_area = '{0:.2f}'.format(marker.get('total_area')).rstrip('0').rstrip('.') \
				if marker.get('total_area') else None
			sale_price = self.format_price(marker['sale_price'], marker['sale_currency_sid'], currency)
			result.update({
			'd0': u'Площадь: {0} м²'.format(total_area) if total_area else u'Площадь неизвестна',
				'd1': u'{0} {1}'.format(sale_price, self.format_currency(currency)),
			})
			return result

		elif marker.get('for_rent', False):
			total_area = '{0:.2f}'.format(marker.get('total_area')).rstrip('0').rstrip('.') \
				if marker.get('total_area') else None
			rent_price = self.format_price(marker['rent_price'], marker['rent_currency_sid'], currency)
			result.update({
				'd0': u'Площадь: {0} м²'.format(total_area) if total_area else u'Площадь неизвестна',
				'd1': u'{0} {1}'.format(rent_price, self.format_currency(currency)),
			})
			return result

		raise RuntimeException('Marker is not for sale and not for rent.')


	def filter(self, publications, filters):
		# WARNING:
		# дана функція для економії часу виконання не виконує deepcopy над publications

		if filters is None:
			return publications

		operation_sid = filters.get('operation_sid')
		if operation_sid is None:
			raise InvalidArgument('Invalid conditions. Operation_sid is absent.')


		# Перед фільтруванням оголошень слід перевірити цілісність і коректність об’єкту умов.
		# На даному етапі виконується перевірка всіх обов’язкових полів filters.
		# Дану перевірку винесено за цикл фільтрування щоб підвищити швидкодію,
		# оскільки об’єкт filters не змінюється в ході фільтрування і достатньо перевіріити його лише раз.
		currency_sid = filters.get('currency_sid')
		if currency_sid is None:
			# Перевіряти фільтри цін має зміст лише тоді, коли задано валюту фільтру,
			# інакше неможливо привести валюту ціни з фільтра до валюти з оголошення.
			# На фронтенді валюта повинна бути задана за замовчуванням.
			raise InvalidArgument('sale_currency_sid is absent.')
		elif currency_sid not in CURRENCIES.values():
			raise InvalidArgument('currency_sid is invalid.')

		if operation_sid == 1: # rent
			rent_period_sid = filters.get('period_sid')
			if rent_period_sid is None:
				raise InvalidArgument('Rent period sid is absent.')


		# Для відбору елементів зі списку publications, використовується список statuses.
		# Кість елементів цього списку відповідає к-сті елементів publications.
		# На початку фільтрування всі елементи statuses встановлені в True.
		# Під час фільтрування деякі з них будуть встановлені в False.
		# На завершальному етапі зі списку publications будуть відібрані лише ті елементи,
		# відповідний елемент statuses яких встановлений в True.
		#
		# Додатковий список використовується для підвищення швидкодії фільтрування,
		# оскільки зміна True/False відбуваєтсья в рази швидше, ніж вилучення елементів зі списку
		# з повторною його перебудовою на кожній перевірці та ітерації.
		statuses = [True] * len(publications)


		# sale filters
		if operation_sid == 0:
			for i in range(len(statuses)):
				# Якщо даний запис вже позначений як виключений — не аналізувати його.
				if not statuses[i]:
					continue

				marker = publications[i][1]

				# operation type
				if not marker.get('for_sale', False):
					statuses[i] = False
					continue

				# sale price
				price_min = filters.get('price_from')
				price_max = filters.get('price_to')
				if price_min is not None:
					price_min = convert_currency(price_min, currency_sid, marker['sale_currency_sid'])
				if price_max is not None:
					price_max = convert_currency(price_max, currency_sid, marker['sale_currency_sid'])


				if (price_max is not None) and (price_min is not None):
					if not price_min <= marker['sale_price'] <= price_max:
						statuses[i] = False
						continue

				elif price_min is not None:
					if not price_min <= marker['sale_price']:
						statuses[i] = False
						continue

				elif price_max is not None:
					if not marker['sale_price'] <= price_max:
						statuses[i] = False
						continue


				# market type
				if ('new_buildings' in filters) and ('secondary_market' in filters):
					# Немає змісту фільтрувати.
					# Під дані умови потрапляють всі об’єкти.
					pass

				elif 'new_buildings' in filters:
					statuses[i] = (marker['market_type_sid'] == MARKET_TYPES.new_building())
				elif 'new_buildings' in filters:
					statuses[i] = (marker['market_type_sid'] == MARKET_TYPES.secondary_market())


				# rooms count
				rooms_count_min = filters.get('rooms_count_from')
				rooms_count_max = filters.get('rooms_count_to')
				rooms_count = marker.get('rooms_count')

				if (rooms_count_max is not None) or (rooms_count_min is not None):
					# Поле "к-сть кімнат" не обов’язкове.
					# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
					# відхилити запис через неможливість аналізу.
					if rooms_count is None:
						statuses[i] = False
						continue


				if (rooms_count_max is not None) and (rooms_count_min is not None):
					if not rooms_count_min <= rooms_count <= rooms_count_max:
						statuses[i] = False
						continue

				elif rooms_count_min is not None:
					if not rooms_count_min <= rooms_count:
						statuses[i] = False
						continue

				elif rooms_count_max is not None:
					if not rooms_count <= rooms_count_max:
						statuses[i] = False
						continue


				# total area
				total_area_min = filters.get('total_area_from')
				total_area_max = filters.get('total_area_to')
				total_area = marker.get('total_area')

				if (total_area_max is not None) or (total_area_min is not None):
					# Поле "загальна площа" може бути не обов’язковим.
					# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
					# відхилити запис через неможливість аналізу.
					if total_area is None:
						statuses[i] = False
						continue


				if (total_area_max is not None) and (total_area_min is not None):
					if not total_area_min <= total_area <= total_area_max:
						statuses[i] = False
						continue

				elif total_area_min is not None:
					if not total_area_min <= total_area:
						statuses[i] = False
						continue

				elif total_area_max is not None:
					if not total_area <= total_area_max:
						statuses[i] = False
						continue


				# floor
				floor_min = filters.get('floor_from')
				floor_max = filters.get('floor_to')
				floor = marker.get('floor')

				if (floor_max is not None) or (floor_max is not None):
					# Поле "к-сть поверхів" не обов’язкове.
					# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
					# відхилити запис через неможливість аналізу.
					if floor is None:
						statuses[i] = False
						continue


				if (floor_min is not None) and (floor_max is not None):
					if not floor_min <= floor <= floor_max:
						statuses[i] = False
						continue

				elif floor_min is not None:
					if not floor_min <= floor:
						statuses[i] = False
						continue

				elif floor_max is not None:
					if not floor <= floor_max:
						statuses[i] = False
						continue


				# electricity
				if 'electricity' in filters:
					if (not 'electricity' in marker) or (not marker['electricity']):
						statuses[i] = False
						continue

				# gas
				if  'gas' in filters:
					if (not 'gas' in marker) or (not marker['gas']):
						statuses[i] = False
						continue

				# hot water
				if 'hot_water' in filters:
					if (not 'hot_water' in marker) or (not marker['hot_water']):
						statuses[i] = False
						continue

				# cold water
				if  'cold_water' in filters:
					if (not 'cold_water' in marker) or (not marker['cold_water']):
						statuses[i] = False
						continue

				# lift
				if 'lift' in filters:
					if (not 'lift' in marker) or (not marker['lift']):
						statuses[i] = False
						continue


				# heating type
				heating_type_sid = filters.get('heating_type_sid')
				if heating_type_sid is not None:
					# Поле "тип опалення" може бути не обов’язковим.
					# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
					# відхилити запис через неможливість аналізу.
					if 'heating_type_sid' not in marker:
						statuses[i] = False
						continue

					if heating_type_sid == 1: # центральне
						if marker['heating_type_sid'] != HEATING_TYPES.central():
							statuses[i] = False
							continue

					elif heating_type_sid == 2: # індивідуальне
						if marker['heating_type_sid'] != HEATING_TYPES.individual():
							statuses[i] = False
							continue

					elif heating_type_sid == 3: # відсутнє
						if marker['heating_type_sid'] != HEATING_TYPES.none():
							statuses[i] = False
							continue


		# rent filters
		elif operation_sid == 1:
			for i in range(len(publications)):
				# Якщо даний маркер вже позначений як виключений — не аналізувати його.
				if not statuses[i]:
					continue

				marker = publications[i][1]

				# operation type
				if not marker.get('for_rent', False):
					statuses[i] = False
					continue

				# rent period
				if not 'rent_period_sid' in marker:
					# Неможливо визначити, чи здається об’єкт в оренду.
					# Виключаємо з видачі.
					statuses[i] = False
					continue

				if rent_period_sid == 1: # посуточно
					if marker['rent_period_sid'] != LIVING_RENT_PERIODS.daily():
						statuses[i] = False
						continue

				elif rent_period_sid == 2: # помісячно і довгострокова оренда
					if (marker['rent_period_sid'] != LIVING_RENT_PERIODS.monthly()) or \
							(marker['rent_period_sid'] != LIVING_RENT_PERIODS.long_period()):
						statuses[i] = False
						continue

				# rent price
				price_min = filters.get('price_from')
				price_max = filters.get('price_to')
				if price_min is not None:
					price_min = convert_currency(price_min, currency_sid, marker['rent_currency_sid'])
				if price_max is not None:
					price_max = convert_currency(price_max, currency_sid, marker['rent_currency_sid'])


				if (price_max is not None) and (price_min is not None):
					if not price_min <= marker['rent_price'] <= price_max:
						statuses[i] = False
						continue

				elif price_min is not None:
					if not price_min <= marker['rent_price']:
						statuses[i] = False
						continue

				elif price_max is not None:
					if not marker['rent_price'] <= price_max:
						statuses[i] = False
						continue

				# persons_count
				persons_count_min = filters.get('persons_count_from')
				persons_count_max = filters.get('persons_count_to')
				persons_count = marker.get('persons_count')

				if (persons_count_min is not None) or (persons_count_max is not None):
					# Поле "к-сть місць"може бути не обов’язковим.
					# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
					# відхилити запис через неможливість аналізу.
					if persons_count is None:
						statuses[i] = False
						continue


				if (persons_count_min is not None) and (persons_count_max is not None):
					if not persons_count_min <= persons_count <= persons_count_max:
						statuses[i] = False
						continue

				elif persons_count_min is not None:
					if not persons_count_min <= persons_count:
						statuses[i] = False
						continue

				elif persons_count_max is not None:
					if not persons_count <= persons_count_max:
						statuses[i] = False
						continue


				# for family
				if 'family' in filters:
					if (not 'for_family' in marker) or (not marker['for_family']):
						statuses[i] = False
						continue

				# foreigners
				if 'foreigners' in filters:
					if (not 'foreigners' in marker) or (not marker['foreigners']):
						statuses[i] = False
						continue

				# lift
				if 'lift' in filters:
					if (not 'lift' in marker) or (not marker['lift']):
						statuses[i] = False
						continue

				# electricity
				if 'electricity' in filters:
					if (not 'electricity' in marker) or (not marker['electricity']):
						statuses[i] = False
						continue

				# gas
				if  'gas' in filters:
					if (not 'gas' in marker) or (not marker['gas']):
						statuses[i] = False
						continue

				# hot water
				if 'hot_water' in filters:
					if (not 'hot_water' in marker) or (not marker['hot_water']):
						statuses[i] = False
						continue

				# cold water
				if  'cold_water' in filters:
					if (not 'cold_water' in marker) or (not marker['cold_water']):
						statuses[i] = False
						continue
		else:
			raise InvalidArgument('Invalid conditions. Operation_sid is unexpected.')

		result = []
		for i in range(len(statuses)):
			if statuses[i]:
				result.append(publications[i])
		return result



class TradesMarkersManager(BaseMarkersManager):
	def __init__(self):
		super(TradesMarkersManager, self).__init__(OBJECTS_TYPES.trade())


	def record_min_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'hash_id',
			'for_sale', 'for_rent',
			'sale_terms__price', 'sale_terms__currency_sid',
			'rent_terms__price', 'rent_terms__currency_sid',
			'body__electricity', 'body__gas', 'body__sewerage', 'body__hot_water', 'body__cold_water',
			'body__building_type_sid', 'body__halls_area', 'body__total_area', 'body__floor',)


	def serialize_publication(self, record):
		if True not in (record.for_sale, record.for_rent):
			raise self.SerializationError('Object must be "for sale", "for rent", or both. Nothing selected.')

		if record.body.rooms_count is None:
			raise self.SerializationError('rooms_count is required but absent.')

		if record.body.total_area is None:
			raise self.SerializationError('total_area is required but absent.')


		data = [
			record.hash_id,
			record.for_sale,
		    record.for_rent,

			float(record.body.halls_area), # json can't handle decimal
			float(record.body.total_area), # json can't handle decimal

			record.body.electricity,
		    record.body.gas,
		    record.body.sewerage,
		    record.body.hot_water,
		    record.body.cold_water,

			record.body.market_type_sid,
			record.body.building_type_sid,
		]


		if record.for_sale:
			if record.sale_terms.price is None:
				raise self.SerializationError('sale_price is required but absent.')

			data.extend([
		        float(record.sale_terms.price), # json can't handle decimal
			    record.sale_terms.currency_sid,
			])


		if record.for_rent:
			data.extend([
				float(record.rent_terms.price), # json can't handle decimal
			    record.rent_terms.currency_sid,
			])


		digest = json.dumps(data).replace('true', 't').replace('false', 'f').replace(' ', '')
		return digest


	def deserialize_marker_data(self, data):
		data = json.loads(data.replace('t', 'true').replace('f', 'false'))

		index = iter(xrange(0, len(data)))
		deserialized_data = {
			'hash_id':              data[next(index)],
			'for_sale':             data[next(index)],
		    'for_rent':             data[next(index)],

			'halls_area':           data[next(index)],
		    'total_area':           data[next(index)],

			'electricity':          data[next(index)],
		    'gas':                  data[next(index)],
		    'sewerage':             data[next(index)],
		    'hot_water':            data[next(index)],
		    'cold_water':           data[next(index)],

			'market_type_sid':      data[next(index)],
			'building_type_sid':    data[next(index)],
		}

		if deserialized_data['for_sale']:
			deserialized_data.update({
				'sale_price': data[next(index)],
				'sale_currency_sid': data[next(index)],
			})


		if deserialized_data['for_rent']:
			deserialized_data.update({
				'rent_price': data[next(index)],
				'rent_currency_sid': data[next(index)],
			})


		return deserialized_data


	def marker_brief(self, marker, filters=None):
		"""
		Сформує бриф для маркеру на основі даних, переданих у фільтрі.
		(В даний момент враховується лише валюта запиту)
		"""

		# todo: додати зміну видачі в залежності від фільтрів.
		# Наприклад, якщо задано к-сть кімнат від 1 до 1 - нема змісту показувати в брифі к-сть кімнат,
		# ітак ясно, що їх буде не більше одної.

		result = {
			'id': marker['hash_id']
		}

		# Гривня як базова валюта обирається згідно з чинним законодавством,
		# але якщо у фільтрі вказана інша - переформатувати бриф на неї.
		if filters is None:
			currency = CURRENCIES.uah()
		else:
			currency = filters.get('currency_sid', CURRENCIES.uah())


		if marker.get('for_sale', False):
			total_area = '{0:.2f}'.format(marker.get('total_area')).rstrip('0').rstrip('.') \
				if marker.get('total_area') else None
			sale_price = self.format_price(marker['sale_price'], marker['sale_currency_sid'], currency)
			result.update({
				'd0': u'Площадь: {0} м²'.format(total_area) if total_area else u'Площадь неизвестна',
				'd1': u'{0} {1}'.format(sale_price, self.format_currency(currency)),
			})
			return result

		elif marker.get('for_rent', False):
			total_area = '{0:.2f}'.format(marker.get('total_area')).rstrip('0').rstrip('.') \
				if marker.get('total_area') else None
			rent_price = self.format_price(marker['rent_price'], marker['rent_currency_sid'], currency)
			result.update({
				'd0': u'Площадь: {0} м²'.format(total_area) if total_area else u'Площадь неизвестна',
				'd1': u'{0} {1}'.format(rent_price, self.format_currency(currency)),
			})
			return result

		raise RuntimeException('Marker is not for sale and not for rent.')



	def filter(self, publications, filters):
		# WARNING:
		# дана функція для економії часу виконання не виконує deepcopy над publications

		if filters is None:
			return publications

		operation_sid = filters.get('operation_sid')
		if operation_sid is None:
			raise InvalidArgument('Invalid conditions. Operation_sid is absent.')


		# Перед фільтруванням оголошень слід перевірити цілісність і коректність об’єкту умов.
		# На даному етапі виконується перевірка всіх обов’язкових полів filters.
		# Дану перевірку винесено за цикл фільтрування щоб підвищити швидкодію,
		# оскільки об’єкт filters не змінюється в ході фільтрування і достатньо перевіріити його лише раз.
		currency_sid = filters.get('currency_sid')
		if currency_sid is None:
			# Перевіряти фільтри цін має зміст лише тоді, коли задано валюту фільтру,
			# інакше неможливо привести валюту ціни з фільтра до валюти з оголошення.
			# На фронтенді валюта повинна бути задана за замовчуванням.
			raise InvalidArgument('sale_currency_sid is absent.')
		elif currency_sid not in CURRENCIES.values():
			raise InvalidArgument('currency_sid is invalid.')

		if operation_sid not in [0, 1]:
			raise InvalidArgument('Invalid operation_sid.')


		# Для відбору елементів зі списку publications, використовується список statuses.
		# Кість елементів цього списку відповідає к-сті елементів publications.
		# На початку фільтрування всі елементи statuses встановлені в True.
		# Під час фільтрування деякі з них будуть встановлені в False.
		# На завершальному етапі зі списку publications будуть відібрані лише ті елементи,
		# відповідний елемент statuses яких встановлений в True.
		#
		# Додатковий список використовується для підвищення швидкодії фільтрування,
		# оскільки зміна True/False відбуваєтсья в рази швидше, ніж вилучення елементів зі списку
		# з повторною його перебудовою на кожній перевірці та ітерації.
		statuses = [True] * len(publications)


		for i in range(len(statuses)):
			# Якщо даний запис вже позначений як виключений — не аналізувати його.
			if not statuses[i]:
				continue

			marker = publications[i][1]

			# operation type
			if operation_sid == 0:
				if not marker.get('for_sale', False):
					statuses[i] = False
					continue

			elif operation_sid == 1:
				if not marker.get('for_rent', False):
					statuses[i] = False
					continue


			# price
			price_min = filters.get('price_from')
			price_max = filters.get('price_to')
			if price_min is not None:
				price_min = convert_currency(price_min, currency_sid, marker['sale_currency_sid'])
			if price_max is not None:
				price_max = convert_currency(price_max, currency_sid, marker['sale_currency_sid'])


			if (price_max is not None) and (price_min is not None):
				if not price_min <= marker['sale_price'] <= price_max:
					statuses[i] = False
					continue

			elif price_min is not None:
				if not price_min <= marker['sale_price']:
					statuses[i] = False
					continue

			elif price_max is not None:
				if not marker['sale_price'] <= price_max:
					statuses[i] = False
					continue


			# market type
			if ('new_buildings' in filters) and ('secondary_market' in filters):
				# Немає змісту фільтрувати.
				# Під дані умови потрапляють всі об’єкти.
				pass

			elif 'new_buildings' in filters:
				statuses[i] = (marker['market_type_sid'] == MARKET_TYPES.new_building())
			elif 'new_buildings' in filters:
				statuses[i] = (marker['market_type_sid'] == MARKET_TYPES.secondary_market())


			# halls area
			halls_area_min = filters.get('halls_area_from')
			halls_area_max = filters.get('halls_area_to')
			halls_area = marker.get('halls_area')

			if (halls_area_max is not None) or (halls_area_min is not None):
				# Поле "площа залів" може бути не обов’язковим.
				# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
				# відхилити запис через неможливість аналізу.
				if halls_area is None:
					statuses[i] = False
					continue

			if (halls_area_max is not None) and (halls_area_min is not None):
				if not halls_area_min <= halls_area <= halls_area_max:
					statuses[i] = False
					continue

			elif halls_area_min is not None:
				if not halls_area_min <= halls_area:
					statuses[i] = False
					continue

			elif halls_area_max is not None:
				if not halls_area <= halls_area_max:
					statuses[i] = False
					continue


			# total area
			total_area_min = filters.get('total_area_from')
			total_area_max = filters.get('total_area_to')
			total_area = marker.get('total_area')

			if (total_area_max is not None) or (total_area_min is not None):
				# Поле "загальна площа" може бути не обов’язковим.
				# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
				# відхилити запис через неможливість аналізу.
				if total_area is None:
					statuses[i] = False
					continue


			if (total_area_max is not None) and (total_area_min is not None):
				if not total_area_min <= total_area <= total_area_max:
					statuses[i] = False
					continue

			elif total_area_min is not None:
				if not total_area_min <= total_area:
					statuses[i] = False
					continue

			elif total_area_max is not None:
				if not total_area <= total_area_max:
					statuses[i] = False
					continue


			# building type
			building_type_sid = filters.get('building_type_sid')
			if building_type_sid is not None:
				# Поле "тип будинку" може бути не обов’язковим.
				# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
				# відхилити запис через неможливість аналізу.
				if 'building_type_sid' not in marker:
					statuses[i] = False
					continue

				if building_type_sid == 1: # ТРЦ
					if marker['building_type_sid'] != TRADE_BUILDING_TYPES.entertainment():
						statuses[i] = False
						continue

				elif building_type_sid == 2: # бізнес-центр
					if marker['building_type_sid'] != TRADE_BUILDING_TYPES.business():
						statuses[i] = False
						continue

				elif building_type_sid == 3: # окреме
					if marker['building_type_sid'] != TRADE_BUILDING_TYPES.separate():
						statuses[i] = False
						continue


			if 'electricity' in filters:
				if (not 'electricity' in marker) or (not marker['electricity']):
					statuses[i] = False
					continue

			if  'gas' in filters:
				if (not 'gas' in marker) or (not marker['gas']):
					statuses[i] = False
					continue

			if 'hot_water' in filters:
				if (not 'hot_water' in marker) or (not marker['hot_water']):
					statuses[i] = False
					continue

			if  'cold_water' in filters:
				if (not 'cold_water' in marker) or (not marker['cold_water']):
					statuses[i] = False
					continue

			if 'sewerage' in filters:
				if (not 'sewerage' in marker) or (not marker['sewerage']):
					statuses[i] = False
					continue

		result = []
		for i in range(len(statuses)):
			if statuses[i]:
				result.append(publications[i])
		return result



class OfficesMarkersManager(BaseMarkersManager):
	def __init__(self):
		super(OfficesMarkersManager, self).__init__(OBJECTS_TYPES.office())


	def record_min_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'hash_id',
			'for_sale', 'for_rent',
			'sale_terms__price', 'sale_terms__currency_sid',
			'rent_terms__price', 'rent_terms__currency_sid',
			'body__security', 'body__kitchen', 'body__hot_water', 'body__cold_water',
		    'body__building_type_sid', 'body__total_area', 'body__cabinets_count')


	def serialize_publication(self, record):
		if True not in (record.for_sale, record.for_rent):
			raise self.SerializationError('Object must be "for sale", "for rent", or both. Nothing selected.')

		if record.body.rooms_count is None:
			raise self.SerializationError('rooms_count is required but absent.')

		if record.body.total_area is None:
			raise self.SerializationError('total_area is required but absent.')


		data = [
			record.hash_id,
			record.for_sale,
		    record.for_rent,

			float(record.body.total_area), # json can't handle decimal
			record.body.cabinets_count,

			record.body.security,
		    record.body.kitchen,
		    record.body.hot_water,
		    record.body.cold_water,

			record.body.market_type_sid,
		    record.body.building_type_sid,
		]


		if record.for_sale:
			if record.sale_terms.price is None:
				raise self.SerializationError('sale_price is required but absent.')

			data.extend([
		        float(record.sale_terms.price), # json can't handle decimal
			    record.sale_terms.currency_sid,
			])


		if record.for_rent:
			data.extend([
				float(record.rent_terms.price), # json can't handle decimal
			    record.rent_terms.currency_sid,
			])


		digest = json.dumps(data).replace('true', 't').replace('false', 'f').replace(' ', '')
		return digest


	def deserialize_marker_data(self, data):
		data = json.loads(data.replace('t', 'true').replace('f', 'false'))

		index = iter(xrange(0, len(data)))
		deserialized_data = {
			'hash_id':              data[next(index)],
			'for_sale':             data[next(index)],
		    'for_rent':             data[next(index)],

			'cabinets_count':       data[next(index)],
		    'total_area':           data[next(index)],

			'security':             data[next(index)],
		    'kitchen':              data[next(index)],
		    'hot_water':            data[next(index)],
		    'cold_water':           data[next(index)],

			'market_type_sid':      data[next(index)],
			'building_type_sid':    data[next(index)],
		}

		if deserialized_data['for_sale']:
			deserialized_data.update({
				'sale_price': data[next(index)],
				'sale_currency_sid': data[next(index)],
			})


		if deserialized_data['for_rent']:
			deserialized_data.update({
				'rent_price': data[next(index)],
				'rent_currency_sid': data[next(index)],
			})


		return deserialized_data


	def marker_brief(self, marker, filters=None):
		"""
		Сформує бриф для маркеру на основі даних, переданих у фільтрі.
		(В даний момент враховується лише валюта запиту)
		"""

		# todo: додати зміну видачі в залежності від фільтрів.
		# Наприклад, якщо задано к-сть кімнат від 1 до 1 - нема змісту показувати в брифі к-сть кімнат,
		# ітак ясно, що їх буде не більше одної.

		result = {
			'id': marker['hash_id']
		}

		# Гривня як базова валюта обирається згідно з чинним законодавством,
		# але якщо у фільтрі вказана інша - переформатувати бриф на неї.
		if filters is None:
			currency = CURRENCIES.uah()
		else:
			currency = filters.get('currency_sid', CURRENCIES.uah())


		if marker.get('for_sale', False):
			total_area = '{0:.2f}'.format(marker.get('total_area')).rstrip('0').rstrip('.') \
				if marker.get('total_area') else None
			sale_price = self.format_price(marker['sale_price'], marker['sale_currency_sid'], currency)
			result.update({
				'd0': u'Площадь: {0} м²'.format(total_area) if total_area else u'Площадь неизвестна',
				'd1': u'{0} {1}'.format(sale_price, self.format_currency(currency)),
			})
			return result

		elif marker.get('for_rent', False):
			total_area = '{0:.2f}'.format(marker.get('total_area')).rstrip('0').rstrip('.') \
				if marker.get('total_area') else None
			rent_price = self.format_price(marker['rent_price'], marker['rent_currency_sid'], currency)
			result.update({
				'd0': u'Площадь: {0} м²'.format(total_area) if total_area else u'Площадь неизвестна',
				'd1': u'{0} {1}'.format(rent_price, self.format_currency(currency)),
			})
			return result

		raise RuntimeException('Marker is not for sale and not for rent.')


	def filter(self, publications, filters):
		# WARNING:
		#   дана функція для економії часу виконання не виконує deepcopy над publications

		if filters is None:
			return publications

		operation_sid = filters.get('operation_sid')
		if operation_sid is None:
			raise InvalidArgument('Invalid conditions. Operation_sid is absent.')


		# Перед фільтруванням оголошень слід перевірити цілісність і коректність об’єкту умов.
		# На даному етапі виконується перевірка всіх обов’язкових полів filters.
		# Дану перевірку винесено за цикл фільтрування щоб підвищити швидкодію,
		# оскільки об’єкт filters не змінюється в ході фільтрування і достатньо перевіріити його лише раз.
		currency_sid = filters.get('currency_sid')
		if currency_sid is None:
			# Перевіряти фільтри цін має зміст лише тоді, коли задано валюту фільтру,
			# інакше неможливо привести валюту ціни з фільтра до валюти з оголошення.
			# На фронтенді валюта повинна бути задана за замовчуванням.
			raise InvalidArgument('sale_currency_sid is absent.')
		elif currency_sid not in CURRENCIES.values():
			raise InvalidArgument('currency_sid is invalid.')

		if operation_sid not in [0, 1]:
			raise InvalidArgument('Invalid operation_sid.')


		# Для відбору елементів зі списку publications, використовується список statuses.
		# Кість елементів цього списку відповідає к-сті елементів publications.
		# На початку фільтрування всі елементи statuses встановлені в True.
		# Під час фільтрування деякі з них будуть встановлені в False.
		# На завершальному етапі зі списку publications будуть відібрані лише ті елементи,
		# відповідний елемент statuses яких встановлений в True.
		#
		# Додатковий список використовується для підвищення швидкодії фільтрування,
		# оскільки зміна True/False відбуваєтсья в рази швидше, ніж вилучення елементів зі списку
		# з повторною його перебудовою на кожній перевірці та ітерації.
		statuses = [True] * len(publications)


		for i in range(len(statuses)):
			# Якщо даний запис вже позначений як виключений — не аналізувати його.
			if not statuses[i]:
				continue

			marker = publications[i][1]

			# operation type
			if operation_sid == 0:
				if not marker.get('for_sale', False):
					statuses[i] = False
					continue

			elif operation_sid == 1:
				if not marker.get('for_rent', False):
					statuses[i] = False
					continue

			# price
			if operation_sid == 0:
				marker_price = marker.get('sale_price')
				marker_currency = marker.get('sale_currency_sid')
			else:
				marker_price = marker.get('rent_price')
				marker_currency = marker.get('rent_currency_sid')


			price_min = filters.get('price_from')
			price_max = filters.get('price_to')
			if price_min is not None:
				price_min = convert_currency(price_min, currency_sid, marker_currency)
			if price_max is not None:
				price_max = convert_currency(price_max, currency_sid, marker_currency)


			if (price_max is not None) and (price_min is not None):
				if not price_min <= marker_price <= price_max:
					statuses[i] = False
					continue

			elif price_min is not None:
				if not price_min <= marker_price:
					statuses[i] = False
					continue

			elif price_max is not None:
				if not marker_price <= price_max:
					statuses[i] = False
					continue


			# market type
			if ('new_buildings' in filters) and ('secondary_market' in filters):
				# Немає змісту фільтрувати.
				# Під дані умови потрапляють всі об’єкти.
				pass

			elif 'new_buildings' in filters:
				statuses[i] = (marker['market_type_sid'] == MARKET_TYPES.new_building())
			elif 'new_buildings' in filters:
				statuses[i] = (marker['market_type_sid'] == MARKET_TYPES.secondary_market())


			# total area
			total_area_min = filters.get('total_area_from')
			total_area_max = filters.get('total_area_to')
			total_area = marker.get('total_area')

			if (total_area_max is not None) or (total_area_min is not None):
				# Поле "загальна площа" може бути не обов’язковим.
				# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
				# відхилити запис через неможливість аналізу.
				if total_area is None:
					statuses[i] = False
					continue


			if (total_area_max is not None) and (total_area_min is not None):
				if not total_area_min <= total_area <= total_area_max:
					statuses[i] = False
					continue

			elif total_area_min is not None:
				if not total_area_min <= total_area:
					statuses[i] = False
					continue

			elif total_area_max is not None:
				if not total_area <= total_area_max:
					statuses[i] = False
					continue


			# cabinets count
			cabinets_count_min = filters.get('cabinets_count_from')
			cabinets_count_max = filters.get('cabinets_count_to')
			cabinets_count = marker.get('cabinets_count')

			if (cabinets_count_max is not None) or (cabinets_count_min is not None):
				# Поле може бути не обов’язковим.
				# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
				# відхилити запис через неможливість аналізу.
				if cabinets_count is None:
					statuses[i] = False
					continue

			if (cabinets_count_max is not None) and (cabinets_count_min is not None):
				if not cabinets_count_min <= cabinets_count <= cabinets_count_max:
					statuses[i] = False
					continue

			elif cabinets_count_min is not None:
				if not cabinets_count_min <= cabinets_count:
					statuses[i] = False
					continue

			elif cabinets_count_max is not None:
				if not cabinets_count <= cabinets_count_max:
					statuses[i] = False
					continue


			if 'security' in filters:
				if (not 'security' in marker) or (not marker['security']):
					statuses[i] = False
					continue

			if  'kitchen' in filters:
				if (not 'kitchen' in marker) or (not marker['kitchen']):
					statuses[i] = False
					continue

			if 'hot_water' in filters:
				if (not 'hot_water' in marker) or (not marker['hot_water']):
					statuses[i] = False
					continue

			if  'cold_water' in filters:
				if (not 'cold_water' in marker) or (not marker['cold_water']):
					statuses[i] = False
					continue

		result = []
		for i in range(len(statuses)):
			if statuses[i]:
				result.append(publications[i])
		return result



class WarehousesMarkersManager(BaseMarkersManager):
	def __init__(self):
		super(WarehousesMarkersManager, self).__init__(OBJECTS_TYPES.warehouse())


	def record_min_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'hash_id',
			'for_sale', 'for_rent',
			'sale_terms__price', 'sale_terms__currency_sid',
			'rent_terms__price', 'rent_terms__currency_sid',
			'body__electricity', 'body__gas', 'body__hot_water', 'body__cold_water',
		    'body__security_alarm', 'body__fire_alarm', 'body__area')


	def serialize_publication(self, record):
		if True not in (record.for_sale, record.for_rent):
			raise self.SerializationError('Object must be "for sale", "for rent", or both. Nothing selected.')

		if record.body.rooms_count is None:
			raise self.SerializationError('rooms_count is required but absent.')

		if record.body.total_area is None:
			raise self.SerializationError('total_area is required but absent.')


		data = [
			record.hash_id,
			record.for_sale,
		    record.for_rent,

			float(record.body.area), # json can't handle decimal

			record.body.electricity,
		    record.body.gas,
		    record.body.hot_water,
		    record.body.cold_water,
		    record.body.security_alarm,
		    record.body.fire_alarm,

		    record.body.market_type_sid,
		]

		# Поле поверху може бути пустим, якщо тип поверху вибрано як "мансарда" чи "цоколь".
		# Якщо воно пусте — немає змісту його сериалізувати.
		if record.body.floor_type_sid == FLOOR_TYPES.floor():
			data.append(record.body.floor)


		if record.for_sale:
			if record.sale_terms.price is None:
				raise self.SerializationError('sale_price is required but absent.')

			data.extend([
		        float(record.sale_terms.price), # json can't handle decimal
			    record.sale_terms.currency_sid,
			])


		if record.for_rent:
			data.extend([
				float(record.rent_terms.price), # json can't handle decimal
			    record.rent_terms.currency_sid,
			])


		digest = json.dumps(data).replace('true', 't').replace('false', 'f').replace(' ', '')
		return digest


	def deserialize_marker_data(self, data):
		data = json.loads(data.replace('t', 'true').replace('f', 'false'))

		index = iter(xrange(0, len(data)))
		deserialized_data = {
			'hash_id':              data[next(index)],
			'for_sale':             data[next(index)],
		    'for_rent':             data[next(index)],

		    'area':           data[next(index)],

			'electricity':          data[next(index)],
		    'gas':                  data[next(index)],
		    'hot_water':            data[next(index)],
		    'cold_water':           data[next(index)],
		    'security_alarm':       data[next(index)],
		    'fire_alarm':           data[next(index)],

		    'market_type_sid':      data[next(index)],
		}


		if deserialized_data['for_sale']:
			deserialized_data.update({
				'sale_price': data[next(index)],
				'sale_currency_sid': data[next(index)],
			})


		if deserialized_data['for_rent']:
			deserialized_data.update({
				'rent_price': data[next(index)],
				'rent_currency_sid': data[next(index)],
			})


		return deserialized_data


	def marker_brief(self, marker, filters=None):
		"""
		Сформує бриф для маркеру на основі даних, переданих у фільтрі.
		(В даний момент враховується лише валюта запиту)
		"""

		# todo: додати зміну видачі в залежності від фільтрів.
		# Наприклад, якщо задано к-сть кімнат від 1 до 1 - нема змісту показувати в брифі к-сть кімнат,
		# ітак ясно, що їх буде не більше одної.

		result = {
			'id': marker['hash_id']
		}

		# Гривня як базова валюта обирається згідно з чинним законодавством,
		# але якщо у фільтрі вказана інша - переформатувати бриф на неї.
		if filters is None:
			currency = CURRENCIES.uah()
		else:
			currency = filters.get('currency_sid', CURRENCIES.uah())


		if marker.get('for_sale', False):
			area = '{0:.2f}'.format(marker.get('area')).rstrip('0').rstrip('.') if marker.get('area') else None
			sale_price = self.format_price(marker['sale_price'], marker['sale_currency_sid'], currency)
			result.update({
				'd0': u'Площадь: {0} м²'.format(area) if area else u'Площадь неизвестна',
				'd1': u'{0} {1}'.format(sale_price, self.format_currency(currency)),
			})
			return result

		elif marker.get('for_rent', False):
			area = '{0:.2f}'.format(marker.get('area')).rstrip('0').rstrip('.') if marker.get('area') else None
			rent_price = self.format_price(marker['rent_price'], marker['rent_currency_sid'], currency)
			result.update({
				'd0': u'Площадь: {0} м²'.format(area) if area else u'Площадь неизвестна',
				'd1': u'{0} {1}'.format(rent_price, self.format_currency(currency)),
			})
			return result

		raise RuntimeException('Marker is not for sale and not for rent.')


	def filter(self, publications, filters):
		# WARNING:
		#   дана функція для економії часу виконання не виконує deepcopy над publications

		if filters is None:
			return publications

		operation_sid = filters.get('operation_sid')
		if operation_sid is None:
			raise InvalidArgument('Invalid conditions. Operation_sid is absent.')


		# Перед фільтруванням оголошень слід перевірити цілісність і коректність об’єкту умов.
		# На даному етапі виконується перевірка всіх обов’язкових полів filters.
		# Дану перевірку винесено за цикл фільтрування щоб підвищити швидкодію,
		# оскільки об’єкт filters не змінюється в ході фільтрування і достатньо перевіріити його лише раз.
		currency_sid = filters.get('currency_sid')
		if currency_sid is None:
			# Перевіряти фільтри цін має зміст лише тоді, коли задано валюту фільтру,
			# інакше неможливо привести валюту ціни з фільтра до валюти з оголошення.
			# На фронтенді валюта повинна бути задана за замовчуванням.
			raise InvalidArgument('sale_currency_sid is absent.')
		elif currency_sid not in CURRENCIES.values():
			raise InvalidArgument('currency_sid is invalid.')

		if operation_sid not in [0, 1]:
			raise InvalidArgument('Invalid operation_sid.')


		# Для відбору елементів зі списку publications, використовується список statuses.
		# Кість елементів цього списку відповідає к-сті елементів publications.
		# На початку фільтрування всі елементи statuses встановлені в True.
		# Під час фільтрування деякі з них будуть встановлені в False.
		# На завершальному етапі зі списку publications будуть відібрані лише ті елементи,
		# відповідний елемент statuses яких встановлений в True.
		#
		# Додатковий список використовується для підвищення швидкодії фільтрування,
		# оскільки зміна True/False відбуваєтсья в рази швидше, ніж вилучення елементів зі списку
		# з повторною його перебудовою на кожній перевірці та ітерації.
		statuses = [True] * len(publications)


		for i in range(len(statuses)):
			# Якщо даний запис вже позначений як виключений — не аналізувати його.
			if not statuses[i]:
				continue

			marker = publications[i][1]

			# operation type
			if operation_sid == 0:
				if not marker.get('for_sale', False):
					statuses[i] = False
					continue

			elif operation_sid == 1:
				if not marker.get('for_rent', False):
					statuses[i] = False
					continue

			# price
			marker_currency = marker.get('sale_currency_sid')
			if marker_currency is None:
				marker_currency = marker.get('rent_currency_sid')

			price_min = filters.get('price_from')
			price_max = filters.get('price_to')
			if price_min is not None:
				price_min = convert_currency(price_min, currency_sid, marker_currency)
			if price_max is not None:
				price_max = convert_currency(price_max, currency_sid, marker_currency)


			if (price_max is not None) and (price_min is not None):
				if not price_min <= marker['sale_price'] <= price_max:
					statuses[i] = False
					continue

			elif price_min is not None:
				if not price_min <= marker['sale_price']:
					statuses[i] = False
					continue

			elif price_max is not None:
				if not marker['sale_price'] <= price_max:
					statuses[i] = False
					continue


			# market type
			if ('new_buildings' in filters) and ('secondary_market' in filters):
				# Немає змісту фільтрувати.
				# Під дані умови потрапляють всі об’єкти.
				pass

			elif 'new_buildings' in filters:
				statuses[i] = (marker['market_type_sid'] == MARKET_TYPES.new_building())
			elif 'new_buildings' in filters:
				statuses[i] = (marker['market_type_sid'] == MARKET_TYPES.secondary_market())


			# halls area
			area_min = filters.get('halls_area_from')
			area_max = filters.get('halls_area_to')
			area = marker.get('area')

			if (area_max is not None) or (area_min is not None):
				# Поле "площа залів" може бути не обов’язковим.
				# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
				# відхилити запис через неможливість аналізу.
				if area is None:
					statuses[i] = False
					continue

			if (area_max is not None) and (area_min is not None):
				if not area_min <= area <= area_max:
					statuses[i] = False
					continue

			elif area_min is not None:
				if not area_min <= area:
					statuses[i] = False
					continue

			elif area_max is not None:
				if not area <= area_max:
					statuses[i] = False
					continue


			if 'electricity' in filters:
				if (not 'electricity' in marker) or (not marker['electricity']):
					statuses[i] = False
					continue

			if  'gas' in filters:
				if (not 'gas' in marker) or (not marker['gas']):
					statuses[i] = False
					continue

			if 'hot_water' in filters:
				if (not 'hot_water' in marker) or (not marker['hot_water']):
					statuses[i] = False
					continue

			if  'cold_water' in filters:
				if (not 'cold_water' in marker) or (not marker['cold_water']):
					statuses[i] = False
					continue

			if 'security_alarm' in filters:
				if (not 'security_alarm' in marker) or (not marker['security_alarm']):
					statuses[i] = False
					continue

			if 'fire_alarm' in filters:
				if (not 'fire_alarm' in marker) or (not marker['fire_alarm']):
					statuses[i] = False
					continue

		result = []
		for i in range(len(statuses)):
			if statuses[i]:
				result.append(publications[i])
		return result



class BusinessesMarkersManager(BaseMarkersManager):
	def __init__(self):
		super(BusinessesMarkersManager, self).__init__(OBJECTS_TYPES.business())


	def record_min_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'hash_id',
			'for_sale', 'for_rent',
			'sale_terms__price', 'sale_terms__currency_sid',
			'rent_terms__price', 'rent_terms__currency_sid')


	def serialize_publication(self, record):
		if True not in (record.for_sale, record.for_rent):
			raise self.SerializationError('Object must be "for sale", "for rent", or both. Nothing selected.')

		if record.body.rooms_count is None:
			raise self.SerializationError('rooms_count is required but absent.')

		if record.body.total_area is None:
			raise self.SerializationError('total_area is required but absent.')


		data = [
			record.hash_id,
			record.for_sale,
		    record.for_rent,

		    record.body.market_type_sid,
		]

		if record.for_sale:
			if record.sale_terms.price is None:
				raise self.SerializationError('sale_price is required but absent.')

			data.extend([
		        float(record.sale_terms.price), # json can't handle decimal
			    record.sale_terms.currency_sid,
			])


		if record.for_rent:
			data.extend([
				float(record.rent_terms.price), # json can't handle decimal
			    record.rent_terms.currency_sid,
			])


		digest = json.dumps(data).replace('true', 't').replace('false', 'f').replace(' ', '')
		return digest


	def deserialize_marker_data(self, data):
		data = json.loads(data.replace('t', 'true').replace('f', 'false'))

		index = iter(xrange(0, len(data)))
		deserialized_data = {
			'hash_id':              data[next(index)],
			'for_sale':             data[next(index)],
		    'for_rent':             data[next(index)],

			'market_type_sid':      data[next(index)],
		}


		if deserialized_data['for_sale']:
			deserialized_data.update({
				'sale_price': data[next(index)],
				'sale_currency_sid': data[next(index)],
			})


		if deserialized_data['for_rent']:
			deserialized_data.update({
				'rent_price': data[next(index)],
				'rent_currency_sid': data[next(index)],
			})


		return deserialized_data


	def marker_brief(self, marker, filters=None):
		"""
		Сформує бриф для маркеру на основі даних, переданих у фільтрі.
		(В даний момент враховується лише валюта запиту)
		"""

		# todo: додати зміну видачі в залежності від фільтрів.
		# Наприклад, якщо задано к-сть кімнат від 1 до 1 - нема змісту показувати в брифі к-сть кімнат,
		# ітак ясно, що їх буде не більше одної.

		result = {
			'id': marker['hash_id']
		}

		# Гривня як базова валюта обирається згідно з чинним законодавством,
		# але якщо у фільтрі вказана інша - переформатувати бриф на неї.
		if filters is None:
			currency = CURRENCIES.uah()
		else:
			currency = filters.get('currency_sid', CURRENCIES.uah())


		if marker.get('for_sale', False):
			sale_price = self.format_price(marker['sale_price'], marker['sale_currency_sid'], currency)
			result.update({
				'd0': u'{0} {1}'.format(sale_price, self.format_currency(currency)),
			    'd1': u'' # немає додаткового параметру
			})
			return result

		elif marker.get('for_rent', False):
			rent_price = self.format_price(marker['rent_price'], marker['rent_currency_sid'], currency)
			result.update({
				'd0': u'{0} {1}'.format(rent_price, self.format_currency(currency)),
			    'd1': u''  # немає додаткового параметру
			})
			return result

		raise RuntimeException('Marker is not for sale and not for rent.')


	def filter(self, publications, filters):
		# WARNING:
		#   дана функція для економії часу виконання не виконує deepcopy над publications

		if filters is None:
			return publications

		operation_sid = filters.get('operation_sid')
		if operation_sid is None:
			raise InvalidArgument('Invalid conditions. Operation_sid is absent.')


		# Перед фільтруванням оголошень слід перевірити цілісність і коректність об’єкту умов.
		# На даному етапі виконується перевірка всіх обов’язкових полів filters.
		# Дану перевірку винесено за цикл фільтрування щоб підвищити швидкодію,
		# оскільки об’єкт filters не змінюється в ході фільтрування і достатньо перевіріити його лише раз.
		currency_sid = filters.get('currency_sid')
		if currency_sid is None:
			# Перевіряти фільтри цін має зміст лише тоді, коли задано валюту фільтру,
			# інакше неможливо привести валюту ціни з фільтра до валюти з оголошення.
			# На фронтенді валюта повинна бути задана за замовчуванням.
			raise InvalidArgument('sale_currency_sid is absent.')
		elif currency_sid not in CURRENCIES.values():
			raise InvalidArgument('currency_sid is invalid.')

		if operation_sid not in [0, 1]:
			raise InvalidArgument('Invalid operation_sid.')


		# Для відбору елементів зі списку publications, використовується список statuses.
		# Кість елементів цього списку відповідає к-сті елементів publications.
		# На початку фільтрування всі елементи statuses встановлені в True.
		# Під час фільтрування деякі з них будуть встановлені в False.
		# На завершальному етапі зі списку publications будуть відібрані лише ті елементи,
		# відповідний елемент statuses яких встановлений в True.
		#
		# Додатковий список використовується для підвищення швидкодії фільтрування,
		# оскільки зміна True/False відбуваєтсья в рази швидше, ніж вилучення елементів зі списку
		# з повторною його перебудовою на кожній перевірці та ітерації.
		statuses = [True] * len(publications)


		for i in range(len(statuses)):
			# Якщо даний запис вже позначений як виключений — не аналізувати його.
			if not statuses[i]:
				continue

			marker = publications[i][1]

			# operation type
			if operation_sid == 0:
				if not marker.get('for_sale', False):
					statuses[i] = False
					continue

			elif operation_sid == 1:
				if not marker.get('for_rent', False):
					statuses[i] = False
					continue


			# price
			price_min = filters.get('price_from')
			price_max = filters.get('price_to')
			if price_min is not None:
				price_min = convert_currency(price_min, currency_sid, marker['sale_currency_sid'])
			if price_max is not None:
				price_max = convert_currency(price_max, currency_sid, marker['sale_currency_sid'])


			if (price_max is not None) and (price_min is not None):
				if not price_min <= marker['sale_price'] <= price_max:
					statuses[i] = False
					continue

			elif price_min is not None:
				if not price_min <= marker['sale_price']:
					statuses[i] = False
					continue

			elif price_max is not None:
				if not marker['sale_price'] <= price_max:
					statuses[i] = False
					continue


			# market type
			if ('new_buildings' in filters) and ('secondary_market' in filters):
				# Немає змісту фільтрувати.
				# Під дані умови потрапляють всі об’єкти.
				pass

			elif 'new_buildings' in filters:
				statuses[i] = (marker['market_type_sid'] == MARKET_TYPES.new_building())
			elif 'new_buildings' in filters:
				statuses[i] = (marker['market_type_sid'] == MARKET_TYPES.secondary_market())

		result = []
		for i in range(len(statuses)):
			if statuses[i]:
				result.append(publications[i])
		return result



class CateringsMarkersManager(BaseMarkersManager):
	def __init__(self):
		super(CateringsMarkersManager, self).__init__(OBJECTS_TYPES.catering())


	def record_min_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'hash_id',
			'for_sale', 'for_rent',
			'sale_terms__price', 'sale_terms__currency_sid',
			'rent_terms__price', 'rent_terms__currency_sid',
			'body__electricity', 'body__gas', 'body__hot_water', 'body__cold_water',
			'body__building_type_sid', 'body__halls_count', 'body__halls_area', 'body__total_area',)


	def serialize_publication(self, record):
		if True not in (record.for_sale, record.for_rent):
			raise self.SerializationError('Object must be "for sale", "for rent", or both. Nothing selected.')

		if record.body.rooms_count is None:
			raise self.SerializationError('rooms_count is required but absent.')

		if record.body.total_area is None:
			raise self.SerializationError('total_area is required but absent.')


		data = [
			record.hash_id,
			record.for_sale,
		    record.for_rent,

			float(record.body.halls_area), # json can't handle decimal
			float(record.body.total_area), # json can't handle decimal

			record.body.electricity,
		    record.body.gas,
		    record.body.sewerage,
		    record.body.hot_water,
		    record.body.cold_water,

			record.body.market_type_sid,
			record.body.building_type_sid,
		]


		if record.for_sale:
			if record.sale_terms.price is None:
				raise self.SerializationError('sale_price is required but absent.')

			data.extend([
		        float(record.sale_terms.price), # json can't handle decimal
			    record.sale_terms.currency_sid,
			])


		if record.for_rent:
			data.extend([
				float(record.rent_terms.price), # json can't handle decimal
			    record.rent_terms.currency_sid,
			])


		digest = json.dumps(data).replace('true', 't').replace('false', 'f').replace(' ', '')
		return digest


	def deserialize_marker_data(self, data):
		data = json.loads(data.replace('t', 'true').replace('f', 'false'))

		index = iter(xrange(0, len(data)))
		deserialized_data = {
			'hash_id':              data[next(index)],
			'for_sale':             data[next(index)],
		    'for_rent':             data[next(index)],

			'halls_area':           data[next(index)],
		    'total_area':           data[next(index)],

			'electricity':          data[next(index)],
		    'gas':                  data[next(index)],
		    'sewerage':             data[next(index)],
		    'hot_water':            data[next(index)],
		    'cold_water':           data[next(index)],

			'market_type_sid':      data[next(index)],
			'building_type_sid':    data[next(index)],
		}

		if deserialized_data['for_sale']:
			deserialized_data.update({
				'sale_price': data[next(index)],
				'sale_currency_sid': data[next(index)],
			})


		if deserialized_data['for_rent']:
			deserialized_data.update({
				'rent_price': data[next(index)],
				'rent_currency_sid': data[next(index)],
			})


		return deserialized_data


	def marker_brief(self, marker, filters=None):
		"""
		Сформує бриф для маркеру на основі даних, переданих у фільтрі.
		(В даний момент враховується лише валюта запиту)
		"""

		# todo: додати зміну видачі в залежності від фільтрів.
		# Наприклад, якщо задано к-сть кімнат від 1 до 1 - нема змісту показувати в брифі к-сть кімнат,
		# ітак ясно, що їх буде не більше одної.

		result = {
			'id': marker['hash_id']
		}

		# Гривня як базова валюта обирається згідно з чинним законодавством,
		# але якщо у фільтрі вказана інша - переформатувати бриф на неї.
		if filters is None:
			currency = CURRENCIES.uah()
		else:
			currency = filters.get('currency_sid', CURRENCIES.uah())


		if marker.get('for_sale', False):
			halls_area = '{0:.2f}'.format(marker.get('halls_area')).rstrip('0').rstrip('.') \
				if marker.get('halls_area') else None
			sale_price = self.format_price(marker['sale_price'], marker['sale_currency_sid'], currency)
			result.update({
				'd0': u'Пл. залов: {0} м²'.format(halls_area) if halls_area else u'Пл. залов неизвестна',
				'd1': u'{0} {1}'.format(sale_price, self.format_currency(currency)),
			})
			return result

		elif marker.get('for_rent', False):
			halls_area = '{0:.2f}'.format(marker.get('halls_area')).rstrip('0').rstrip('.') \
				if marker.get('halls_area') else None
			rent_price = self.format_price(marker['rent_price'], marker['rent_currency_sid'], currency)
			result.update({
				'd0': u'Пл. залов: {0} м²'.format(halls_area) if halls_area else u'Пл. залов неизвестна',
				'd1': u'{0} {1}'.format(rent_price, self.format_currency(currency)),
			})
			return result

		raise RuntimeException('Marker is not for sale and not for rent.')


	def filter(self, publications, filters):
		# WARNING:
		#   дана функція для економії часу виконання не виконує deepcopy над publications

		if filters is None:
			return publications

		operation_sid = filters.get('operation_sid')
		if operation_sid is None:
			raise InvalidArgument('Invalid conditions. Operation_sid is absent.')


		# Перед фільтруванням оголошень слід перевірити цілісність і коректність об’єкту умов.
		# На даному етапі виконується перевірка всіх обов’язкових полів filters.
		# Дану перевірку винесено за цикл фільтрування щоб підвищити швидкодію,
		# оскільки об’єкт filters не змінюється в ході фільтрування і достатньо перевіріити його лише раз.
		currency_sid = filters.get('currency_sid')
		if currency_sid is None:
			# Перевіряти фільтри цін має зміст лише тоді, коли задано валюту фільтру,
			# інакше неможливо привести валюту ціни з фільтра до валюти з оголошення.
			# На фронтенді валюта повинна бути задана за замовчуванням.
			raise InvalidArgument('sale_currency_sid is absent.')
		elif currency_sid not in CURRENCIES.values():
			raise InvalidArgument('currency_sid is invalid.')

		if operation_sid not in [0, 1]:
			raise InvalidArgument('Invalid operation_sid.')


		# Для відбору елементів зі списку publications, використовується список statuses.
		# Кість елементів цього списку відповідає к-сті елементів publications.
		# На початку фільтрування всі елементи statuses встановлені в True.
		# Під час фільтрування деякі з них будуть встановлені в False.
		# На завершальному етапі зі списку publications будуть відібрані лише ті елементи,
		# відповідний елемент statuses яких встановлений в True.
		#
		# Додатковий список використовується для підвищення швидкодії фільтрування,
		# оскільки зміна True/False відбуваєтсья в рази швидше, ніж вилучення елементів зі списку
		# з повторною його перебудовою на кожній перевірці та ітерації.
		statuses = [True] * len(publications)


		for i in range(len(statuses)):
			# Якщо даний запис вже позначений як виключений — не аналізувати його.
			if not statuses[i]:
				continue

			marker = publications[i][1]


			# operation type
			if operation_sid == 0:
				if not marker.get('for_sale', False):
					statuses[i] = False
					continue

			elif operation_sid == 1:
				if not marker.get('for_rent', False):
					statuses[i] = False
					continue

			# price
			marker_currency = marker.get('sale_currency_sid')
			if marker_currency is None:
				marker_currency = marker.get('rent_currency_sid')

			price_min = filters.get('price_from')
			price_max = filters.get('price_to')
			if price_min is not None:
				price_min = convert_currency(price_min, currency_sid, marker_currency)
			if price_max is not None:
				price_max = convert_currency(price_max, currency_sid, marker_currency)


			if (price_max is not None) and (price_min is not None):
				if not price_min <= marker['sale_price'] <= price_max:
					statuses[i] = False
					continue

			elif price_min is not None:
				if not price_min <= marker['sale_price']:
					statuses[i] = False
					continue

			elif price_max is not None:
				if not marker['sale_price'] <= price_max:
					statuses[i] = False
					continue


			# market type
			if ('new_buildings' in filters) and ('secondary_market' in filters):
				# Немає змісту фільтрувати.
				# Під дані умови потрапляють всі об’єкти.
				pass

			elif 'new_buildings' in filters:
				statuses[i] = (marker['market_type_sid'] == MARKET_TYPES.new_building())
			elif 'new_buildings' in filters:
				statuses[i] = (marker['market_type_sid'] == MARKET_TYPES.secondary_market())


			# total area
			total_area_min = filters.get('total_area_from')
			total_area_max = filters.get('total_area_to')
			total_area = marker.get('total_area')

			if (total_area_max is not None) or (total_area_min is not None):
				# Поле може бути не обов’язковим.
				# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
				# відхилити запис через неможливість аналізу.
				if total_area is None:
					statuses[i] = False
					continue

			if (total_area_max is not None) and (total_area_min is not None):
				if not total_area_min <= total_area <= total_area_max:
					statuses[i] = False
					continue

			elif total_area_min is not None:
				if not total_area_min <= total_area:
					statuses[i] = False
					continue

			elif total_area_max is not None:
				if not total_area <= total_area_max:
					statuses[i] = False
					continue


			# halls area
			halls_area_min = filters.get('halls_area_from')
			halls_area_max = filters.get('halls_area_to')
			halls_area = marker.get('halls_area')

			if (halls_area_max is not None) or (halls_area_min is not None):
				# Поле "площа залів" може бути не обов’язковим.
				# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
				# відхилити запис через неможливість аналізу.
				if halls_area is None:
					statuses[i] = False
					continue

			if (halls_area_max is not None) and (halls_area_min is not None):
				if not halls_area_min <= halls_area <= halls_area_max:
					statuses[i] = False
					continue

			elif halls_area_min is not None:
				if not halls_area_min <= halls_area:
					statuses[i] = False
					continue

			elif halls_area_max is not None:
				if not halls_area <= halls_area_max:
					statuses[i] = False
					continue
					
					
			# halls count
			halls_count_min = filters.get('halls_count_from')
			halls_count_max = filters.get('halls_count_to')
			halls_count = marker.get('halls_count')

			if (halls_count_max is not None) or (halls_count_min is not None):
				# Поле може бути не обов’язковим.
				# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
				# відхилити запис через неможливість аналізу.
				if halls_count is None:
					statuses[i] = False
					continue

			if (halls_count_max is not None) and (halls_count_min is not None):
				if not halls_count_min <= halls_count <= halls_count_max:
					statuses[i] = False
					continue

			elif halls_count_min is not None:
				if not halls_count_min <= halls_count:
					statuses[i] = False
					continue

			elif halls_count_max is not None:
				if not halls_count <= halls_count_max:
					statuses[i] = False
					continue


			# building type
			building_type_sid = filters.get('building_type_sid')
			if building_type_sid is not None:
				# Поле "тип будинку" може бути не обов’язковим.
				# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
				# відхилити запис через неможливість аналізу.
				if 'building_type_sid' not in marker:
					statuses[i] = False
					continue

				if building_type_sid == 1: # ТРЦ
					if marker['building_type_sid'] != TRADE_BUILDING_TYPES.entertainment():
						statuses[i] = False
						continue

				elif building_type_sid == 2: # бізнес-центр
					if marker['building_type_sid'] != TRADE_BUILDING_TYPES.business():
						statuses[i] = False
						continue

				elif building_type_sid == 3: # окреме
					if marker['building_type_sid'] != TRADE_BUILDING_TYPES.separate():
						statuses[i] = False
						continue


			if 'electricity' in filters:
				if (not 'electricity' in marker) or (not marker['electricity']):
					statuses[i] = False
					continue

			if  'gas' in filters:
				if (not 'gas' in marker) or (not marker['gas']):
					statuses[i] = False
					continue

			if 'hot_water' in filters:
				if (not 'hot_water' in marker) or (not marker['hot_water']):
					statuses[i] = False
					continue

			if  'cold_water' in filters:
				if (not 'cold_water' in marker) or (not marker['cold_water']):
					statuses[i] = False
					continue

		result = []
		for i in range(len(statuses)):
			if statuses[i]:
				result.append(publications[i])
		return result



class GaragesMarkersManager(BaseMarkersManager):
	def __init__(self):
		super(GaragesMarkersManager, self).__init__(OBJECTS_TYPES.garage())


	def record_min_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'hash_id',
			'for_sale', 'for_rent',
			'sale_terms__price', 'sale_terms__currency_sid',
			'rent_terms__price', 'rent_terms__currency_sid',
			'body__pit', 'body__area', 'body__ceiling_height',)


	def serialize_publication(self, record):
		if True not in (record.for_sale, record.for_rent):
			raise self.SerializationError('Object must be "for sale", "for rent", or both. Nothing selected.')

		if record.body.rooms_count is None:
			raise self.SerializationError('rooms_count is required but absent.')

		if record.body.total_area is None:
			raise self.SerializationError('total_area is required but absent.')


		data = [
			record.hash_id,
			record.for_sale,
		    record.for_rent,

			float(record.body.area), # json can't handle decimal
			float(record.body.ceiling_height), # json can't handle decimal

			record.body.pit,
		]


		if record.for_sale:
			if record.sale_terms.price is None:
				raise self.SerializationError('sale_price is required but absent.')

			data.extend([
		        float(record.sale_terms.price), # json can't handle decimal
			    record.sale_terms.currency_sid,
			])


		if record.for_rent:
			data.extend([
				float(record.rent_terms.price), # json can't handle decimal
			    record.rent_terms.currency_sid,
			])


		digest = json.dumps(data).replace('true', 't').replace('false', 'f').replace(' ', '')
		return digest


	def deserialize_marker_data(self, data):
		data = json.loads(data.replace('t', 'true').replace('f', 'false'))

		index = iter(xrange(0, len(data)))
		deserialized_data = {
			'hash_id':              data[next(index)],
			'for_sale':             data[next(index)],
		    'for_rent':             data[next(index)],

		    'area':                 data[next(index)],
		    'ceiling_height':       data[next(index)],

			'pit':                  data[next(index)],
		}


		if deserialized_data['for_sale']:
			deserialized_data.update({
				'sale_price': data[next(index)],
				'sale_currency_sid': data[next(index)],
			})


		if deserialized_data['for_rent']:
			deserialized_data.update({
				'rent_price': data[next(index)],
				'rent_currency_sid': data[next(index)],
			})


		return deserialized_data


	def marker_brief(self, marker, filters=None):
		"""
		Сформує бриф для маркеру на основі даних, переданих у фільтрі.
		(В даний момент враховується лише валюта запиту)
		"""

		# todo: додати зміну видачі в залежності від фільтрів.
		# Наприклад, якщо задано к-сть кімнат від 1 до 1 - нема змісту показувати в брифі к-сть кімнат,
		# ітак ясно, що їх буде не більше одної.

		result = {
			'id': marker['hash_id']
		}

		# Гривня як базова валюта обирається згідно з чинним законодавством,
		# але якщо у фільтрі вказана інша - переформатувати бриф на неї.
		if filters is None:
			currency = CURRENCIES.uah()
		else:
			currency = filters.get('currency_sid', CURRENCIES.uah())


		if marker.get('for_sale', False):
			area = u'{0:.2f}'.format(marker.get('area')).rstrip('0').rstrip('.') \
				if marker.get('area') else None
			sale_price = self.format_price(marker['sale_price'], marker['sale_currency_sid'], currency)
			result.update({
				'd0': u'Площадь: {0} м²'.format(area),
				'd1': u'{0} {1}'.format(sale_price, self.format_currency(currency)),
			})
			return result

		elif marker.get('for_rent', False):
			area = u'Площадь: {0:.2f} м²'.format(marker.get('area')).rstrip('0').rstrip('.') \
				if marker.get('area') else None
			rent_price = self.format_price(marker['rent_price'], marker['rent_currency_sid'], currency)
			result.update({
				'd0': u'Площадь: {0} м²'.format(area) if area else u'Площадь неизвестна',
				'd1': u'{0} {1}'.format(rent_price, self.format_currency(currency)),
			})
			return result

		raise RuntimeException('Marker is not for sale and not for rent.')


	def filter(self, publications, filters):
		# WARNING:
		#   дана функція для економії часу виконання не виконує deepcopy над publications

		if filters is None:
			return publications

		operation_sid = filters.get('operation_sid')
		if operation_sid is None:
			raise InvalidArgument('Invalid conditions. Operation_sid is absent.')


		# Перед фільтруванням оголошень слід перевірити цілісність і коректність об’єкту умов.
		# На даному етапі виконується перевірка всіх обов’язкових полів filters.
		# Дану перевірку винесено за цикл фільтрування щоб підвищити швидкодію,
		# оскільки об’єкт filters не змінюється в ході фільтрування і достатньо перевіріити його лише раз.
		currency_sid = filters.get('currency_sid')
		if currency_sid is None:
			# Перевіряти фільтри цін має зміст лише тоді, коли задано валюту фільтру,
			# інакше неможливо привести валюту ціни з фільтра до валюти з оголошення.
			# На фронтенді валюта повинна бути задана за замовчуванням.
			raise InvalidArgument('sale_currency_sid is absent.')
		elif currency_sid not in CURRENCIES.values():
			raise InvalidArgument('currency_sid is invalid.')

		if operation_sid not in [0, 1]:
			raise InvalidArgument('Invalid operation_sid.')


		# Для відбору елементів зі списку publications, використовується список statuses.
		# Кість елементів цього списку відповідає к-сті елементів publications.
		# На початку фільтрування всі елементи statuses встановлені в True.
		# Під час фільтрування деякі з них будуть встановлені в False.
		# На завершальному етапі зі списку publications будуть відібрані лише ті елементи,
		# відповідний елемент statuses яких встановлений в True.
		#
		# Додатковий список використовується для підвищення швидкодії фільтрування,
		# оскільки зміна True/False відбуваєтсья в рази швидше, ніж вилучення елементів зі списку
		# з повторною його перебудовою на кожній перевірці та ітерації.
		statuses = [True] * len(publications)


		for i in range(len(statuses)):
			# Якщо даний запис вже позначений як виключений — не аналізувати його.
			if not statuses[i]:
				continue

			marker = publications[i][1]

			# operation type
			if operation_sid == 0:
				if not marker.get('for_sale', False):
					statuses[i] = False
					continue

			elif operation_sid == 1:
				if not marker.get('for_rent', False):
					statuses[i] = False
					continue


			# price
			price_min = filters.get('price_from')
			price_max = filters.get('price_to')
			if price_min is not None:
				price_min = convert_currency(price_min, currency_sid, marker['sale_currency_sid'])
			if price_max is not None:
				price_max = convert_currency(price_max, currency_sid, marker['sale_currency_sid'])


			if (price_max is not None) and (price_min is not None):
				if not price_min <= marker['sale_price'] <= price_max:
					statuses[i] = False
					continue

			elif price_min is not None:
				if not price_min <= marker['sale_price']:
					statuses[i] = False
					continue

			elif price_max is not None:
				if not marker['sale_price'] <= price_max:
					statuses[i] = False
					continue

			# total area
			total_area_min = filters.get('total_area_from')
			total_area_max = filters.get('total_area_to')
			total_area = marker.get('total_area')

			if (total_area_max is not None) or (total_area_min is not None):
				# Поле може бути не обов’язковим.
				# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
				# відхилити запис через неможливість аналізу.
				if total_area is None:
					statuses[i] = False
					continue

			if (total_area_max is not None) and (total_area_min is not None):
				if not total_area_min <= total_area <= total_area_max:
					statuses[i] = False
					continue

			elif total_area_min is not None:
				if not total_area_min <= total_area:
					statuses[i] = False
					continue

			elif total_area_max is not None:
				if not total_area <= total_area_max:
					statuses[i] = False
					continue
					
					
			# ceiling height
			ceiling_height_min = filters.get('ceiling_height_from')
			ceiling_height_max = filters.get('ceiling_height_to')
			ceiling_height = marker.get('ceiling_height')

			if (ceiling_height_max is not None) or (ceiling_height_min is not None):
				# Поле може бути не обов’язковим.
				# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
				# відхилити запис через неможливість аналізу.
				if ceiling_height is None:
					statuses[i] = False
					continue

			if (ceiling_height_max is not None) and (ceiling_height_min is not None):
				if not ceiling_height_min <= ceiling_height <= ceiling_height_max:
					statuses[i] = False
					continue

			elif ceiling_height_min is not None:
				if not ceiling_height_min <= ceiling_height:
					statuses[i] = False
					continue

			elif ceiling_height_max is not None:
				if not ceiling_height <= ceiling_height_max:
					statuses[i] = False
					continue


			if 'pit' in filters:
				if (not 'pit' in marker) or (not marker['pit']):
					statuses[i] = False
					continue

		result = []
		for i in range(len(statuses)):
			if statuses[i]:
				result.append(publications[i])
		return result



class LandsMarkersManager(BaseMarkersManager):
	def __init__(self):
		super(LandsMarkersManager, self).__init__(OBJECTS_TYPES.land())


	def record_min_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'hash_id',
			'for_sale', 'for_rent',
			'sale_terms__price', 'sale_terms__currency_sid',
			'rent_terms__price', 'rent_terms__currency_sid',
			'body__electricity', 'body__gas', 'body__sewerage', 'body__water', 'body__area')


	def serialize_publication(self, record):
		if True not in (record.for_sale, record.for_rent):
			raise self.SerializationError('Object must be "for sale", "for rent", or both. Nothing selected.')

		if record.body.rooms_count is None:
			raise self.SerializationError('rooms_count is required but absent.')

		if record.body.total_area is None:
			raise self.SerializationError('total_area is required but absent.')


		data = [
			record.hash_id,
			record.for_sale,
		    record.for_rent,

			float(record.body.area), # json can't handle decimal

			record.body.electricity,
		    record.body.gas,
		    record.body.sewerage,
		    record.body.water,
		]


		if record.for_sale:
			if record.sale_terms.price is None:
				raise self.SerializationError('sale_price is required but absent.')

			data.extend([
		        float(record.sale_terms.price), # json can't handle decimal
			    record.sale_terms.currency_sid,
			])


		if record.for_rent:
			data.extend([
				float(record.rent_terms.price), # json can't handle decimal
			    record.rent_terms.currency_sid,
			])


		digest = json.dumps(data).replace('true', 't').replace('false', 'f').replace(' ', '')
		return digest


	def deserialize_marker_data(self, data):
		data = json.loads(data.replace('t', 'true').replace('f', 'false'))

		index = iter(xrange(0, len(data)))
		deserialized_data = {
			'hash_id':              data[next(index)],
			'for_sale':             data[next(index)],
		    'for_rent':             data[next(index)],

		    'area':                 data[next(index)],

			'electricity':          data[next(index)],
		    'gas':                  data[next(index)],
		    'sewerage':             data[next(index)],
		    'water':                data[next(index)],
		}


		if deserialized_data['for_sale']:
			deserialized_data.update({
				'sale_price': data[next(index)],
				'sale_currency_sid': data[next(index)],
			})


		if deserialized_data['for_rent']:
			deserialized_data.update({
				'rent_price': data[next(index)],
				'rent_currency_sid': data[next(index)],
			})


		return deserialized_data


	def marker_brief(self, marker, filters=None):
		"""
		Сформує бриф для маркеру на основі даних, переданих у фільтрі.
		(В даний момент враховується лише валюта запиту)
		"""

		# todo: додати зміну видачі в залежності від фільтрів.
		# Наприклад, якщо задано к-сть кімнат від 1 до 1 - нема змісту показувати в брифі к-сть кімнат,
		# ітак ясно, що їх буде не більше одної.

		result = {
			'id': marker['hash_id']
		}

		# Гривня як базова валюта обирається згідно з чинним законодавством,
		# але якщо у фільтрі вказана інша - переформатувати бриф на неї.
		if filters is None:
			currency = CURRENCIES.uah()
		else:
			currency = filters.get('currency_sid', CURRENCIES.uah())


		if marker.get('for_sale', False):
			area = u'{0:.2f}'.format(marker.get('area')).rstrip('0').rstrip('.') \
				if marker.get('area') else None
			sale_price = self.format_price(marker['sale_price'], marker['sale_currency_sid'], currency)
			result.update({
				'd0': u'Площадь: {0} м²'.format(area),
				'd1': u'{0} {1}'.format(sale_price, self.format_currency(currency)),
			})
			return result

		elif marker.get('for_rent', False):
			area = u'Площадь: {0:.2f} м²'.format(marker.get('area')).rstrip('0').rstrip('.') \
				if marker.get('area') else None
			rent_price = self.format_price(marker['rent_price'], marker['rent_currency_sid'], currency)
			result.update({
				'd0': u'Площадь: {0} м²'.format(area) if area else u'Площадь неизвестна',
				'd1': u'{0} {1}'.format(rent_price, self.format_currency(currency)),
			})
			return result

		raise RuntimeException('Marker is not for sale and not for rent.')


	def filter(self, publications, filters):
		# WARNING:
		#   дана функція для економії часу виконання не виконує deepcopy над publications

		if filters is None:
			return publications

		operation_sid = filters.get('operation_sid')
		if operation_sid is None:
			raise InvalidArgument('Invalid conditions. Operation_sid is absent.')


		# Перед фільтруванням оголошень слід перевірити цілісність і коректність об’єкту умов.
		# На даному етапі виконується перевірка всіх обов’язкових полів filters.
		# Дану перевірку винесено за цикл фільтрування щоб підвищити швидкодію,
		# оскільки об’єкт filters не змінюється в ході фільтрування і достатньо перевіріити його лише раз.
		currency_sid = filters.get('currency_sid')
		if currency_sid is None:
			# Перевіряти фільтри цін має зміст лише тоді, коли задано валюту фільтру,
			# інакше неможливо привести валюту ціни з фільтра до валюти з оголошення.
			# На фронтенді валюта повинна бути задана за замовчуванням.
			raise InvalidArgument('sale_currency_sid is absent.')
		elif currency_sid not in CURRENCIES.values():
			raise InvalidArgument('currency_sid is invalid.')

		if operation_sid not in [0, 1]:
			raise InvalidArgument('Invalid operation_sid.')


		# Для відбору елементів зі списку publications, використовується список statuses.
		# Кість елементів цього списку відповідає к-сті елементів publications.
		# На початку фільтрування всі елементи statuses встановлені в True.
		# Під час фільтрування деякі з них будуть встановлені в False.
		# На завершальному етапі зі списку publications будуть відібрані лише ті елементи,
		# відповідний елемент statuses яких встановлений в True.
		#
		# Додатковий список використовується для підвищення швидкодії фільтрування,
		# оскільки зміна True/False відбуваєтсья в рази швидше, ніж вилучення елементів зі списку
		# з повторною його перебудовою на кожній перевірці та ітерації.
		statuses = [True] * len(publications)


		for i in range(len(statuses)):
			# Якщо даний запис вже позначений як виключений — не аналізувати його.
			if not statuses[i]:
				continue

			marker = publications[i][1]

			# operation type
			if operation_sid == 0:
				if not marker.get('for_sale', False):
					statuses[i] = False
					continue

			elif operation_sid == 1:
				if not marker.get('for_rent', False):
					statuses[i] = False
					continue


			# price
			marker_currency = marker.get('sale_currency_sid')
			if marker_currency is None:
				marker_currency = marker.get('rent_currency_sid')

			price_min = filters.get('price_from')
			price_max = filters.get('price_to')
			if price_min is not None:
				price_min = convert_currency(price_min, currency_sid, marker_currency)
			if price_max is not None:
				price_max = convert_currency(price_max, currency_sid, marker_currency)


			if (price_max is not None) and (price_min is not None):
				if not price_min <= marker['sale_price'] <= price_max:
					statuses[i] = False
					continue

			elif price_min is not None:
				if not price_min <= marker['sale_price']:
					statuses[i] = False
					continue

			elif price_max is not None:
				if not marker['sale_price'] <= price_max:
					statuses[i] = False
					continue


			# area
			area_min = filters.get('area_from')
			area_max = filters.get('area_to')
			area = marker.get('area')

			if (area_max is not None) or (area_min is not None):
				# Поле може бути не обов’язковим.
				# У випадку, коли воно задане у фільтрі, але відсутнє в записі маркера —
				# відхилити запис через неможливість аналізу.
				if area is None:
					statuses[i] = False
					continue

			if (area_max is not None) and (area_min is not None):
				if not area_min <= area <= area_max:
					statuses[i] = False
					continue

			elif area_min is not None:
				if not area_min <= area:
					statuses[i] = False
					continue

			elif area_max is not None:
				if not area <= area_max:
					statuses[i] = False
					continue


			if 'electricity' in filters:
				if (not 'electricity' in marker) or (not marker['electricity']):
					statuses[i] = False
					continue

			if  'gas' in filters:
				if (not 'gas' in marker) or (not marker['gas']):
					statuses[i] = False
					continue

			if 'water' in filters:
				if (not 'water' in marker) or (not marker['water']):
					statuses[i] = False
					continue

			if  'sewerage' in filters:
				if (not 'sewerage' in marker) or (not marker['sewerage']):
					statuses[i] = False
					continue

		result = []
		for i in range(len(statuses)):
			if statuses[i]:
				result.append(publications[i])
		return result
