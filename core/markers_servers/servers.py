#coding=utf-8
import abc
from django.core.exceptions import SuspiciousOperation

from core.markers_servers.exceptions import TooBigTransaction, SerializationError, DeserializationError
from core.markers_servers.utils import DegreeSegmentPoint, Point, SegmentPoint, DegreePoint
from core.publications.constants import OBJECTS_TYPES, HEAD_MODELS, MARKET_TYPES, CURRENCIES, HEATING_TYPES, \
	LIVING_RENT_PERIODS
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
		current = DegreeSegmentPoint(ne.lat, ne.lng)
		stop = DegreeSegmentPoint(sw.lat, sw.lng)

		if current.degree.lng > stop.degree.lng:
			current.degree.lng, stop.degree.lng = stop.degree.lng, current.degree.lng
		elif current.segment.lng > stop.segment.lng:
			current.segment.lng, stop.segment.lng = stop.segment.lng, current.segment.lng

		if current.degree.lat < stop.degree.lat:
			current.degree.lat, stop.degree.lat = stop.degree.lat, current.degree.lat
		elif current.segment.lat < stop.segment.lat:
			current.segment.lat, stop.segment.lat = stop.segment.lat, current.segment.lat


		digests = []
		while True:
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


		results = {}
		for digest in digests:
			records_ids = self.redis.hkeys(digest)

			pipe = self.redis.pipeline()
			for rid in records_ids:
				pipe.hget(digest, rid)

			degrees = self.__degrees_from_digest(digest)
			records = pipe.execute()
			if records:
				results[degrees] = {}

			for record in zip(records_ids, records):
				coordinates = record[0]
				data = record[1]

				results[degrees][coordinates] = data

		return results



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


	def __degrees_from_digest(self, digest):
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
	def deserialize_publication_record(self, record):
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


	def deserialize_publication_record(self, record):
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


	def deserialize_publication_record(self, record):
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
		"""
		format: int - hid,
				separator,
				bitmask:
					0 | 1 - record is for sale
					0 | 1 - record is for rent
		"""

		sale_data = ''
		sale_bitmask = ''
		if record.for_sale:
			sale_currency = record.sale_terms.currency_sid
			if CURRENCIES.dol() == sale_currency:
				sale_bitmask += '00'
			elif CURRENCIES.uah() == sale_currency:
				sale_bitmask += '01'
			elif CURRENCIES.eur() == sale_currency:
				sale_bitmask += '10'
			else:
				raise SerializationError('invalid sale currency_sid.')

			# next fields can be None
			if record.sale_terms.price is not None:
				sale_data += str(record.sale_terms.price) + self.separator
			else:
				raise SerializationError('None-value can not be serialized.')



		rent_data = ''
		rent_bitmask = ''
		if record.for_rent:
			rent_period = record.rent_terms.period_sid
			if LIVING_RENT_PERIODS.daily() == rent_period:
				rent_bitmask += '00'
			elif LIVING_RENT_PERIODS.monthly() == rent_period:
				rent_bitmask += '01'
			elif LIVING_RENT_PERIODS.long_period() == rent_period:
				rent_bitmask += '10'
			else:
				raise SerializationError('invalid rent period_sid.')

			rent_currency = record.rent_terms.currency_sid
			if CURRENCIES.dol() == rent_currency:
				rent_bitmask += '00'
			elif CURRENCIES.uah() == rent_currency:
				rent_bitmask += '01'
			elif CURRENCIES.eur() == rent_currency:
				rent_bitmask += '10'
			else:
				raise SerializationError('invalid rent currency_sid.')

			rent_bitmask += '1' if record.rent_terms.family else '0'
			rent_bitmask += '1' if record.rent_terms.foreigners else '0'

			# next fields can be None
			if record.rent_terms.price is not  None:
				rent_data += str(record.rent_terms.price) + self.separator
			else:
				raise SerializationError('None-value can not be serialized.')

			# Не обов’язкове поле
			if record.rent_terms.persons_count is not None:
				rent_data += str(record.rent_terms.persons_count) + self.separator
			else:
				rent_data += self.separator


		# common terms
		common_data = ''
		common_bitmask = ''

		common_bitmask += '1' if record.for_sale else '0'
		common_bitmask += '1' if record.for_rent else '0'

		common_bitmask += '1' if record.body.electricity else '0'
		common_bitmask += '1' if record.body.gas else '0'
		common_bitmask += '1' if record.body.sewerage else '0'
		common_bitmask += '1' if record.body.hot_water else '0'
		common_bitmask += '1' if record.body.cold_water else '0'

		market_type = record.body.market_type_sid
		if MARKET_TYPES.new_building() == market_type:
			common_bitmask += '0'
		elif MARKET_TYPES.secondary_market() == market_type:
			common_bitmask += '1'
		else:
			raise SerializationError('invalid market_type_sid.')

		heating = record.body.heating_type_sid
		if HEATING_TYPES.individual() == heating:
			common_bitmask += '00'
		elif HEATING_TYPES.central() == heating:
			common_bitmask += '01'
		elif HEATING_TYPES.other() == heating:
			common_bitmask += '10'
		elif HEATING_TYPES.none() == heating:
			common_bitmask += '11'
		else:
			raise SerializationError('invalid heating_type_sid.')

		# next fields can be None
		common_data += str(record.body.rooms_count) + self.separator
		common_data += str(record.body.floors_count) + self.separator


		bitmask = common_bitmask + sale_bitmask + rent_bitmask
		data = common_data + sale_data + rent_data

		record_data = str(int(bitmask, 2)) + self.separator + data
		if record_data[-1] == self.separator:
			record_data = record_data[:-1]
		return record_data


	def deserialize_publication_record(self, record):
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


	def deserialize_publication_record(self, record):
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


	def deserialize_publication_record(self, record):
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


	def deserialize_publication_record(self, record):
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


	def deserialize_publication_record(self, record):
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


	def deserialize_publication_record(self, record):
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


	def deserialize_publication_record(self, record):
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


	def deserialize_publication_record(self, record):
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


	def deserialize_publication_record(self, record):
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


	def deserialize_publication_record(self, record):
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


	def deserialize_publication_record(self, record):
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