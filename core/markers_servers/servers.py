#coding=utf-8
import abc
from django.core.exceptions import SuspiciousOperation
from core.markers_servers.exceptions import TooBigTransaction

from core.markers_servers.utils import DegreeSegmentPoint, DegreePoint, SegmentPoint, LatLngPoint
from core.publications.constants import OBJECTS_TYPES, HEAD_MODELS
from mappino.wsgi import redis_connections



class AbstractMarkersServer(object):
	__metaclass__ = abc.ABCMeta

	def __init__(self, tid):
		if tid not in OBJECTS_TYPES.values():
			raise ValueError('invalid @tid.')
		self.tid = tid
		self.model = HEAD_MODELS[tid]
		self.redis = redis_connections['steady']
		self.separator = ';'


	def markers(self, ne_lat, ne_lng, sw_lat, sw_lng, condition):
		current = DegreeSegmentPoint(ne_lat, ne_lng)
		stop = DegreeSegmentPoint(sw_lat, sw_lng)
		digests = []
		while (current.degree.lat != stop.degree.lat) and \
				(current.segment.lat != stop.segment.lat):
			while (current.degree.lng != stop.degree.lng) and \
					(current.segment.lng != stop.segment.lng):
				digests.append(self.__segment_digest(current.degree, current.segment))

				# Заборонити одночасну вибірку маркерів з великої к-сті сегментів.
				# Таким чином можна уберегтись від занадто великих транзакцій і накопичування
				# великої к-сті запитів від інших користувачів в черзі на обробку.
				if len(digests) > 5*5:
					raise TooBigTransaction()

				current.inc_segment_lng()
			current.dec_segment_lat()

		filtered_pubs = []
		for digest in digests:
			filtered = self.filter(self.redis.hkeys(digest), condition)
			formatted = self.format(filtered)
			filtered_pubs.extend(formatted)


	def add_publication(self, hid):
		record = self.record_queryset(hid).only(
			'degree_lng', 'degree_lat', 'segment_lng', 'segment_lat', 'pos_lng', 'pos_lat')[0]

		degree = DegreePoint(record.degree_lat, record.degree_lng)
		segment = SegmentPoint(record.segment_lat, record.segment_lng)
		position = LatLngPoint(record.pos_lat, record.pos_lng)

		seg_digest = self.__segment_digest(degree, segment)
		pos_digest = self.__position_digest(position)
		data = self.serialize_publication_record(record)

		self.redis.hset(seg_digest, pos_digest, data)


	def __segment_digest(self, degree, segment):
		if degree.lng >= 0:
			degree_digest = str(degree.lat) + '+' + str(degree.lng)
		else:
			degree_digest = str(degree.lat) + str(degree.lng)
		return  str(self.tid) + ':' + degree_digest + ':' + str(segment.lat) + ':' + str(segment.lng)


	@staticmethod
	def __position_digest(pos):
		return str(pos.lat) + ':' + str(pos.lng)


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



class HousesMarkersServer(AbstractMarkersServer):
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

