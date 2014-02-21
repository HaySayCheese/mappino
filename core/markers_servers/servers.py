#coding=utf-8
import copy

import abc
from django.core.exceptions import SuspiciousOperation

from core.markers_servers.exceptions import TooBigTransaction, SerializationError, DeserializationError
from core.markers_servers.utils import DegreeSegmentPoint, Point, SegmentPoint, DegreePoint
from core.publications.constants import OBJECTS_TYPES, HEAD_MODELS
from mappino.wsgi import redis_connections



class BaseMarkersServer(object):
	__metaclass__ = abc.ABCMeta


	def __init__(self, tid):
		if tid not in OBJECTS_TYPES.values():
			raise ValueError('invalid @tid.')
		self.tid = tid
		self.model = HEAD_MODELS[tid]
		self.redis = redis_connections['steady']
		self.separator = ';'
		self.digest_separator = ':'


	def markers(self, ne, sw, condition):
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


		segments_digests = []
		current = copy.deepcopy(start)
		while True:
			current.degree.lng = start.degree.lng
			current.segment.lng = start.segment.lng

			while True:
				segments_digests.append(self.__segment_digest(current.degree, current.segment))

				# Заборонити одночасну вибірку маркерів з великої к-сті сегментів.
				# Таким чином можна уберегтись від занадто великих транзакцій і накопичування
				# великої к-сті запитів від інших користувачів в черзі на обробку.
				if len(segments_digests) > 5*5:
					raise TooBigTransaction()

				if (current.degree.lng == stop.degree.lng) and (current.segment.lng == stop.segment.lng):
					break
				current.inc_segment_lng()

			if (current.degree.lat == stop.degree.lat) and (current.segment.lat == stop.segment.lat):
				break
			current.dec_segment_lat()


		data = {}
		for digest in segments_digests:
			degree = self.__degree_from_digest(digest)

			coordinates = self.redis.hkeys(digest)
			pipe = self.redis.pipeline()
			for c in coordinates:
				pipe.hget(digest, c)

			markers = pipe.execute()
			if markers:
				data[degree] = {}

			for record in zip(coordinates, markers):
				coordinates = record[0]
				item = record[1]

				data[degree][coordinates] = self.deserialize_publication_record(item, brief=True)
		return data



	def add_publication(self, hid):
		record = self.record_queryset(hid).only(
			'degree_lng', 'degree_lat', 'segment_lng', 'segment_lat', 'pos_lng', 'pos_lat')[0]

		degree = DegreePoint(record.degree_lat, record.degree_lng)
		segment = SegmentPoint(record.segment_lat, record.segment_lng)
		seg_digest = self.__segment_digest(degree, segment)

		sector = Point(record.segment_lat, record.segment_lng)
		position = Point(record.pos_lat, record.pos_lng)
		pos_digest = self.__position_digest(sector, position)

		data = self.serialize_publication_record(record)
		self.redis.hset(seg_digest, pos_digest, data)


	def __segment_digest(self, degree, segment):
		return  str(self.tid) + self.digest_separator + \
		        str(degree.lat) + self.digest_separator + \
		        str(degree.lng) + self.digest_separator + \
		        str(segment.lat) + self.digest_separator + \
		        str(segment.lng)


	def __degree_from_digest(self, digest):
		index = digest.find(self.digest_separator)
		if index == -1:
			raise DeserializationError()

		coordinates = digest[index+1:].split(self.digest_separator)
		return coordinates[0] + ';' + coordinates[1]


	def __position_digest(self, segment, position):
		return  str(segment.lat) + str(position.lat) + self.digest_separator + \
		        str(segment.lng) + str(position.lng)


	@abc.abstractmethod
	def serialize_publication_record(self, record):
		return


	@abc.abstractmethod
	def deserialize_publication_record(self, record, brief=False):
		return


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


	@staticmethod
	@abc.abstractmethod
	def format(publications):
		return



class FlatsMarkersServer(BaseMarkersServer):
	def __init__(self):
		super(FlatsMarkersServer, self).__init__(OBJECTS_TYPES.flat())


	def serialize_publication_record(self, record):
		return ''


	def deserialize_publication_record(self, record, brief=True):
		return ''


	def record_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'for_sale', 'for_rent', 'sale_terms__price', 'rent_terms__price')


	@staticmethod
	def filter(publications, conditions):
		return


	@staticmethod
	def format(publications):
		return



class ApartmentsMarkersServer(BaseMarkersServer):
	def __init__(self):
		super(ApartmentsMarkersServer, self).__init__(OBJECTS_TYPES.apartments())


	def serialize_publication_record(self, record):
		return ''


	def deserialize_publication_record(self, record, brief=True):
		return ''


	def record_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'for_sale', 'for_rent', 'sale_terms__price', 'rent_terms__price')


	@staticmethod
	def filter(publications, conditions):
		return


	@staticmethod
	def format(publications):
		return



class HousesMarkersServer(BaseMarkersServer):
	def __init__(self):
		super(HousesMarkersServer, self).__init__(OBJECTS_TYPES.house())


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
		bitmask += bin(record.body.market_type_sid)[2:] # 1 bit
		bitmask += bin(record.body.heating_type_sid)[2:] # 2 bits
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
			bitmask += bin(record.sale_terms.currency_sid)[2:] # 2 bits
			if len(bitmask) != 12:
				raise SerializationError('Bitmask corruption. Potential deserialization error.')

			# REQUIRED field
			if record.sale_terms.price is not None:
				data += str(record.sale_terms.price) + self.separator
			else:
				raise SerializationError('Sale price is required.')


		#-- rent terms
		if record.for_rent:
			bitmask += bin(record.rent_terms.period_sid)[2:] # 2 bits
			bitmask += bin(record.rent_terms.currency_sid)[2:] # 2 bits
			bitmask += '1' if record.rent_terms.family else '0'
			bitmask += '1' if record.rent_terms.foreigners else '0'
			if len(bitmask) not in (18, 16):
				raise SerializationError('Bitmask corruption. Potential deserialization error.')

			# REQUIRED field
			if record.rent_terms.price is not  None:
				data += str(record.rent_terms.price) + self.separator
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


	def deserialize_publication_record(self, record_data, brief=False):
		parts = record_data.split(self.separator)
		if brief:
			# Подати коротку форму для передачі разом із маркером на клієнт.
			return {
				'id': int(parts[0]),
			    # todo: додати сюди відомості про об’єкт в залежності від фільтрів
			}

		bitmask = bin(int(parts[-1]))[:2]
		data = {
			'id': int(parts[0]),
			'rooms_count':  int(parts[1]) if parts[1] != '' else None,
			'floors_count': int(parts[2]) if parts[2] != '' else None,

		    'electricity': (bitmask[-3] == '1'),
			'gas':         (bitmask[-4] == '1'),
			'sewerage':    (bitmask[-5] == '1'),
			'hot_water':   (bitmask[-6] == '1'),
			'cold_water':  (bitmask[-7] == '1'),
		}

		if bitmask[-1] == '1':
			# sale terms
			data.update({
				'for_sale': True,
			    'sale_price': float(parts[3]),
			})

			# check for rent terms
			if bitmask[-2] == '1':
				data.update({
					'for_rent': True,
					'rent_price': float(parts[4]),
				    'persons_count': int(parts[5]) if parts[5] != '' else None
				})

		else:
			if bitmask[-2] == '1':
				# rent terms
				data.update({
					'for_rent': True,
					'rent_price': float(parts[4]),
				    'persons_count': int(parts[5]) if parts[5] != '' else None
				})
		return data



	def record_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'for_sale', 'for_rent', 'sale_terms__price', 'rent_terms__price')


	@staticmethod
	def filter(publications, conditions):
		return


	@staticmethod
	def format(publications):
		return



class CottagesMarkersServer(BaseMarkersServer):
	def __init__(self):
		super(CottagesMarkersServer, self).__init__(OBJECTS_TYPES.cottage())


	def serialize_publication_record(self, record):
		"""
		format: int - hid,
				separator,
				bitmask:
					0 | 1 - record is for sale
					0 | 1 - record is for rent
		"""

		bitmask =  '1' if record.for_sale else '0'
		bitmask += '1' if record.for_rent else '0'

		data = str(record.id) + self.separator + \
		       str(int(bitmask, 2)) + self.separator

		if record.for_sale:
			if record.sale_terms.price is None:
				raise SuspiciousOperation('Attempt to publish record with empty sale-price.')
			data += str(record.sale_terms.price)

		if record.for_rent:
			if record.rent_terms.price is None:
				raise SuspiciousOperation('Attempt to publish record with empty rent-price.')
			data += str(record.rent_terms.price)
		return data


	def deserialize_publication_record(self, record, brief=True):
		return ''

	def record_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'for_sale', 'for_rent', 'sale_terms__price', 'rent_terms__price')


	@staticmethod
	def filter(publications, conditions):
		return


	@staticmethod
	def format(publications):
		return



class DachasMarkersServer(BaseMarkersServer):
	def __init__(self):
		super(DachasMarkersServer, self).__init__(OBJECTS_TYPES.dacha())


	def serialize_publication_record(self, record):
		return ''


	def deserialize_publication_record(self, record, brief=True):
		return ''


	def record_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'for_sale', 'for_rent', 'sale_terms__price', 'rent_terms__price')


	@staticmethod
	def filter(publications, conditions):
		return


	@staticmethod
	def format(publications):
		return



class RoomsMarkersServer(BaseMarkersServer):
	def __init__(self):
		super(RoomsMarkersServer, self).__init__(OBJECTS_TYPES.room())


	def serialize_publication_record(self, record):
		return ''


	def deserialize_publication_record(self, record, brief=True):
		return ''


	def record_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'for_sale', 'for_rent', 'sale_terms__price', 'rent_terms__price')


	@staticmethod
	def filter(publications, conditions):
		return


	@staticmethod
	def format(publications):
		return



class TradesMarkersServer(BaseMarkersServer):
	def __init__(self):
		super(TradesMarkersServer, self).__init__(OBJECTS_TYPES.trade())


	def serialize_publication_record(self, record):
		return ''


	def deserialize_publication_record(self, record, brief=True):
		return ''


	def record_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'for_sale', 'for_rent', 'sale_terms__price', 'rent_terms__price')


	@staticmethod
	def filter(publications, conditions):
		return


	@staticmethod
	def format(publications):
		return



class OfficesMarkersServer(BaseMarkersServer):
	def __init__(self):
		super(OfficesMarkersServer, self).__init__(OBJECTS_TYPES.office())


	def serialize_publication_record(self, record):
		return ''


	def deserialize_publication_record(self, record, brief=True):
		return ''


	def record_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'for_sale', 'for_rent', 'sale_terms__price', 'rent_terms__price')


	@staticmethod
	def filter(publications, conditions):
		return


	@staticmethod
	def format(publications):
		return



class WarehousesMarkersServer(BaseMarkersServer):
	def __init__(self):
		super(WarehousesMarkersServer, self).__init__(OBJECTS_TYPES.warehouse())


	def serialize_publication_record(self, record):
		return ''


	def deserialize_publication_record(self, record, brief=True):
		return ''


	def record_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'for_sale', 'for_rent', 'sale_terms__price', 'rent_terms__price')


	@staticmethod
	def filter(publications, conditions):
		return


	@staticmethod
	def format(publications):
		return



class BusinessesMarkersServer(BaseMarkersServer):
	def __init__(self):
		super(BusinessesMarkersServer, self).__init__(OBJECTS_TYPES.business())


	def serialize_publication_record(self, record):
		return ''


	def deserialize_publication_record(self, record, brief=True):
		return ''


	def record_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'for_sale', 'for_rent', 'sale_terms__price', 'rent_terms__price')


	@staticmethod
	def filter(publications, conditions):
		return


	@staticmethod
	def format(publications):
		return



class CateringsMarkersServer(BaseMarkersServer):
	def __init__(self):
		super(CateringsMarkersServer, self).__init__(OBJECTS_TYPES.catering())


	def serialize_publication_record(self, record):
		return ''


	def deserialize_publication_record(self, record, brief=True):
		return ''


	def record_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'for_sale', 'for_rent', 'sale_terms__price', 'rent_terms__price')


	@staticmethod
	def filter(publications, conditions):
		return


	@staticmethod
	def format(publications):
		return



class GaragesMarkersServer(BaseMarkersServer):
	def __init__(self):
		super(GaragesMarkersServer, self).__init__(OBJECTS_TYPES.garage())


	def serialize_publication_record(self, record):
		return ''


	def deserialize_publication_record(self, record, brief=True):
		return ''


	def record_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'for_sale', 'for_rent', 'sale_terms__price', 'rent_terms__price')


	@staticmethod
	def filter(publications, conditions):
		return


	@staticmethod
	def format(publications):
		return



class LandsMarkersServer(BaseMarkersServer):
	def __init__(self):
		super(LandsMarkersServer, self).__init__(OBJECTS_TYPES.land())


	def serialize_publication_record(self, record):
		return ''


	def deserialize_publication_record(self, record, brief=True):
		return ''


	def record_queryset(self, hid):
		return self.model.objects.filter(id=hid).only(
			'for_sale', 'for_rent', 'sale_terms__price', 'rent_terms__price')


	@staticmethod
	def filter(publications, conditions):
		return


	@staticmethod
	def format(publications):
		return