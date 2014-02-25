#coding=utf-8
import copy
import mmh3

import abc
from django.core.exceptions import ObjectDoesNotExist

from core.currencies.currencies_manager import convert as convert_currency
from core.markers_servers.exceptions import TooBigTransaction, SerializationError, DeserializationError
from core.markers_servers.utils import DegreeSegmentPoint, Point, SegmentPoint, DegreePoint
from core.publications.constants import OBJECTS_TYPES, HEAD_MODELS, CURRENCIES
from mappino.wsgi import redis_connections


class BaseMarkersManager(object):
	"""
	Передбачено, що кожному типу об’єктів відповідатиме власний менеджер маркерів.
	Але, оскільки деякий функціонал у всіх менеждереів спільний, — його винесено в даний клас.
	"""
	__metaclass__ = abc.ABCMeta


	def __init__(self, tid):
		if tid not in OBJECTS_TYPES.values():
			raise ValueError('invalid @tid.')
		self.tid = tid
		self.model = HEAD_MODELS[tid]

		self.redis = redis_connections['steady']
		self.redis_segments_hashes_prefix = 'segments_hashes'
		self.separator = ';'
		self.digest_separator = ':'


	def markers(self, ne, sw, condition=None):
		# ToDo: описати condition в коментарі
		"""
		Args:
			ne: (North East) Point з координатами північно-західного кута в’юпорта.
			sw: (South West) Point з координатами південно-східного кута в’юпорта.

		Повертає набір маркерів для в’юпорта з координатами ne та sw у форматі:
		>> lat;lng градуса:
		>>   lat;lng маркера:
		>>     дані маркера (id, ...)

		В деяких випадках може повернути маркери суміжних сегментів із тими, які були запитані.
		"""

		if (ne is None) or (sw is None):
			raise ValueError('Invalid coordinates.')
		# todo: додати перевірку для condition

		result = {}
		for digest in self.__segments_digests(ne, sw):
			degree = self.__degree_from_digest(digest)

			coordinates = self.redis.hkeys(digest)
			pipe = self.redis.pipeline()
			for c in coordinates:
				pipe.hget(digest, c)

			markers = pipe.execute()
			if markers:
				result[degree] = {}

			for record in zip(coordinates, markers):
				coordinates = record[0]
				item = record[1]

				marker_data = self.deserialize_publication_record(item)
				result[degree][coordinates] = self.marker_brief(marker_data, condition)
		return result


	def viewport_hash(self, ne, sw):
		"""
		Args:
			ne: (North East) Point з координатами північно-західного кута в’юпорта.
			sw: (South West) Point з координатами південно-східного кута в’юпорта.

		Повертає хеш всіх сегментів, які потрапляють у в’юпорт з координатами ne та sw.
		Хеш вираховується як hash(хеш 1-го сегменту + хеш 2-го сегменту + ... + хеш N-го сегменту).
		Для підрахунку хешу використовується MurmurHash. (див. док. __update_segment_hash)
		"""
		digests = self.__segments_digests(ne, sw)

		pipe = self.redis.pipeline()
		for digest in digests:
			pipe.hget(self.redis_segments_hashes_prefix, digest)

		key = ''
		for h in pipe.execute():
			if h is not None:
				key += h
		return str(mmh3.hash(key))


	def add_publication(self, hid):
		"""
		Args:
			hid: id head-запису оголошення.

		Сериалізує дані оголошення у формат для зберігання в індексі маркерів і
		оновить сегмент, в який потрапляє маркер даного оголошення.
		Оновленню в тому числі підлягатиме хеш сегменту.
		"""
		if hid is None:
			raise ValueError('Invalid hid.')

		try:
			record = self.record_queryset(hid).only(
				'degree_lng', 'degree_lat', 'segment_lng', 'segment_lat', 'pos_lng', 'pos_lat')[0]
		except IndexError:
			raise ObjectDoesNotExist('Invalid hid. Object with such hid does not exist.')

		degree = DegreePoint(record.degree_lat, record.degree_lng)
		segment = SegmentPoint(record.segment_lat, record.segment_lng)
		seg_digest = self.__segment_digest(degree, segment)

		sector = Point(record.segment_lat, record.segment_lng)
		position = Point(record.pos_lat, record.pos_lng)
		pos_digest = self.__position_digest(sector, position)

		data = self.serialize_publication_record(record)
		self.redis.hset(seg_digest, pos_digest, data)
		self.__update_segment_hash(seg_digest, hid)


	def __segments_digests(self, ne, sw):
		"""
		Args:
			ne: (North East) Point з координатами північно-західного кута в’юпорта.
			sw: (South West) Point з координатами південно-східного кута в’юпорта.

		Повертає список всіх дайджестів сегментів, які потрапляють у в’юпорт.
		"""

		start = DegreeSegmentPoint(ne.lat, ne.lng)
		stop = DegreeSegmentPoint(sw.lat, sw.lng)

		# Мапи google деколи повертають координати так, що stop опиняється перед start,
		# і тоді алгоритм починає пробіг по всьому глобусу і падає на перевірці розміру транзакції.
		# Дані перетворення видозмінюють координати так, щоб start завжди був перед stop,
		# неважливо в якому порядку вони прийдуть.
		if start.degree.lng > stop.degree.lng:
			start.degree.lng, stop.degree.lng = stop.degree.lng, start.degree.lng
		elif start.segment.lng > stop.segment.lng:
			start.segment.lng, stop.segment.lng = stop.segment.lng, start.segment.lng

		if start.degree.lat < stop.degree.lat:
			start.degree.lat, stop.degree.lat = stop.degree.lat, start.degree.lat
		elif start.segment.lat < stop.segment.lat:
			start.segment.lat, stop.segment.lat = stop.segment.lat, start.segment.lat

		digests = []
		current = copy.deepcopy(start)
		while True:
			current.degree.lng = start.degree.lng
			current.segment.lng = start.segment.lng

			while True:
				digests.append(self.__segment_digest(current.degree, current.segment))

				# Заборонити одночасну вибірку маркерів з великої к-сті сегментів.
				# Таким чином можна уберегтись від занадто великих транзакцій і накопичування
				# великої к-сті запитів від інших користувачів в черзі на обробку.
				if len(digests) > 5*5:
					raise TooBigTransaction()

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


	def __degree_from_digest(self, digest):
		"""
		Поверне градус сегмента у форматі "lat;lng".
		Відомості про градус беруться з дайджеста сегмента.
		"""
		index = digest.find(self.digest_separator)
		if index < 0:
			raise RuntimeError('Invalid digest.')

		coordinates = digest[index+1:].split(self.digest_separator)
		if ('' in coordinates) or (None in coordinates):
			raise RuntimeError('Invalid digest.')

		return coordinates[0] + ';' + coordinates[1]


	def __update_segment_hash(self, digest, record_id):
		"""
		Кожен сегмент маркерів має власний хеш.
		Він використовується, наприклад, як etag для запитів на отримання маркерів.
		Даний метод оновить хеш для сегменту з дайджестом digest.

		Для хешування використовується MurmurHash,
		оскільки він дуже швидкий і видає короткі дайджести,
		а криптостійкість в даному випадку не важлива.

		Новий хеш вираховується за формулою h = hash(попередній хеш + record_id)
		"""
		current_hash = self.redis.hget(self.redis_segments_hashes_prefix, digest)
		if current_hash is None:
			current_hash = ''

		segment_hash = mmh3.hash(current_hash + str(record_id))
		self.redis.hset(self.redis_segments_hashes_prefix, digest, segment_hash)


	@staticmethod
	def __format_price(price, base_currency, destination_currency):
		result = u''
		if base_currency != destination_currency:
			result += u'≈'

		converted_price = convert_currency(price, base_currency, destination_currency)
		if int(converted_price) == converted_price:
			return result + u'{:0,.0f}'.format(converted_price)
		return result + u'{:0,.2f}'.format(converted_price)


	@abc.abstractmethod
	def serialize_publication_record(self, record):
		return


	@abc.abstractmethod
	def deserialize_publication_record(self, record):
		return


	@abc.abstractmethod
	def marker_brief(self, data, condition=None):
		pass


	@abc.abstractmethod
	def record_queryset(self, hid):
		"""
		Повертає head-запис лише з тими полями моделі,
		які прийматимуть участь у формуванні брифу маркеру і фільтрів.
		"""
		return self.model.objects(id=hid)


	@staticmethod
	@abc.abstractmethod
	def filter(publications, conditions):
		return



class FlatsMarkersManager(BaseMarkersManager):
	def __init__(self):
		super(FlatsMarkersManager, self).__init__(OBJECTS_TYPES.flat())


	def record_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'for_sale', 'for_rent',
			'sale_terms__price', 'sale_terms__currency_sid',

			'rent_terms__price', 'rent_terms__currency_sid', 'rent_terms__period_sid',
		    'rent_terms__persons_count', 'rent_terms__family', 'rent_terms__foreigners',

			'body__electricity', 'body__gas', 'body__hot_water', 'body__cold_water', 'body__lift',
			'body__market_type_sid', 'body__heating_type_sid', 'body__ind_heating_type_sid',
			'body__rooms_count', 'body__total_area', 'body__floor_count')


	def serialize_publication_record(self, record):
		# common terms
		#-- bitmask
		bitmask = ''
		bitmask += '1' if record.for_sale else '0'
		bitmask += '1' if record.for_rent else '0'
		bitmask += '1' if record.body.electricity else '0'
		bitmask += '1' if record.body.gas else '0'
		bitmask += '1' if record.body.hot_water else '0'
		bitmask += '1' if record.body.cold_water else '0'
		bitmask += '1' if record.body.lift else '0'
		bitmask += '{0:01b}'.format(record.body.market_type_sid)  # 1 bit
		bitmask += '{0:02b}'.format(record.body.heating_type_sid) # 2 bits
		bitmask += '{0:02b}'.format(record.body.rooms_planning_sid) # 2 bits
		if len(bitmask) != 12:
			raise SerializationError('Bitmask corruption. Potential deserialization error.')


		#-- data
		data = ''
		data += str(record.id) + self.separator

		# WARNING: field can be None
		if record.body.rooms_count is not None:
			data += str(record.body.rooms_count) + self.separator
		else: data += self.separator

		# WARNING: field can be None
		if record.body.total_area is not None:
			data += str(record.body.total_area) + self.separator
		else: data += self.separator

		# WARNING: field can be None
		if record.body.floor is not None:
			data += str(record.body.floor) + self.separator
		else: data += self.separator


		#-- sale terms
		if record.for_sale:
			bitmask += '{0:02b}'.format(record.sale_terms.currency_sid) # 2 bits
			if len(bitmask) != 14:
				raise SerializationError('Bitmask corruption. Potential deserialization error.')

			# REQUIRED field
			if record.sale_terms.price is not None:
				data += str(record.sale_terms.price) + self.separator
				data += str(record.sale_terms.currency_sid) + self.separator
			else:
				raise SerializationError('Sale price is required.')


		#-- rent terms
		if record.for_rent:
			bitmask += '{0:02b}'.format(record.rent_terms.period_sid)   # 2 bits
			bitmask += '{0:02b}'.format(record.rent_terms.currency_sid) # 2 bits
			bitmask += '1' if record.rent_terms.family else '0'
			bitmask += '1' if record.rent_terms.foreigners else '0'
			if len(bitmask) not in (22, 20):
				raise SerializationError('Bitmask corruption. Potential deserialization error.')

			# REQUIRED field
			if record.rent_terms.price is not None:
				data += str(record.rent_terms.price) + self.separator
			else:
				raise SerializationError('Rent price is required.')

			# REQUIRED field
			if record.rent_terms.currency_sid is not None:
				data += str(record.rent_terms.currency_sid) + self.separator
			else:
				raise SerializationError('Rent price is required.')

			# REQUIRED field
			if record.rent_terms.currency_sid is not None:
				data += str(record.rent_terms.currency_sid) + self.separator
			else:
				raise SerializationError('Rent price is required.')

			# WARNING: next fields can be None
			if record.rent_terms.persons_count is not None:
				data += str(record.rent_terms.persons_count) + self.separator
			else:
				data += self.separator


		# Інвертація бітової маски для того, щоб біти типу операції опинились справа.
		# Це пов’язано із тим, що при десериалізації старші біти, втрачаються, якщо вони нулі.
		# Доповнити маску неможливо, оскільки для доповнення слід знати точну к-сть біт маски,
		# а це залежить від того чи продаєтсья об’єкт, чи здаєтсья в оренду, чи і те і інше.
		bitmask = bitmask[::-1]

		record_data = data + self.separator +  str(int(bitmask, 2))
		if record_data[-1] == self.separator:
			record_data = record_data[:-1]
		return record_data


	def deserialize_publication_record(self, record_data):
		parts = record_data.split(self.separator)
		bitmask = bin(int(parts[-1]))[2:]
		data = {
			'id': int(parts[0]),
			'rooms_count':  int(parts[1])   if parts[1] != '' else None,
			'total_area':   float(parts[2]) if parts[2] != '' else None,
			'floor':        int(parts[3])   if parts[3] != '' else None,

		    'electricity':  (bitmask[-3] == '1'),
			'gas':          (bitmask[-4] == '1'),
			'hot_water':    (bitmask[-5] == '1'),
			'cold_water':   (bitmask[-6] == '1'),
			'lift':         (bitmask[-7] == '1'),

		    'market_type_sid':      int('' + bitmask[-8]),
		    'heating_type_sid':     int('' + bitmask[-9]  + bitmask[-10]),
		    'rooms_planning_sid':   int('' + bitmask[-11] + bitmask[-12])
		}

		if bitmask[-1] == '1':
			# sale terms
			data.update({
				'for_sale': True,
			    'sale_price': float(parts[4]),
			    'sale_currency_sid': int(parts[5]),
			})

			# check for rent terms
			if bitmask[-2] == '1':
				data.update({
					'for_rent': True,
					'rent_price': float(parts[6]),
				    'rent_currency_sid': int(parts[7]),
				    'persons_count': int(parts[8]) if parts[8] != '' else None
				})

		else:
			if bitmask[-2] == '1':
				# rent terms
				data.update({
					'for_rent': True,
					'rent_price': float(parts[4]),
					'rent_currency_sid': float(parts[5]),
				    'persons_count': int(parts[6]) if parts[6] != '' else None
				})
		return data


	def marker_brief(self, data, condition=None):
		if condition is None:
			# Фільтри не виставлені, віддаєм у форматі за замовчуванням
			if (data.get('for_sale', False)) and (data.get('for_rent', False)):
				return {
					'id': data['id'],
					'd0': u'Продажа: ' + self.__format_price(
						data['sale_price'],
						data['sale_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',

					'd1': u'Аренда: ' + self.__format_price(
						data['rent_price'],
						data['rent_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			elif data.get('for_sale', False):
				return {
					'id': data['id'],
					'd0': u'Комнат: ' + str(data['rooms_count']),
					'd1': self.__format_price(
						data['sale_price'],
						data['sale_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			elif data.get('for_rent', False):
				return{
					'id': data['id'],
					'd0': u'Мест: ' + str(data['persons_count']),
					'd1': self.__format_price(
						data['rent_price'],
						data['rent_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			else:
				raise DeserializationError()

		else:
			# todo: додати сюди відомості про об’єкт в залежності від фільтрів
			# todo: додати конввертацію валют в залженост від фільтрів
			pass


	@staticmethod
	def filter(publications, conditions):
		return



class ApartmentsMarkersManager(BaseMarkersManager):
	def __init__(self):
		super(ApartmentsMarkersManager, self).__init__(OBJECTS_TYPES.apartments())


	def record_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'for_sale', 'for_rent',
			'sale_terms__price', 'sale_terms__currency_sid',

			'rent_terms__price', 'rent_terms__currency_sid', 'rent_terms__period_sid',
		    'rent_terms__persons_count', 'rent_terms__family', 'rent_terms__foreigners',

			'body__electricity', 'body__gas', 'body__hot_water', 'body__cold_water', 'body__lift',
			'body__market_type_sid', 'body__heating_type_sid', 'body__ind_heating_type_sid',
			'body__rooms_count', 'body__total_area', 'body__floor_count')


	def serialize_publication_record(self, record):
		# common terms
		#-- bitmask
		bitmask = ''
		bitmask += '1' if record.for_sale else '0'
		bitmask += '1' if record.for_rent else '0'
		bitmask += '1' if record.body.electricity else '0'
		bitmask += '1' if record.body.gas else '0'
		bitmask += '1' if record.body.hot_water else '0'
		bitmask += '1' if record.body.cold_water else '0'
		bitmask += '1' if record.body.lift else '0'
		bitmask += '{0:01b}'.format(record.body.market_type_sid)  # 1 bit
		bitmask += '{0:02b}'.format(record.body.heating_type_sid) # 2 bits
		bitmask += '{0:02b}'.format(record.body.rooms_planning_sid) # 2 bits
		if len(bitmask) != 12:
			raise SerializationError('Bitmask corruption. Potential deserialization error.')


		#-- data
		data = ''
		data += str(record.id) + self.separator

		# WARNING: field can be None
		if record.body.rooms_count is not None:
			data += str(record.body.rooms_count) + self.separator
		else: data += self.separator

		# WARNING: field can be None
		if record.body.total_area is not None:
			data += str(record.body.total_area) + self.separator
		else: data += self.separator

		# WARNING: field can be None
		if record.body.floor is not None:
			data += str(record.body.floor) + self.separator
		else: data += self.separator


		#-- sale terms
		if record.for_sale:
			bitmask += '{0:02b}'.format(record.sale_terms.currency_sid) # 2 bits
			if len(bitmask) != 14:
				raise SerializationError('Bitmask corruption. Potential deserialization error.')

			# REQUIRED field
			if record.sale_terms.price is not None:
				data += str(record.sale_terms.price) + self.separator
				data += str(record.sale_terms.currency_sid) + self.separator
			else:
				raise SerializationError('Sale price is required.')

			# REQUIRED field
			if record.sale_terms.currency_sid is not None:
				data += str(record.sale_terms.currency_sid) + self.separator
			else:
				raise SerializationError('Sale price is required.')


		#-- rent terms
		if record.for_rent:
			bitmask += '{0:02b}'.format(record.rent_terms.period_sid)   # 2 bits
			bitmask += '{0:02b}'.format(record.rent_terms.currency_sid) # 2 bits
			bitmask += '1' if record.rent_terms.family else '0'
			bitmask += '1' if record.rent_terms.foreigners else '0'
			if len(bitmask) not in (22, 20):
				raise SerializationError('Bitmask corruption. Potential deserialization error.')

			# REQUIRED field
			if record.rent_terms.price is not  None:
				data += str(record.rent_terms.price) + self.separator
			else:
				raise SerializationError('Rent price is required.')

			# REQUIRED field
			if record.rent_terms.currency_sid is not None:
				data += str(record.rent_terms.currency_sid) + self.separator
			else:
				raise SerializationError('Rent price is required.')

			# WARNING: next fields can be None
			if record.rent_terms.persons_count is not None:
				data += str(record.rent_terms.persons_count) + self.separator
			else:
				data += self.separator


		# Інвертація бітової маски для того, щоб біти типу операції опинились справа.
		# Це пов’язано із тим, що при десериалізації старші біти, втрачаються, якщо вони нулі.
		# Доповнити маску неможливо, оскільки для доповнення слід знати точну к-сть біт маски,
		# а це залежить від того чи продаєтсья об’єкт, чи здаєтсья в оренду, чи і те і інше.
		bitmask = bitmask[::-1]

		record_data = data + self.separator +  str(int(bitmask, 2))
		if record_data[-1] == self.separator:
			record_data = record_data[:-1]
		return record_data


	def deserialize_publication_record(self, record_data):
		parts = record_data.split(self.separator)
		bitmask = bin(int(parts[-1]))[2:]
		data = {
			'id': int(parts[0]),
			'rooms_count':  int(parts[1])   if parts[1] != '' else None,
			'total_area':   float(parts[2]) if parts[2] != '' else None,
			'floor':        int(parts[3])   if parts[3] != '' else None,

		    'electricity':  (bitmask[-3] == '1'),
			'gas':          (bitmask[-4] == '1'),
			'hot_water':    (bitmask[-5] == '1'),
			'cold_water':   (bitmask[-6] == '1'),
			'lift':         (bitmask[-7] == '1'),

		    'market_type_sid':      int('' + bitmask[-8]),
		    'heating_type_sid':     int('' + bitmask[-9]  + bitmask[-10]),
		    'rooms_planning_sid':   int('' + bitmask[-11] + bitmask[-12])
		}

		if bitmask[-1] == '1':
			# sale terms
			data.update({
				'for_sale': True,
			    'sale_price': float(parts[4]),
			    'sale_currency_sid': int(parts[5]),
			})

			# check for rent terms
			if bitmask[-2] == '1':
				data.update({
					'for_rent': True,
					'rent_price': float(parts[6]),
				    'rent_currency_sid': int(parts[7]),
				    'persons_count': int(parts[8]) if parts[8] != '' else None
				})

		else:
			if bitmask[-2] == '1':
				# rent terms
				data.update({
					'for_rent': True,
					'rent_price': float(parts[4]),
					'rent_currency_sid': float(parts[5]),
				    'persons_count': int(parts[6]) if parts[6] != '' else None
				})
		return data


	def marker_brief(self, data, condition=None):
		if condition is None:
			# Фільтри не виставлені, віддаєм у форматі за замовчуванням
			if (data.get('for_sale', False)) and (data.get('for_rent', False)):
				return {
					'id': data['id'],
					'd0': u'Продажа: ' + self.__format_price(
						data['sale_price'],
						data['sale_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',

					'd1': u'Аренда: ' + self.__format_price(
						data['rent_price'],
						data['rent_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			elif data.get('for_sale', False):
				return {
					'id': data['id'],
					'd0': u'Комнат: ' + str(data['rooms_count']),
					'd1': self.__format_price(
						data['sale_price'],
						data['sale_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			elif data.get('for_rent', False):
				return{
					'id': data['id'],
					'd0': u'Мест: ' + str(data['persons_count']),
					'd1': self.__format_price(
						data['rent_price'],
						data['rent_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			else:
				raise DeserializationError()

		else:
			# todo: додати сюди відомості про об’єкт в залежності від фільтрів
			# todo: додати конввертацію валют в залженост від фільтрів
			pass


	@staticmethod
	def filter(publications, conditions):
		return



class HousesMarkersManager(BaseMarkersManager):
	def __init__(self):
		super(HousesMarkersManager, self).__init__(OBJECTS_TYPES.house())


	def record_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'for_sale', 'for_rent',
			'sale_terms__price', 'sale_terms__currency_sid',

			'rent_terms__price', 'rent_terms__currency_sid', 'rent_terms__period_sid',
		    'rent_terms__persons_count', 'rent_terms__family', 'rent_terms__foreigners',

			'body__electricity', 'body__gas', 'body__sewerage', 'body__hot_water', 'body__cold_water',
			'body__market_type_sid', 'body__heating_type_sid',
			'body__rooms_count', 'body__floors_count')


	def serialize_publication_record(self, record):
		# common terms
		#-- bitmask
		bitmask = ''
		bitmask += '1' if record.for_sale else '0'
		bitmask += '1' if record.for_rent else '0'
		bitmask += '1' if record.body.electricity else '0'
		bitmask += '1' if record.body.gas else '0'
		bitmask += '1' if record.body.sewerage else '0'
		bitmask += '1' if record.body.hot_water else '0'
		bitmask += '1' if record.body.cold_water else '0'
		bitmask += '{0:01b}'.format(record.body.market_type_sid)  # 1 bit
		bitmask += '{0:02b}'.format(record.body.heating_type_sid) # 2 bits
		if len(bitmask) != 10:
			raise SerializationError('Bitmask corruption. Potential deserialization error.')


		#-- data
		data = ''
		data += str(record.id) + self.separator

		# WARNING: next fields can be None
		if record.body.rooms_count is not None:
			data += str(record.body.rooms_count) + self.separator
		else: data += self.separator

		if record.body.floors_count is not None:
			data += str(record.body.floors_count) + self.separator
		else: data += self.separator


		#-- sale terms
		if record.for_sale:
			bitmask += '{0:02b}'.format(record.sale_terms.currency_sid) # 2 bits
			if len(bitmask) != 12:
				raise SerializationError('Bitmask corruption. Potential deserialization error.')

			# REQUIRED field
			if record.sale_terms.price is not None:
				data += str(record.sale_terms.price) + self.separator
			else:
				raise SerializationError('Sale price is required.')

			# REQUIRED field
			if record.sale_terms.currency_sid is not None:
				data += str(record.sale_terms.currency_sid) + self.separator
			else:
				raise SerializationError('Sale price is required.')


		#-- rent terms
		if record.for_rent:
			bitmask += '{0:02b}'.format(record.rent_terms.period_sid)   # 2 bits
			bitmask += '{0:02b}'.format(record.rent_terms.currency_sid) # 2 bits
			bitmask += '1' if record.rent_terms.family else '0'
			bitmask += '1' if record.rent_terms.foreigners else '0'
			if len(bitmask) not in (18, 16):
				raise SerializationError('Bitmask corruption. Potential deserialization error.')

			# REQUIRED field
			if record.rent_terms.price is not  None:
				data += str(record.rent_terms.price) + self.separator
			else:
				raise SerializationError('Rent price is required.')

			# REQUIRED field
			if record.rent_terms.currency_sid is not None:
				data += str(record.rent_terms.currency_sid) + self.separator
			else:
				raise SerializationError('Rent price is required.')

			# WARNING: next fields can be None
			if record.rent_terms.persons_count is not None:
				data += str(record.rent_terms.persons_count) + self.separator
			else:
				data += self.separator


		# Інвертація бітової маски для того, щоб біти типу операції опинились справа.
		# Це пов’язано із тим, що при десериалізації старші біти, втрачаються, якщо вони нулі.
		# Доповнити маску неможливо, оскільки для доповнення слід знати точну к-сть біт маски,
		# а це залежить від того чи продаєтсья об’єкт, чи здаєтсья в оренду, чи і те і інше.
		bitmask = bitmask[::-1]

		record_data = data + self.separator +  str(int(bitmask, 2))
		if record_data[-1] == self.separator:
			record_data = record_data[:-1]
		return record_data


	def deserialize_publication_record(self, record_data):
		parts = record_data.split(self.separator)
		bitmask = bin(int(parts[-1]))[2:]
		data = {
			'id': int(parts[0]),
			'rooms_count':  int(parts[1]) if parts[1] != '' else None,
			'floors_count': int(parts[2]) if parts[2] != '' else None,

		    'electricity': (bitmask[-3] == '1'),
			'gas':         (bitmask[-4] == '1'),
			'sewerage':    (bitmask[-5] == '1'),
			'hot_water':   (bitmask[-6] == '1'),
			'cold_water':  (bitmask[-7] == '1'),

		    'market_type_sid':  int('' + bitmask[-8]),
		    'heating_type_sid': int('' + bitmask[-9] + bitmask[-10]),
		}

		if bitmask[-1] == '1':
			# sale terms
			data.update({
				'for_sale': True,
			    'sale_price': float(parts[3]),
			    'sale_currency_sid': int(parts[4]),
			})

			# check for rent terms
			if bitmask[-2] == '1':
				data.update({
					'for_rent': True,
					'rent_price': float(parts[5]),
				    'rent_currency_sid': int(parts[6]),
				    'persons_count': int(parts[7]) if parts[7] != '' else None
				})

		else:
			if bitmask[-2] == '1':
				# rent terms
				# todo: check indexes
				data.update({
					'for_rent': True,
					'rent_price': float(parts[3]),
					'rent_currency_sid': float(parts[4]),
				    'persons_count': int(parts[5]) if parts[5] != '' else None
				})
		return data


	def marker_brief(self, data, condition=None):
		if condition is None:
			# Фільтри не виставлені, віддаєм у форматі за замовчуванням
			if (data.get('for_sale', False)) and (data.get('for_rent', False)):
				return {
					'id': data['id'],
					'd0': u'Продажа: ' + self.__format_price(
						data['sale_price'],
						data['sale_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',

					'd1': u'Аренда: ' + self.__format_price(
						data['rent_price'],
						data['rent_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			elif data.get('for_sale', False):
				return {
					'id': data['id'],
					'd0': u'Комнат: ' + str(data['rooms_count']),
					'd1': self.__format_price(
						data['sale_price'],
						data['sale_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			elif data.get('for_rent', False):
				return{
					'id': data['id'],
					'd0': u'Мест: ' + str(data['persons_count']),
					'd1': self.__format_price(
						data['rent_price'],
						data['rent_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			else:
				raise DeserializationError()

		else:
			# todo: додати сюди відомості про об’єкт в залежності від фільтрів
			# todo: додати конввертацію валют в залженост від фільтрів
			pass


	@staticmethod
	def filter(publications, conditions):
		return



class CottagesMarkersManager(BaseMarkersManager):
	def __init__(self):
		super(CottagesMarkersManager, self).__init__(OBJECTS_TYPES.cottage())


	def record_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'for_sale', 'for_rent',
			'sale_terms__price', 'sale_terms__currency_sid',

			'rent_terms__price', 'rent_terms__currency_sid', 'rent_terms__period_sid',
		    'rent_terms__persons_count', 'rent_terms__family', 'rent_terms__foreigners',

			'body__electricity', 'body__gas', 'body__sewerage', 'body__hot_water', 'body__cold_water',
			'body__market_type_sid', 'body__heating_type_sid',
			'body__rooms_count', 'body__floors_count')


	def serialize_publication_record(self, record):
		# common terms
		#-- bitmask
		bitmask = ''
		bitmask += '1' if record.for_sale else '0'
		bitmask += '1' if record.for_rent else '0'
		bitmask += '1' if record.body.electricity else '0'
		bitmask += '1' if record.body.gas else '0'
		bitmask += '1' if record.body.sewerage else '0'
		bitmask += '1' if record.body.hot_water else '0'
		bitmask += '1' if record.body.cold_water else '0'
		bitmask += '{0:01b}'.format(record.body.market_type_sid)  # 1 bit
		bitmask += '{0:02b}'.format(record.body.heating_type_sid) # 2 bits
		if len(bitmask) != 10:
			raise SerializationError('Bitmask corruption. Potential deserialization error.')


		#-- data
		data = ''
		data += str(record.id) + self.separator

		# WARNING: next fields can be None
		if record.body.rooms_count is not None:
			data += str(record.body.rooms_count) + self.separator
		else: data += self.separator

		if record.body.floors_count is not None:
			data += str(record.body.floors_count) + self.separator
		else: data += self.separator


		#-- sale terms
		if record.for_sale:
			bitmask += '{0:02b}'.format(record.sale_terms.currency_sid) # 2 bits
			if len(bitmask) != 12:
				raise SerializationError('Bitmask corruption. Potential deserialization error.')

			# REQUIRED field
			if record.sale_terms.price is not None:
				data += str(record.sale_terms.price) + self.separator
			else:
				raise SerializationError('Sale price is required.')

			# REQUIRED field
			if record.sale_terms.currency_sid is not None:
				data += str(record.sale_terms.currency_sid) + self.separator
			else:
				raise SerializationError('Sale price is required.')


		#-- rent terms
		if record.for_rent:
			bitmask += '{0:02b}'.format(record.rent_terms.period_sid)   # 2 bits
			bitmask += '{0:02b}'.format(record.rent_terms.currency_sid) # 2 bits
			bitmask += '1' if record.rent_terms.family else '0'
			bitmask += '1' if record.rent_terms.foreigners else '0'
			if len(bitmask) not in (18, 16):
				raise SerializationError('Bitmask corruption. Potential deserialization error.')

			# REQUIRED field
			if record.rent_terms.price is not  None:
				data += str(record.rent_terms.price) + self.separator
			else:
				raise SerializationError('Rent price is required.')

			# REQUIRED field
			if record.rent_terms.currency_sid is not None:
				data += str(record.rent_terms.currency_sid) + self.separator
			else:
				raise SerializationError('Rent price is required.')

			# WARNING: next fields can be None
			if record.rent_terms.persons_count is not None:
				data += str(record.rent_terms.persons_count) + self.separator
			else:
				data += self.separator


		# Інвертація бітової маски для того, щоб біти типу операції опинились справа.
		# Це пов’язано із тим, що при десериалізації старші біти, втрачаються, якщо вони нулі.
		# Доповнити маску неможливо, оскільки для доповнення слід знати точну к-сть біт маски,
		# а це залежить від того чи продаєтсья об’єкт, чи здаєтсья в оренду, чи і те і інше.
		bitmask = bitmask[::-1]

		record_data = data + self.separator +  str(int(bitmask, 2))
		if record_data[-1] == self.separator:
			record_data = record_data[:-1]
		return record_data


	def deserialize_publication_record(self, record_data):
		parts = record_data.split(self.separator)
		bitmask = bin(int(parts[-1]))[2:]
		data = {
			'id': int(parts[0]),
			'rooms_count':  int(parts[1]) if parts[1] != '' else None,
			'floors_count': int(parts[2]) if parts[2] != '' else None,

		    'electricity': (bitmask[-3] == '1'),
			'gas':         (bitmask[-4] == '1'),
			'sewerage':    (bitmask[-5] == '1'),
			'hot_water':   (bitmask[-6] == '1'),
			'cold_water':  (bitmask[-7] == '1'),

		    'market_type_sid':  int('' + bitmask[-8]),
		    'heating_type_sid': int('' + bitmask[-9] + bitmask[-10]),
		}

		if bitmask[-1] == '1':
			# sale terms
			data.update({
				'for_sale': True,
			    'sale_price': float(parts[3]),
			    'sale_currency_sid': int(parts[4]),
			})

			# check for rent terms
			if bitmask[-2] == '1':
				data.update({
					'for_rent': True,
					'rent_price': float(parts[5]),
				    'rent_currency_sid': int(parts[6]),
				    'persons_count': int(parts[7]) if parts[7] != '' else None
				})

		else:
			if bitmask[-2] == '1':
				# rent terms
				# todo: check indexes
				data.update({
					'for_rent': True,
					'rent_price': float(parts[3]),
					'rent_currency_sid': float(parts[4]),
				    'persons_count': int(parts[5]) if parts[5] != '' else None
				})
		return data


	def marker_brief(self, data, condition=None):
		if condition is None:
			# Фільтри не виставлені, віддаєм у форматі за замовчуванням
			if (data.get('for_sale', False)) and (data.get('for_rent', False)):
				return {
					'id': data['id'],
					'd0': u'Продажа: ' + self.__format_price(
						data['sale_price'],
						data['sale_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',

					'd1': u'Аренда: ' + self.__format_price(
						data['rent_price'],
						data['rent_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			elif data.get('for_sale', False):
				return {
					'id': data['id'],
					'd0': u'Комнат: ' + str(data['rooms_count']),
					'd1': self.__format_price(
						data['sale_price'],
						data['sale_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			elif data.get('for_rent', False):
				return{
					'id': data['id'],
					'd0': u'Мест: ' + str(data['persons_count']),
					'd1': self.__format_price(
						data['rent_price'],
						data['rent_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			else:
				raise DeserializationError()

		else:
			# todo: додати сюди відомості про об’єкт в залежності від фільтрів
			# todo: додати конввертацію валют в залженост від фільтрів
			pass


	@staticmethod
	def filter(publications, conditions):
		return



class DachasMarkersManager(BaseMarkersManager):
	def __init__(self):
		super(DachasMarkersManager, self).__init__(OBJECTS_TYPES.dacha())


	def record_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'for_sale', 'for_rent',
			'sale_terms__price', 'sale_terms__currency_sid',

			'rent_terms__price', 'rent_terms__currency_sid', 'rent_terms__period_sid',
			'rent_terms__persons_count', 'rent_terms__family', 'rent_terms__foreigners',

			'body__electricity', 'body__gas', 'body__sewerage', 'body__hot_water', 'body__cold_water',
			'body__market_type_sid', 'body__heating_type_sid',
			'body__rooms_count', 'body__floors_count', 'body__total_area')


	def serialize_publication_record(self, record):
		# common terms
		#-- bitmask
		bitmask = ''
		bitmask += '1' if record.for_sale else '0'
		bitmask += '1' if record.for_rent else '0'
		bitmask += '1' if record.body.electricity else '0'
		bitmask += '1' if record.body.gas else '0'
		bitmask += '1' if record.body.sewerage else '0'
		bitmask += '1' if record.body.hot_water else '0'
		bitmask += '1' if record.body.cold_water else '0'
		bitmask += '{0:01b}'.format(record.body.market_type_sid)  # 1 bit
		bitmask += '{0:02b}'.format(record.body.heating_type_sid) # 2 bits
		if len(bitmask) != 10:
			raise SerializationError('Bitmask corruption. Potential deserialization error.')


		#-- data
		data = ''
		data += str(record.id) + self.separator

		# WARNING: field can be None
		if record.body.rooms_count is not None:
			data += str(record.body.rooms_count) + self.separator
		else: data += self.separator

		# WARNING: field can be None
		if record.body.total_area is not None:
			data += str(record.body.total_area) + self.separator
		else: data += self.separator

		# WARNING: field can be None
		if record.body.floors_count is not None:
			data += str(record.body.floors_count) + self.separator
		else: data += self.separator


		#-- sale terms
		if record.for_sale:
			bitmask += '{0:02b}'.format(record.sale_terms.currency_sid) # 2 bits
			if len(bitmask) != 12:
				raise SerializationError('Bitmask corruption. Potential deserialization error.')

			# REQUIRED field
			if record.sale_terms.price is not None:
				data += str(record.sale_terms.price) + self.separator
			else:
				raise SerializationError('Sale price is required.')

			# REQUIRED field
			if record.sale_terms.currency_sid is not None:
				data += str(record.sale_terms.currency_sid) + self.separator
			else:
				raise SerializationError('Sale price is required.')


		#-- rent terms
		if record.for_rent:
			bitmask += '{0:02b}'.format(record.rent_terms.period_sid)   # 2 bits
			bitmask += '{0:02b}'.format(record.rent_terms.currency_sid) # 2 bits
			bitmask += '1' if record.rent_terms.family else '0'
			bitmask += '1' if record.rent_terms.foreigners else '0'
			if len(bitmask) not in (18, 16):
				raise SerializationError('Bitmask corruption. Potential deserialization error.')

			# REQUIRED field
			if record.rent_terms.price is not  None:
				data += str(record.rent_terms.price) + self.separator
			else:
				raise SerializationError('Rent price is required.')

			# REQUIRED field
			if record.rent_terms.currency_sid is not None:
				data += str(record.rent_terms.currency_sid) + self.separator
			else:
				raise SerializationError('Rent price is required.')

			# WARNING: next fields can be None
			if record.rent_terms.persons_count is not None:
				data += str(record.rent_terms.persons_count) + self.separator
			else:
				data += self.separator


		# Інвертація бітової маски для того, щоб біти типу операції опинились справа.
		# Це пов’язано із тим, що при десериалізації старші біти, втрачаються, якщо вони нулі.
		# Доповнити маску неможливо, оскільки для доповнення слід знати точну к-сть біт маски,
		# а це залежить від того чи продаєтсья об’єкт, чи здаєтсья в оренду, чи і те і інше.
		bitmask = bitmask[::-1]

		record_data = data + self.separator +  str(int(bitmask, 2))
		if record_data[-1] == self.separator:
			record_data = record_data[:-1]
		return record_data


	def deserialize_publication_record(self, record_data):
		parts = record_data.split(self.separator)
		bitmask = bin(int(parts[-1]))[2:]
		data = {
			'id': int(parts[0]),
			'rooms_count':  int(parts[1]) if parts[1] != '' else None,
		    'total_area':   int(parts[2]) if parts[2] != '' else None,
			'floors_count': int(parts[3]) if parts[2] != '' else None,

		    'electricity': (bitmask[-3] == '1'),
			'gas':         (bitmask[-4] == '1'),
			'sewerage':    (bitmask[-5] == '1'),
			'hot_water':   (bitmask[-6] == '1'),
			'cold_water':  (bitmask[-7] == '1'),

		    'market_type_sid':  int('' + bitmask[-8]),
		    'heating_type_sid': int('' + bitmask[-9] + bitmask[-10]),
		}

		if bitmask[-1] == '1':
			# sale terms
			data.update({
				'for_sale': True,
			    'sale_price': float(parts[4]),
			    'sale_currency_sid': int(parts[5]),
			})

			# check for rent terms
			if bitmask[-2] == '1':
				data.update({
					'for_rent': True,
					'rent_price': float(parts[6]),
				    'rent_currency_sid': int(parts[7]),
				    'persons_count': int(parts[8]) if parts[8] != '' else None
				})

		else:
			if bitmask[-2] == '1':
				# rent terms
				# todo: check indexes
				data.update({
					'for_rent': True,
					'rent_price': float(parts[4]),
					'rent_currency_sid': float(parts[5]),
				    'persons_count': int(parts[6]) if parts[6] != '' else None
				})
		return data


	def marker_brief(self, data, condition=None):
		if condition is None:
			# Фільтри не виставлені, віддаєм у форматі за замовчуванням
			if (data.get('for_sale', False)) and (data.get('for_rent', False)):
				return {
					'id': data['id'],
					'd0': u'Продажа: ' + self.__format_price(
						data['sale_price'],
						data['sale_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',

					'd1': u'Аренда: ' + self.__format_price(
						data['rent_price'],
						data['rent_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			elif data.get('for_sale', False):
				return {
					'id': data['id'],
					'd0': u'Площадь: ' + str(data['total_area']) + u' м²',
					'd1': self.__format_price(
						data['sale_price'],
						data['sale_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			elif data.get('for_rent', False):
				return{
					'id': data['id'],
					'd0': u'Площадь: ' + str(data['total_area']) + u' м²',
					'd1': self.__format_price(
						data['rent_price'],
						data['rent_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			else:
				raise DeserializationError()

		else:
			# todo: додати сюди відомості про об’єкт в залежності від фільтрів
			# todo: додати конввертацію валют в залженост від фільтрів
			pass


	@staticmethod
	def filter(publications, conditions):
		return



class RoomsMarkersManager(BaseMarkersManager):
	def __init__(self):
		super(RoomsMarkersManager, self).__init__(OBJECTS_TYPES.room())


	def record_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'for_sale', 'for_rent',
			'sale_terms__price', 'sale_terms__currency_sid',

			'rent_terms__price', 'rent_terms__currency_sid', 'rent_terms__period_sid',
		    'rent_terms__persons_count', 'rent_terms__family', 'rent_terms__foreigners',

			'body__electricity', 'body__gas', 'body__hot_water', 'body__cold_water', 'body__lift',
			'body__market_type_sid', 'body__heating_type_sid', 'body__ind_heating_type_sid',
			'body__rooms_count', 'body__total_area', 'body__floor_count')


	def serialize_publication_record(self, record):
		# common terms
		#-- bitmask
		bitmask = ''
		bitmask += '1' if record.for_sale else '0'
		bitmask += '1' if record.for_rent else '0'
		bitmask += '1' if record.body.electricity else '0'
		bitmask += '1' if record.body.gas else '0'
		bitmask += '1' if record.body.hot_water else '0'
		bitmask += '1' if record.body.cold_water else '0'
		bitmask += '1' if record.body.lift else '0'
		bitmask += '{0:01b}'.format(record.body.market_type_sid)  # 1 bit
		bitmask += '{0:02b}'.format(record.body.heating_type_sid) # 2 bits
		bitmask += '{0:02b}'.format(record.body.rooms_planning_sid) # 2 bits
		if len(bitmask) != 12:
			raise SerializationError('Bitmask corruption. Potential deserialization error.')


		#-- data
		data = ''
		data += str(record.id) + self.separator

		# WARNING: field can be None
		if record.body.rooms_count is not None:
			data += str(record.body.rooms_count) + self.separator
		else: data += self.separator

		# WARNING: field can be None
		if record.body.total_area is not None:
			data += str(record.body.total_area) + self.separator
		else: data += self.separator

		# WARNING: field can be None
		if record.body.floor is not None:
			data += str(record.body.floor) + self.separator
		else: data += self.separator


		#-- sale terms
		if record.for_sale:
			bitmask += '{0:02b}'.format(record.sale_terms.currency_sid) # 2 bits
			if len(bitmask) != 14:
				raise SerializationError('Bitmask corruption. Potential deserialization error.')

			# REQUIRED field
			if record.sale_terms.price is not None:
				data += str(record.sale_terms.price) + self.separator
				data += str(record.sale_terms.currency_sid) + self.separator
			else:
				raise SerializationError('Sale price is required.')


		#-- rent terms
		if record.for_rent:
			bitmask += '{0:02b}'.format(record.rent_terms.period_sid)   # 2 bits
			bitmask += '{0:02b}'.format(record.rent_terms.currency_sid) # 2 bits
			bitmask += '1' if record.rent_terms.family else '0'
			bitmask += '1' if record.rent_terms.foreigners else '0'
			if len(bitmask) not in (22, 20):
				raise SerializationError('Bitmask corruption. Potential deserialization error.')

			# REQUIRED field
			if record.rent_terms.price is not  None:
				data += str(record.rent_terms.price) + self.separator
			else:
				raise SerializationError('Rent price is required.')

			# REQUIRED field
			if record.rent_terms.currency_sid is not None:
				data += str(record.rent_terms.currency_sid) + self.separator
			else:
				raise SerializationError('Rent price is required.')

			# REQUIRED field
			if record.sale_terms.currency_sid is not None:
				data += str(record.sale_terms.currency_sid) + self.separator
			else:
				raise SerializationError('Sale price is required.')

			# WARNING: next fields can be None
			if record.rent_terms.persons_count is not None:
				data += str(record.rent_terms.persons_count) + self.separator
			else:
				data += self.separator


		# Інвертація бітової маски для того, щоб біти типу операції опинились справа.
		# Це пов’язано із тим, що при десериалізації старші біти, втрачаються, якщо вони нулі.
		# Доповнити маску неможливо, оскільки для доповнення слід знати точну к-сть біт маски,
		# а це залежить від того чи продаєтсья об’єкт, чи здаєтсья в оренду, чи і те і інше.
		bitmask = bitmask[::-1]

		record_data = data + self.separator +  str(int(bitmask, 2))
		if record_data[-1] == self.separator:
			record_data = record_data[:-1]
		return record_data


	def deserialize_publication_record(self, record_data):
		parts = record_data.split(self.separator)
		bitmask = bin(int(parts[-1]))[2:]
		data = {
			'id': int(parts[0]),
			'rooms_count':  int(parts[1]) if parts[1] != '' else None,
			'total_area':   float(parts[2]) if parts[2] != '' else None,
			'floor':        int(parts[3]) if parts[3] != '' else None,

		    'electricity':  (bitmask[-3] == '1'),
			'gas':          (bitmask[-4] == '1'),
			'hot_water':    (bitmask[-5] == '1'),
			'cold_water':   (bitmask[-6] == '1'),
			'lift':         (bitmask[-7] == '1'),

		    'market_type_sid':    int('' + bitmask[-8]),
		    'heating_type_sid':   int('' + bitmask[-9]  + bitmask[-10]),
		    'rooms_planning_sid': int('' + bitmask[-11] + bitmask[-12]),
		}

		if bitmask[-1] == '1':
			# sale terms
			data.update({
				'for_sale': True,
			    'sale_price': float(parts[4]),
			    'sale_currency_sid': int(parts[5]),
			})

			# check for rent terms
			if bitmask[-2] == '1':
				data.update({
					'for_rent': True,
					'rent_price': float(parts[6]),
				    'rent_currency_sid': int(parts[7]),
				    'persons_count': int(parts[8]) if parts[8] != '' else None
				})

		else:
			if bitmask[-2] == '1':
				# rent terms
				data.update({
					'for_rent': True,
					'rent_price': float(parts[4]),
					'rent_currency_sid': float(parts[5]),
				    'persons_count': int(parts[6]) if parts[6] != '' else None
				})
		return data


	def marker_brief(self, data, condition=None):
		if condition is None:
			# Фільтри не виставлені, віддаєм у форматі за замовчуванням
			if (data.get('for_sale', False)) and (data.get('for_rent', False)):
				return {
					'id': data['id'],
					'd0': u'Продажа: ' + self.__format_price(
						data['sale_price'],
						data['sale_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',

					'd1': u'Аренда: ' + self.__format_price(
						data['rent_price'],
						data['rent_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			elif data.get('for_sale', False):
				return {
					'id': data['id'],
					'd0': u'Площадь: ' + str(data['total_area']) + u' м²',
					'd1': self.__format_price(
						data['sale_price'],
						data['sale_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			elif data.get('for_rent', False):
				return{
					'id': data['id'],
					'd0': u'Мест: ' + str(data['persons_count']) + u' м²',
					'd1': self.__format_price(
						data['rent_price'],
						data['rent_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			else:
				raise DeserializationError()

		else:
			# todo: додати сюди відомості про об’єкт в залежності від фільтрів
			# todo: додати конввертацію валют в залженост від фільтрів
			pass


	@staticmethod
	def filter(publications, conditions):
		return



class TradesMarkersManager(BaseMarkersManager):
	def __init__(self):
		super(TradesMarkersManager, self).__init__(OBJECTS_TYPES.trade())


	def record_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'for_sale', 'for_rent',
			'sale_terms__price', 'sale_terms__currency_sid',

			'rent_terms__price', 'rent_terms__currency_sid', 'rent_terms__period_sid',

			'body__electricity', 'body__gas', 'body__sewerage', 'body__hot_water', 'body__cold_water',
			'body__market_type_sid',
			'body__halls_area', 'body__total_area', 'body__floor',)


	def serialize_publication_record(self, record):
		# common terms
		#-- bitmask
		bitmask = ''
		bitmask += '1' if record.for_sale else '0'
		bitmask += '1' if record.for_rent else '0'
		bitmask += '1' if record.body.electricity else '0'
		bitmask += '1' if record.body.gas else '0'
		bitmask += '1' if record.body.sewerage else '0'
		bitmask += '1' if record.body.hot_water else '0'
		bitmask += '1' if record.body.cold_water else '0'
		bitmask += '{0:01b}'.format(record.body.market_type_sid)  # 1 bit
		bitmask += '{0:03b}'.format(record.body.building_type_sid)  # 3 bits
		if len(bitmask) != 11:
			raise SerializationError('Bitmask corruption. Potential deserialization error.')


		#-- data
		data = ''
		data += str(record.id) + self.separator

		# REQUIRED
		if record.body.halls_area is not None:
			data += str(record.body.halls_area) + self.separator
		else: data += self.separator

		# WARNING: this field can be None
		if record.body.total_area is not None:
			data += str(record.body.total_area) + self.separator
		else: data += self.separator

		# WARNING: this field can be None
		if record.body.floor is not None:
			data += str(record.body.floor) + self.separator
		else: data += self.separator


		#-- sale terms
		if record.for_sale:
			bitmask += '{0:02b}'.format(record.sale_terms.currency_sid) # 2 bits
			if len(bitmask) != 13:
				raise SerializationError('Bitmask corruption. Potential deserialization error.')

			# REQUIRED field
			if record.sale_terms.price is not None:
				data += str(record.sale_terms.price) + self.separator
			else:
				raise SerializationError('Sale price is required.')

			# REQUIRED field
			if record.sale_terms.currency_sid is not None:
				data += str(record.sale_terms.currency_sid) + self.separator
			else:
				raise SerializationError('Sale price is required.')


		#-- rent terms
		if record.for_rent:
			bitmask += '{0:02b}'.format(record.rent_terms.period_sid)   # 2 bits
			bitmask += '{0:02b}'.format(record.rent_terms.currency_sid) # 2 bits
			if len(bitmask) not in (17, 19):
				raise SerializationError('Bitmask corruption. Potential deserialization error.')

			# REQUIRED field
			if record.rent_terms.price is not None:
				data += str(record.rent_terms.price) + self.separator
			else:
				raise SerializationError('Rent price is required.')

			# REQUIRED field
			if record.rent_terms.currency_sid is not None:
				data += str(record.rent_terms.currency_sid) + self.separator
			else:
				raise SerializationError('Rent price is required.')


		# Інвертація бітової маски для того, щоб біти типу операції опинились справа.
		# Це пов’язано із тим, що при десериалізації старші біти, втрачаються, якщо вони нулі.
		# Доповнити маску неможливо, оскільки для доповнення слід знати точну к-сть біт маски,
		# а це залежить від того чи продаєтсья об’єкт, чи здаєтсья в оренду, чи і те і інше.
		bitmask = bitmask[::-1]

		record_data = data + self.separator +  str(int(bitmask, 2))
		if record_data[-1] == self.separator:
			record_data = record_data[:-1]
		return record_data


	def deserialize_publication_record(self, record_data):
		parts = record_data.split(self.separator)
		bitmask = bin(int(parts[-1]))[2:]
		data = {
			'id': int(parts[0]),
			'halls_area':   int(parts[1]) if parts[1] != '' else None,
			'total_area':   int(parts[2]) if parts[2] != '' else None,
			'floor':        int(parts[3]) if parts[3] != '' else None,

		    'electricity':          (bitmask[-3] == '1'),
			'gas':                  (bitmask[-4] == '1'),
			'sewerage':             (bitmask[-5] == '1'),
			'hot_water':            (bitmask[-6] == '1'),
			'cold_water':           (bitmask[-7] == '1'),

			'market_type_sid':      int('' + bitmask[-8]  + bitmask[-9]),
			'building_type_sid':    int('' + bitmask[-10] + bitmask[-11] + bitmask[-12]),
		}

		if bitmask[-1] == '1':
			# sale terms
			data.update({
				'for_sale': True,
			    'sale_price': float(parts[5]),
			    'sale_currency_sid': int(parts[6]),
			})

			# check for rent terms
			if bitmask[-2] == '1':
				data.update({
					'for_rent': True,
					'rent_price': float(parts[7]),
				    'rent_currency_sid': int(parts[8]),
				})

		else:
			if bitmask[-2] == '1':
				# rent terms
				# todo: check indexes
				data.update({
					'for_rent': True,
					'rent_price': float(parts[5]),
					'rent_currency_sid': float(parts[6]),
				})
		return data


	def marker_brief(self, data, condition=None):
		if condition is None:
			# Фільтри не виставлені, віддаєм у форматі за замовчуванням
			if (data.get('for_sale', False)) and (data.get('for_rent', False)):
				return {
					'id': data['id'],
					'd0': u'Продажа: ' + self.__format_price(
						data['sale_price'],
						data['sale_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',

					'd1': u'Аренда: ' + self.__format_price(
						data['rent_price'],
						data['rent_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			elif data.get('for_sale', False):
				return {
					'id': data['id'],
					'd0': u'Площадь: ' + str(data['total_area']) + u' м²',
					'd1': self.__format_price(
						data['sale_price'],
						data['sale_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			elif data.get('for_rent', False):
				return{
					'id': data['id'],
					'd0': u'Площадь: ' + str(data['total_area']) + u' м²',
					'd1': self.__format_price(
						data['rent_price'],
						data['rent_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			else:
				raise DeserializationError()

		else:
			# todo: додати сюди відомості про об’єкт в залежності від фільтрів
			# todo: додати конввертацію валют в залженост від фільтрів
			pass


	@staticmethod
	def filter(publications, conditions):
		return



class OfficesMarkersManager(BaseMarkersManager):
	def __init__(self):
		super(OfficesMarkersManager, self).__init__(OBJECTS_TYPES.office())


	def record_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'for_sale', 'for_rent',
			'sale_terms__price', 'sale_terms__currency_sid',

			'rent_terms__price', 'rent_terms__currency_sid', 'rent_terms__period_sid',

			'body__security', 'body__kitchen', 'body__hot_water', 'body__cold_water',
			'body__cabinets_count', 'body__total_area')


	def serialize_publication_record(self, record):
		# common terms
		#-- bitmask
		bitmask = ''
		bitmask += '1' if record.for_sale else '0'
		bitmask += '1' if record.for_rent else '0'
		bitmask += '1' if record.body.security else '0'
		bitmask += '1' if record.body.kitchen else '0'
		bitmask += '1' if record.body.hot_water else '0'
		bitmask += '1' if record.body.cold_water else '0'
		bitmask += '{0:03b}'.format(record.body.building_type_sid)  # 3 bits
		if len(bitmask) != 8:
			raise SerializationError('Bitmask corruption. Potential deserialization error.')


		#-- data
		data = ''
		data += str(record.id) + self.separator

		# REQUIRED
		if record.body.cabinets_count is not None:
			data += str(record.body.cabinets_count) + self.separator
		else: data += self.separator

		# WARNING: this field can be None
		if record.body.total_area is not None:
			data += str(record.body.total_area) + self.separator
		else: data += self.separator


		#-- sale terms
		if record.for_sale:
			bitmask += '{0:02b}'.format(record.sale_terms.currency_sid) # 2 bits
			if len(bitmask) != 13:
				raise SerializationError('Bitmask corruption. Potential deserialization error.')

			# REQUIRED field
			if record.sale_terms.price is not None:
				data += str(record.sale_terms.price) + self.separator
			else:
				raise SerializationError('Sale price is required.')

			# REQUIRED field
			if record.sale_terms.currency_sid is not None:
				data += str(record.sale_terms.currency_sid) + self.separator
			else:
				raise SerializationError('Sale price is required.')


		#-- rent terms
		if record.for_rent:
			bitmask += '{0:02b}'.format(record.rent_terms.period_sid)   # 2 bits
			bitmask += '{0:02b}'.format(record.rent_terms.currency_sid) # 2 bits
			if len(bitmask) not in (17, 19):
				raise SerializationError('Bitmask corruption. Potential deserialization error.')

			# REQUIRED field
			if record.rent_terms.price is not None:
				data += str(record.rent_terms.price) + self.separator
			else:
				raise SerializationError('Rent price is required.')

			# REQUIRED field
			if record.rent_terms.currency_sid is not None:
				data += str(record.rent_terms.currency_sid) + self.separator
			else:
				raise SerializationError('Rent price is required.')


		# Інвертація бітової маски для того, щоб біти типу операції опинились справа.
		# Це пов’язано із тим, що при десериалізації старші біти, втрачаються, якщо вони нулі.
		# Доповнити маску неможливо, оскільки для доповнення слід знати точну к-сть біт маски,
		# а це залежить від того чи продаєтсья об’єкт, чи здаєтсья в оренду, чи і те і інше.
		bitmask = bitmask[::-1]

		record_data = data + self.separator +  str(int(bitmask, 2))
		if record_data[-1] == self.separator:
			record_data = record_data[:-1]
		return record_data


	def deserialize_publication_record(self, record_data):
		parts = record_data.split(self.separator)
		bitmask = bin(int(parts[-1]))[2:]
		data = {
			'id': int(parts[0]),
			'cabinets_count':   int(parts[1]) if parts[1] != '' else None,
			'total_area':       int(parts[2]) if parts[2] != '' else None,

			'security':     (bitmask[-3] == '1'),
			'kitchen':      (bitmask[-4] == '1'),
			'hot_water':    (bitmask[-5] == '1'),
			'cold_water':   (bitmask[-6] == '1'),

			'building_type_sid':    int('' + bitmask[-7] + bitmask[-8] + bitmask[-9]),
		}

		if bitmask[-1] == '1':
			# sale terms
			data.update({
				'for_sale': True,
			    'sale_price': float(parts[3]),
			    'sale_currency_sid': int(parts[4]),
			})

			# check for rent terms
			if bitmask[-2] == '1':
				data.update({
					'for_rent': True,
					'rent_price': float(parts[5]),
				    'rent_currency_sid': int(parts[6]),
				})

		else:
			if bitmask[-2] == '1':
				# rent terms
				# todo: check indexes
				data.update({
					'for_rent': True,
					'rent_price': float(parts[3]),
					'rent_currency_sid': float(parts[4]),
				})
		return data


	def marker_brief(self, data, condition=None):
		if condition is None:
			# Фільтри не виставлені, віддаєм у форматі за замовчуванням
			if (data.get('for_sale', False)) and (data.get('for_rent', False)):
				return {
					'id': data['id'],
					'd0': u'Продажа: ' + self.__format_price(
						data['sale_price'],
						data['sale_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',

					'd1': u'Аренда: ' + self.__format_price(
						data['rent_price'],
						data['rent_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			elif data.get('for_sale', False):
				return {
					'id': data['id'],
					'd0': u'Кабинетов: ' + str(data['cabinets_count']),
					'd1': self.__format_price(
						data['sale_price'],
						data['sale_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			elif data.get('for_rent', False):
				return{
					'id': data['id'],
					'd0': u'Кабинетов: ' + str(data['cabinets_count']),
					'd1': self.__format_price(
						data['rent_price'],
						data['rent_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			else:
				raise DeserializationError()

		else:
			# todo: додати сюди відомості про об’єкт в залежності від фільтрів
			# todo: додати конввертацію валют в залженост від фільтрів
			pass


	@staticmethod
	def filter(publications, conditions):
		return



class WarehousesMarkersManager(BaseMarkersManager):
	def __init__(self):
		super(WarehousesMarkersManager, self).__init__(OBJECTS_TYPES.warehouse())


	def record_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'for_sale', 'for_rent',
			'sale_terms__price', 'sale_terms__currency_sid',

			'rent_terms__price', 'rent_terms__currency_sid', 'rent_terms__period_sid',

			'body__electricity', 'body__gas', 'body__hot_water', 'body__cold_water',
		    'body__security_alarm', 'body__fire_alarm',
			'body__halls_area',)


	def serialize_publication_record(self, record):
		# common terms
		#-- bitmask
		bitmask = ''
		bitmask += '1' if record.for_sale else '0'
		bitmask += '1' if record.for_rent else '0'
		bitmask += '1' if record.body.electricity else '0'
		bitmask += '1' if record.body.gas else '0'
		bitmask += '1' if record.body.hot_water else '0'
		bitmask += '1' if record.body.cold_water else '0'
		bitmask += '1' if record.body.security_alarm else '0'
		bitmask += '1' if record.body.fire_alarm else '0'
		if len(bitmask) != 8:
			raise SerializationError('Bitmask corruption. Potential deserialization error.')


		#-- data
		data = ''
		data += str(record.id) + self.separator

		# REQUIRED
		if record.body.halls_area is not None:
			data += str(record.body.halls_area) + self.separator
		else: data += self.separator


		#-- sale terms
		if record.for_sale:
			bitmask += '{0:02b}'.format(record.sale_terms.currency_sid) # 2 bits
			if len(bitmask) != 13:
				raise SerializationError('Bitmask corruption. Potential deserialization error.')

			# REQUIRED field
			if record.sale_terms.price is not None:
				data += str(record.sale_terms.price) + self.separator
			else:
				raise SerializationError('Sale price is required.')

			# REQUIRED field
			if record.sale_terms.currency_sid is not None:
				data += str(record.sale_terms.currency_sid) + self.separator
			else:
				raise SerializationError('Sale price is required.')


		#-- rent terms
		if record.for_rent:
			bitmask += '{0:02b}'.format(record.rent_terms.period_sid)   # 2 bits
			bitmask += '{0:02b}'.format(record.rent_terms.currency_sid) # 2 bits
			if len(bitmask) not in (17, 19):
				raise SerializationError('Bitmask corruption. Potential deserialization error.')

			# REQUIRED field
			if record.rent_terms.price is not None:
				data += str(record.rent_terms.price) + self.separator
			else:
				raise SerializationError('Rent price is required.')

			# REQUIRED field
			if record.rent_terms.currency_sid is not None:
				data += str(record.rent_terms.currency_sid) + self.separator
			else:
				raise SerializationError('Rent price is required.')


		# Інвертація бітової маски для того, щоб біти типу операції опинились справа.
		# Це пов’язано із тим, що при десериалізації старші біти, втрачаються, якщо вони нулі.
		# Доповнити маску неможливо, оскільки для доповнення слід знати точну к-сть біт маски,
		# а це залежить від того чи продаєтсья об’єкт, чи здаєтсья в оренду, чи і те і інше.
		bitmask = bitmask[::-1]

		record_data = data + self.separator +  str(int(bitmask, 2))
		if record_data[-1] == self.separator:
			record_data = record_data[:-1]
		return record_data


	def deserialize_publication_record(self, record_data):
		parts = record_data.split(self.separator)
		bitmask = bin(int(parts[-1]))[2:]
		data = {
			'id': int(parts[0]),
			'halls_area':   int(parts[1]) if parts[1] != '' else None,

		    'electricity':      (bitmask[-3] == '1'),
			'gas':              (bitmask[-4] == '1'),
			'hot_water':        (bitmask[-5] == '1'),
			'cold_water':       (bitmask[-6] == '1'),
		    'security_alarm':   (bitmask[-5] == '1'),
			'fire_alarm':       (bitmask[-6] == '1'),
		}

		if bitmask[-1] == '1':
			# sale terms
			data.update({
				'for_sale': True,
			    'sale_price': float(parts[5]),
			    'sale_currency_sid': int(parts[6]),
			})

			# check for rent terms
			if bitmask[-2] == '1':
				data.update({
					'for_rent': True,
					'rent_price': float(parts[7]),
				    'rent_currency_sid': int(parts[8]),
				})

		else:
			if bitmask[-2] == '1':
				# rent terms
				# todo: check indexes
				data.update({
					'for_rent': True,
					'rent_price': float(parts[5]),
					'rent_currency_sid': float(parts[6]),
				})
		return data


	def marker_brief(self, data, condition=None):
		if condition is None:
			# Фільтри не виставлені, віддаєм у форматі за замовчуванням
			if (data.get('for_sale', False)) and (data.get('for_rent', False)):
				return {
					'id': data['id'],
					'd0': u'Продажа: ' + self.__format_price(
						data['sale_price'],
						data['sale_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',

					'd1': u'Аренда: ' + self.__format_price(
						data['rent_price'],
						data['rent_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			elif data.get('for_sale', False):
				return {
					'id': data['id'],
					'd0': u'Площадь: ' + str(data['halls_area']) + u' м²',
					'd1': self.__format_price(
						data['sale_price'],
						data['sale_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			elif data.get('for_rent', False):
				return{
					'id': data['id'],
					'd0': u'Площадь: ' + str(data['halls_area']) + u' м²',
					'd1': self.__format_price(
						data['rent_price'],
						data['rent_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			else:
				raise DeserializationError()

		else:
			# todo: додати сюди відомості про об’єкт в залежності від фільтрів
			# todo: додати конввертацію валют в залженост від фільтрів
			pass


	@staticmethod
	def filter(publications, conditions):
		return



class BusinessesMarkersManager(BaseMarkersManager):
	def __init__(self):
		super(BusinessesMarkersManager, self).__init__(OBJECTS_TYPES.business())


	def record_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'for_sale', 'for_rent',
			'sale_terms__price', 'sale_terms__currency_sid',

			'rent_terms__price', 'rent_terms__currency_sid', 'rent_terms__period_sid',

			'body__building_type_sid', 'body__age', 'body__total_area',)


	def serialize_publication_record(self, record):
		# common terms
		#-- bitmask
		bitmask = ''
		bitmask += '1' if record.for_sale else '0'
		bitmask += '1' if record.for_rent else '0'
		bitmask += '{0:03b}'.format(record.body.building_type_sid)  # 3 bits
		if len(bitmask) != 5:
			raise SerializationError('Bitmask corruption. Potential deserialization error.')


		#-- data
		data = ''
		data += str(record.id) + self.separator

		# WARNING: this field can be None
		if record.body.age is not None:
			data += str(record.body.age) + self.separator
		else: data += self.separator

		# WARNING: this field can be None
		if record.body.total_area is not None:
			data += str(record.body.total_area) + self.separator
		else: data += self.separator


		#-- sale terms
		if record.for_sale:
			bitmask += '{0:02b}'.format(record.sale_terms.currency_sid) # 2 bits
			if len(bitmask) != 7:
				raise SerializationError('Bitmask corruption. Potential deserialization error.')

			# REQUIRED field
			if record.sale_terms.price is not None:
				data += str(record.sale_terms.price) + self.separator
			else:
				raise SerializationError('Sale price is required.')

			# REQUIRED field
			if record.sale_terms.currency_sid is not None:
				data += str(record.sale_terms.currency_sid) + self.separator
			else:
				raise SerializationError('Sale price is required.')


		#-- rent terms
		if record.for_rent:
			bitmask += '{0:02b}'.format(record.rent_terms.period_sid)   # 2 bits
			bitmask += '{0:02b}'.format(record.rent_terms.currency_sid) # 2 bits
			if len(bitmask) not in (9, 11):
				raise SerializationError('Bitmask corruption. Potential deserialization error.')

			# REQUIRED field
			if record.rent_terms.price is not None:
				data += str(record.rent_terms.price) + self.separator
			else:
				raise SerializationError('Rent price is required.')

			# REQUIRED field
			if record.rent_terms.currency_sid is not None:
				data += str(record.rent_terms.currency_sid) + self.separator
			else:
				raise SerializationError('Rent price is required.')


		# Інвертація бітової маски для того, щоб біти типу операції опинились справа.
		# Це пов’язано із тим, що при десериалізації старші біти, втрачаються, якщо вони нулі.
		# Доповнити маску неможливо, оскільки для доповнення слід знати точну к-сть біт маски,
		# а це залежить від того чи продаєтсья об’єкт, чи здаєтсья в оренду, чи і те і інше.
		bitmask = bitmask[::-1]

		record_data = data + self.separator +  str(int(bitmask, 2))
		if record_data[-1] == self.separator:
			record_data = record_data[:-1]
		return record_data


	def deserialize_publication_record(self, record_data):
		parts = record_data.split(self.separator)
		bitmask = bin(int(parts[-1]))[2:]
		data = {
			'id': int(parts[0]),
			'halls_area': int(parts[1]) if parts[1] != '' else None,
			'total_area': int(parts[2]) if parts[2] != '' else None,

			'building_type_sid': int('' + bitmask[-3] + bitmask[-4] + bitmask[-5]),
		}

		if bitmask[-1] == '1':
			# sale terms
			data.update({
				'for_sale': True,
			    'sale_price': float(parts[3]),
			    'sale_currency_sid': int(parts[4]),
			})

			# check for rent terms
			if bitmask[-2] == '1':
				data.update({
					'for_rent': True,
					'rent_price': float(parts[4]),
				    'rent_currency_sid': int(parts[5]),
				})

		else:
			if bitmask[-2] == '1':
				# rent terms
				# todo: check indexes
				data.update({
					'for_rent': True,
					'rent_price': float(parts[3]),
					'rent_currency_sid': float(parts[4]),
				})
		return data


	def marker_brief(self, data, condition=None):
		if condition is None:
			# Фільтри не виставлені, віддаєм у форматі за замовчуванням
			if (data.get('for_sale', False)) and (data.get('for_rent', False)):
				return {
					'id': data['id'],
					'd0': u'Продажа: ' + self.__format_price(
						data['sale_price'],
						data['sale_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',

					'd1': u'Аренда: ' + self.__format_price(
						data['rent_price'],
						data['rent_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			elif data.get('for_sale', False):
				return {
					'id': data['id'],
					'd0': self.__format_price(
						data['sale_price'],
						data['sale_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				    'd1': u''
				}

			elif data.get('for_rent', False):
				return{
					'id': data['id'],
					'd0': self.__format_price(
						data['rent_price'],
						data['rent_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				    'd1': u''
				}

			else:
				raise DeserializationError()

		else:
			# todo: додати сюди відомості про об’єкт в залежності від фільтрів
			# todo: додати конввертацію валют в залженост від фільтрів
			pass


	@staticmethod
	def filter(publications, conditions):
		return



class CateringsMarkersManager(BaseMarkersManager):
	def __init__(self):
		super(CateringsMarkersManager, self).__init__(OBJECTS_TYPES.catering())


	def record_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'for_sale', 'for_rent',
			'sale_terms__price', 'sale_terms__currency_sid',

			'rent_terms__price', 'rent_terms__currency_sid', 'rent_terms__period_sid',

			'body__electricity', 'body__gas', 'body__hot_water', 'body__cold_water',
			'body__building_type_sid', 'body__halls_area', 'body__total_area',)


	def serialize_publication_record(self, record):
		# common terms
		#-- bitmask
		bitmask = ''
		bitmask += '1' if record.for_sale else '0'
		bitmask += '1' if record.for_rent else '0'
		bitmask += '1' if record.body.electricity else '0'
		bitmask += '1' if record.body.gas else '0'
		bitmask += '1' if record.body.hot_water else '0'
		bitmask += '1' if record.body.cold_water else '0'
		bitmask += '{0:03b}'.format(record.body.building_type_sid)  # 3 bits
		if len(bitmask) != 9:
			raise SerializationError('Bitmask corruption. Potential deserialization error.')


		#-- data
		data = ''
		data += str(record.id) + self.separator

		# REQUIRED
		if record.body.halls_count is not None:
			data += str(record.body.halls_count) + self.separator
		else: data += self.separator

		# REQUIRED
		if record.body.halls_area is not None:
			data += str(record.body.halls_area) + self.separator
		else: data += self.separator

		# WARNING: this field can be None
		if record.body.total_area is not None:
			data += str(record.body.total_area) + self.separator
		else: data += self.separator


		#-- sale terms
		if record.for_sale:
			bitmask += '{0:02b}'.format(record.sale_terms.currency_sid) # 2 bits
			if len(bitmask) != 11:
				raise SerializationError('Bitmask corruption. Potential deserialization error.')

			# REQUIRED field
			if record.sale_terms.price is not None:
				data += str(record.sale_terms.price) + self.separator
			else:
				raise SerializationError('Sale price is required.')

			# REQUIRED field
			if record.sale_terms.currency_sid is not None:
				data += str(record.sale_terms.currency_sid) + self.separator
			else:
				raise SerializationError('Sale price is required.')


		#-- rent terms
		if record.for_rent:
			bitmask += '{0:02b}'.format(record.rent_terms.period_sid)   # 2 bits
			bitmask += '{0:02b}'.format(record.rent_terms.currency_sid) # 2 bits
			if len(bitmask) not in (13, 15):
				raise SerializationError('Bitmask corruption. Potential deserialization error.')

			# REQUIRED field
			if record.rent_terms.price is not None:
				data += str(record.rent_terms.price) + self.separator
			else:
				raise SerializationError('Rent price is required.')

			# REQUIRED field
			if record.rent_terms.currency_sid is not None:
				data += str(record.rent_terms.currency_sid) + self.separator
			else:
				raise SerializationError('Rent price is required.')


		# Інвертація бітової маски для того, щоб біти типу операції опинились справа.
		# Це пов’язано із тим, що при десериалізації старші біти, втрачаються, якщо вони нулі.
		# Доповнити маску неможливо, оскільки для доповнення слід знати точну к-сть біт маски,
		# а це залежить від того чи продаєтсья об’єкт, чи здаєтсья в оренду, чи і те і інше.
		bitmask = bitmask[::-1]

		record_data = data + self.separator +  str(int(bitmask, 2))
		if record_data[-1] == self.separator:
			record_data = record_data[:-1]
		return record_data


	def deserialize_publication_record(self, record_data):
		parts = record_data.split(self.separator)
		bitmask = bin(int(parts[-1]))[2:]
		data = {
			'id': int(parts[0]),
		    'halls_count': int(parts[1]), # required
			'halls_area':  int(parts[2]), # required
			'total_area':  int(parts[3]) if parts[3] != '' else None,

		    'electricity': (bitmask[-3] == '1'),
			'gas':         (bitmask[-4] == '1'),
			'hot_water':   (bitmask[-5] == '1'),
			'cold_water':  (bitmask[-6] == '1'),

			'building_type_sid': int('' + bitmask[-7] + bitmask[-8] + bitmask[-9]),
		}

		if bitmask[-1] == '1':
			# sale terms
			data.update({
				'for_sale': True,
			    'sale_price': float(parts[5]),
			    'sale_currency_sid': int(parts[6]),
			})

			# check for rent terms
			if bitmask[-2] == '1':
				data.update({
					'for_rent': True,
					'rent_price': float(parts[7]),
				    'rent_currency_sid': int(parts[8]),
				})

		else:
			if bitmask[-2] == '1':
				# rent terms
				# todo: check indexes
				data.update({
					'for_rent': True,
					'rent_price': float(parts[5]),
					'rent_currency_sid': float(parts[6]),
				})
		return data


	def marker_brief(self, data, condition=None):
		if condition is None:
			# Фільтри не виставлені, віддаєм у форматі за замовчуванням
			if (data.get('for_sale', False)) and (data.get('for_rent', False)):
				return {
					'id': data['id'],
					'd0': u'Продажа: ' + self.__format_price(
						data['sale_price'],
						data['sale_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',

					'd1': u'Аренда: ' + self.__format_price(
						data['rent_price'],
						data['rent_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			elif data.get('for_sale', False):
				return {
					'id': data['id'],
					'd0': u'Пл. залов: ' + str(data['halls_area']) + u' м²',
					'd1': self.__format_price(
						data['sale_price'],
						data['sale_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			elif data.get('for_rent', False):
				return{
					'id': data['id'],
					'd0': u'Пл. залов: ' + str(data['halls_area']) + u' м²',
					'd1': self.__format_price(
						data['rent_price'],
						data['rent_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			else:
				raise DeserializationError()

		else:
			# todo: додати сюди відомості про об’єкт в залежності від фільтрів
			# todo: додати конввертацію валют в залженост від фільтрів
			pass


	@staticmethod
	def filter(publications, conditions):
		return



class GaragesMarkersManager(BaseMarkersManager):
	def __init__(self):
		super(GaragesMarkersManager, self).__init__(OBJECTS_TYPES.garage())


	def record_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'for_sale', 'for_rent',
			'sale_terms__price', 'sale_terms__currency_sid',

			'rent_terms__price', 'rent_terms__currency_sid', 'rent_terms__period_sid',

			'body__pit', 'body__total_area', 'body__ceiling_height',)


	def serialize_publication_record(self, record):
		# common terms
		#-- bitmask
		bitmask = ''
		bitmask += '1' if record.for_sale else '0'
		bitmask += '1' if record.for_rent else '0'
		bitmask += '1' if record.body.pit else '0'
		if len(bitmask) != 3:
			raise SerializationError('Bitmask corruption. Potential deserialization error.')


		#-- data
		data = ''
		data += str(record.id) + self.separator

		# REQUIRED
		if record.body.total_area is not None:
			data += str(record.body.total_area) + self.separator
		else: data += self.separator

		# WARNING: field can be None
		if record.body.ceiling_height is not None:
			data += str(record.body.ceiling_height) + self.separator
		else: data += self.separator


		#-- sale terms
		if record.for_sale:
			bitmask += '{0:02b}'.format(record.sale_terms.currency_sid) # 2 bits
			if len(bitmask) != 11:
				raise SerializationError('Bitmask corruption. Potential deserialization error.')

			# REQUIRED field
			if record.sale_terms.price is not None:
				data += str(record.sale_terms.price) + self.separator
			else:
				raise SerializationError('Sale price is required.')

			# REQUIRED field
			if record.sale_terms.currency_sid is not None:
				data += str(record.sale_terms.currency_sid) + self.separator
			else:
				raise SerializationError('Sale price is required.')


		#-- rent terms
		if record.for_rent:
			bitmask += '{0:02b}'.format(record.rent_terms.period_sid)   # 2 bits
			bitmask += '{0:02b}'.format(record.rent_terms.currency_sid) # 2 bits
			if len(bitmask) not in (13, 15):
				raise SerializationError('Bitmask corruption. Potential deserialization error.')

			# REQUIRED field
			if record.rent_terms.price is not None:
				data += str(record.rent_terms.price) + self.separator
			else:
				raise SerializationError('Rent price is required.')

			# REQUIRED field
			if record.rent_terms.currency_sid is not None:
				data += str(record.rent_terms.currency_sid) + self.separator
			else:
				raise SerializationError('Rent price is required.')


		# Інвертація бітової маски для того, щоб біти типу операції опинились справа.
		# Це пов’язано із тим, що при десериалізації старші біти, втрачаються, якщо вони нулі.
		# Доповнити маску неможливо, оскільки для доповнення слід знати точну к-сть біт маски,
		# а це залежить від того чи продаєтсья об’єкт, чи здаєтсья в оренду, чи і те і інше.
		bitmask = bitmask[::-1]

		record_data = data + self.separator +  str(int(bitmask, 2))
		if record_data[-1] == self.separator:
			record_data = record_data[:-1]
		return record_data


	def deserialize_publication_record(self, record_data):
		parts = record_data.split(self.separator)
		bitmask = bin(int(parts[-1]))[2:]
		data = {
			'id': int(parts[0]),
		    'total_area':       int(parts[1]), # required
			'ceiling_height':   int(parts[2]) if parts[2] != '' else None,

		    'pit':  (bitmask[-3] == '1'),
		}

		if bitmask[-1] == '1':
			# sale terms
			data.update({
				'for_sale': True,
			    'sale_price': float(parts[3]),
			    'sale_currency_sid': int(parts[4]),
			})

			# check for rent terms
			if bitmask[-2] == '1':
				data.update({
					'for_rent': True,
					'rent_price': float(parts[5]),
				    'rent_currency_sid': int(parts[6]),
				})

		else:
			if bitmask[-2] == '1':
				# rent terms
				# todo: check indexes
				data.update({
					'for_rent': True,
					'rent_price': float(parts[3]),
					'rent_currency_sid': float(parts[4]),
				})
		return data


	def marker_brief(self, data, condition=None):
		if condition is None:
			# Фільтри не виставлені, віддаєм у форматі за замовчуванням
			if (data.get('for_sale', False)) and (data.get('for_rent', False)):
				return {
					'id': data['id'],
					'd0': u'Продажа: ' + self.__format_price(
						data['sale_price'],
						data['sale_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',

					'd1': u'Аренда: ' + self.__format_price(
						data['rent_price'],
						data['rent_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			elif data.get('for_sale', False):
				return {
					'id': data['id'],
					'd0': u'Площадь: ' + str(data['total_area']) + u' м²',
					'd1': self.__format_price(
						data['sale_price'],
						data['sale_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			elif data.get('for_rent', False):
				return{
					'id': data['id'],
					'd0': u'Площадь: ' + str(data['total_area']) + u' м²',
					'd1': self.__format_price(
						data['rent_price'],
						data['rent_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			else:
				raise DeserializationError()

		else:
			# todo: додати сюди відомості про об’єкт в залежності від фільтрів
			# todo: додати конввертацію валют в залженост від фільтрів
			pass


	@staticmethod
	def filter(publications, conditions):
		return



class LandsMarkersManager(BaseMarkersManager):
	def __init__(self):
		super(LandsMarkersManager, self).__init__(OBJECTS_TYPES.land())


	def record_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'for_sale', 'for_rent',
			'sale_terms__price', 'sale_terms__currency_sid',

			'rent_terms__price', 'rent_terms__currency_sid', 'rent_terms__period_sid',

			'body__electricity', 'body__gas', 'body__sewerage', 'body__water',
			'body__area')


	def serialize_publication_record(self, record):
		# common terms
		#-- bitmask
		bitmask = ''
		bitmask += '1' if record.for_sale else '0'
		bitmask += '1' if record.for_rent else '0'
		bitmask += '1' if record.body.electricity else '0'
		bitmask += '1' if record.body.gas else '0'
		bitmask += '1' if record.body.sewerage else '0'
		bitmask += '1' if record.body.water else '0'
		if len(bitmask) != 6:
			raise SerializationError('Bitmask corruption. Potential deserialization error.')


		#-- data
		data = ''
		data += str(record.id) + self.separator

		# WARNING: next fields can be None
		if record.body.area is not None:
			data += str(record.body.area) + self.separator
		else: data += self.separator


		#-- sale terms
		if record.for_sale:
			bitmask += '{0:02b}'.format(record.sale_terms.currency_sid) # 2 bits
			if len(bitmask) != 8:
				raise SerializationError('Bitmask corruption. Potential deserialization error.')

			# REQUIRED field
			if record.sale_terms.price is not None:
				data += str(record.sale_terms.price) + self.separator
			else:
				raise SerializationError('Sale price is required.')

			# REQUIRED field
			if record.sale_terms.currency_sid is not None:
				data += str(record.sale_terms.currency_sid) + self.separator
			else:
				raise SerializationError('Sale price is required.')


		#-- rent terms
		if record.for_rent:
			bitmask += '{0:02b}'.format(record.rent_terms.period_sid)   # 2 bits
			bitmask += '{0:02b}'.format(record.rent_terms.currency_sid) # 2 bits
			if len(bitmask) not in (12, 10):
				raise SerializationError('Bitmask corruption. Potential deserialization error.')

			# REQUIRED field
			if record.rent_terms.price is not  None:
				data += str(record.rent_terms.price) + self.separator
			else:
				raise SerializationError('Rent price is required.')

			# REQUIRED field
			if record.rent_terms.currency_sid is not None:
				data += str(record.rent_terms.currency_sid) + self.separator
			else:
				raise SerializationError('Rent price is required.')

			# WARNING: next fields can be None
			if record.rent_terms.persons_count is not None:
				data += str(record.rent_terms.persons_count) + self.separator
			else:
				data += self.separator


		# Інвертація бітової маски для того, щоб біти типу операції опинились справа.
		# Це пов’язано із тим, що при десериалізації старші біти, втрачаються, якщо вони нулі.
		# Доповнити маску неможливо, оскільки для доповнення слід знати точну к-сть біт маски,
		# а це залежить від того чи продаєтсья об’єкт, чи здаєтсья в оренду, чи і те і інше.
		bitmask = bitmask[::-1]

		record_data = data + self.separator +  str(int(bitmask, 2))
		if record_data[-1] == self.separator:
			record_data = record_data[:-1]
		return record_data


	def deserialize_publication_record(self, record_data):
		parts = record_data.split(self.separator)
		bitmask = bin(int(parts[-1]))[2:]
		data = {
			'id': int(parts[0]),
			'area':  int(parts[1]) if parts[1] != '' else None,

		    'electricity':  (bitmask[-3] == '1'),
			'gas':          (bitmask[-4] == '1'),
			'sewerage':     (bitmask[-5] == '1'),
			'water':        (bitmask[-6] == '1'),
		}

		if bitmask[-1] == '1':
			# sale terms
			data.update({
				'for_sale': True,
			    'sale_price': float(parts[3]),
			    'sale_currency_sid': int(parts[4]),
			})

			# check for rent terms
			if bitmask[-2] == '1':
				data.update({
					'for_rent': True,
					'rent_price': float(parts[5]),
				    'rent_currency_sid': int(parts[6])
				})

		else:
			if bitmask[-2] == '1':
				# rent terms
				# todo: check indexes
				data.update({
					'for_rent': True,
					'rent_price': float(parts[3]),
					'rent_currency_sid': float(parts[4])
				})
		return data


	def marker_brief(self, data, condition=None):
		if condition is None:
			# Фільтри не виставлені, віддаєм у форматі за замовчуванням
			if (data.get('for_sale', False)) and (data.get('for_rent', False)):
				return {
					'id': data['id'],
					'd0': u'Продажа: ' + self.__format_price(
						data['sale_price'],
						data['sale_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',

					'd1': u'Аренда: ' + self.__format_price(
						data['rent_price'],
						data['rent_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			elif data.get('for_sale', False):
				return {
					'id': data['id'],
					'd0': u'Площадь: ' + str(data['area'])  + u' м²',
					'd1': self.__format_price(
						data['sale_price'],
						data['sale_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			elif data.get('for_rent', False):
				return{
					'id': data['id'],
					'd0': u'Площадь: ' + str(data['area'])  + u' м²',
					'd1': self.__format_price(
						data['rent_price'],
						data['rent_currency_sid'],
						CURRENCIES.uah()
					) + u' грн.',
				}

			else:
				raise DeserializationError()

		else:
			# todo: додати сюди відомості про об’єкт в залежності від фільтрів
			# todo: додати конввертацію валют в залженост від фільтрів
			pass


	@staticmethod
	def filter(publications, conditions):
		return