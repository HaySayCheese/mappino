#coding=utf-8
import math

from collective.exceptions import RuntimeException
from core.markers_servers.exceptions import TooBigTransaction
from mappino.wsgi import redis_connections


class Grid(object):
	SEGMENTS_PER_VIEWPORT_BY_LAT = 3
	SEGMENTS_PER_VIEWPORT_BY_LNG = 5

	MIN_ZOOM = 1
	MAX_ZOOM = 14

	REDIS_HASH_KEY = 'markers_segments_count'


	def __init__(self):
		self.redis = redis_connections['steady']


	def add_marker(self, lat, lng, tid):
		"""
		Знаходить сегмент, в якому лежать координати маркера і збільшує його лічильник на 1.
		І так для кожного масштабу.
		"""
		lat, lng = self.__normalize_lat_lng(lat, lng)

		# Процедура збільшення/зменшення лічильника відрізняється лише знаком.
		return self.__inc_markers_count(lat, lng, tid, 1)


	def remove_marker(self, lat, lng, tid):
		"""
		Знаходить сегмент, в якому лежать координати маркера і зменшує його лічильник на 1.
		І так для кожного масштабу.
		"""
		lat, lng = self.__normalize_lat_lng(lat, lng)

		# Процедура збільшення/зменшення лічильника відрізняється лише знаком.
		return self.__inc_markers_count(lat, lng, tid, -1)


	def estimate_count(self, tid, ne_lat, ne_lng, sw_lat, sw_lng, zoom=1):
		ne_lat, ne_lng = self.__normalize_lat_lng(ne_lat, ne_lng)
		sw_lat, sw_lng = self.__normalize_lat_lng(sw_lat, sw_lng)
		zoom = self.__normalize_zoom(zoom)


		# Повертаємо координатний прямокутник таким чином, щоб ne точно був на своєму місці.
		# Таким чином уберігаємось від випадків, коли координати передані некоректно.
		if ne_lat < sw_lat:
			sw_lat, ne_lat = ne_lat, sw_lat

		if ne_lng > sw_lng:
			sw_lng, ne_lng = ne_lng, sw_lng


		# Починаємо вибірку
		ne_segment_x, ne_segment_y = self.__segment_xy_from_lat_lng(ne_lat, ne_lng, zoom)
		sw_segment_x, sw_segment_y = self.__segment_xy_from_lat_lng(sw_lat, sw_lng, zoom)

		lng_segments_count = sw_segment_x-ne_segment_x+1 if sw_segment_x-ne_segment_x > 0 else 1
		lat_segments_count = ne_segment_y-sw_segment_y+1 if ne_segment_y-sw_segment_y > 0 else 1
		total_segments_count = lat_segments_count * lng_segments_count


		# Заглушка від DDos
		if total_segments_count > 240:
			raise TooBigTransaction()


		# Формуємо транзакцію до redis
		pipe = self.redis.pipeline()
		for x in xrange(start=ne_segment_x, stop=ne_segment_x + lng_segments_count):
			for y in xrange(start=sw_segment_y, stop=sw_segment_y + lat_segments_count):
				digest = self.__segment_digest(tid, x, y, zoom)
				pipe.hget(self.REDIS_HASH_KEY, digest)

		markers_count_list = pipe.execute()


		lat_step = self.step_on_lat(zoom)
		lng_step = self.step_on_lng(zoom)

		index = 0
		result = {}
		for x in xrange(start=ne_segment_x, stop=ne_segment_x + lng_segments_count):
			for y in xrange(start=sw_segment_y, stop=sw_segment_y + lat_segments_count):
				res_lat = y * lat_step - (lat_step / 2) - 90    # Повертаєму координати назад
				res_lng = x * lng_step - (lng_step / 2) - 180   # у звичний формат з мінусами

				count = markers_count_list[index]
				index += 1

				if count is not None:
					try:
						count = int(count)
					except ValueError:
						raise RuntimeException(
							'Segment contains non-int value, but must contain int, '
							'because this is markers count in this segment.')

					segment_coordinates = '{0};{1}'.format(res_lat, res_lng)
					result[segment_coordinates] = count


		return result


	@classmethod
	def segments_on_lat(cls, zoom):
		return cls.__segments_per_zoom(zoom, cls.SEGMENTS_PER_VIEWPORT_BY_LAT)


	@classmethod
	def segments_on_lng(cls, zoom):
		return cls.__segments_per_zoom(zoom, cls.SEGMENTS_PER_VIEWPORT_BY_LNG)


	@classmethod
	def step_on_lat(cls, zoom):
		return 180.0 / cls.segments_on_lat(zoom)


	@classmethod
	def step_on_lng(cls, zoom):
		return 360.0 / cls.segments_on_lng(zoom)


	@classmethod
	def __segment_xy_from_lat_lng(cls, lat, lng, zoom):
		x = int(math.ceil(lng / cls.step_on_lng(zoom)))
		y = int(math.ceil(lat / cls.step_on_lat(zoom)))
		return x, y


	@staticmethod
	def __segments_per_zoom(zoom, segments_per_viewport):
		k = 2   # Is not a magic number.
				# First 2 zoom-levels have the same segments count,
				# so that need to be handled in code in such method.

		pow_ratio = zoom-k if zoom-k >= 0 else 0
		return segments_per_viewport * (k**pow_ratio)


	@staticmethod
	def __segment_digest(tid, x, y, zoom):
		return '{tid}:{y}:{x}:{z}'.format(tid=tid, x=x, y=y, z=zoom)


	@staticmethod
	def __normalize_lat_lng(lat, lng):
		# Переносимо координати в плюсову площину, щоб не мати мороки зі знаками
		lat += 90
		lng += 180

		# Широта і довгота не можуть строго дорівнювати 0,
		# бо інакше по даним координатам буде неправильно розраховано комірку сітки, в якій вони лежать.
		# Дану перевірку можна було б проводити в функції, яка безпосередньо займається розрахунком комірки,
		# але з огляду на оптимізацію дану перевірку винесено сюди.
		# (краще один раз перевірити і далі працювати з перевіреними даними,
		#  ніж на кожній ітерації знову перевіряти те ж саме)
		#
		# Також, широта і довгота перевіряються на предмет переповнення по максимальному значенню.
		# В цьому випадку вони зменшуються до найбільшого допустимого значення.
		if lat <= 0:
			lat = 0.00001
		elif lat >= 180:
			lat = 179.99999

		if lng <= 0:
			lng = 0.00001
		elif lng >= 360:
			lng = 359.99999

		return lat, lng


	@classmethod
	def __normalize_zoom(cls, zoom):
		if zoom < cls.MIN_ZOOM:
			return cls.MIN_ZOOM

		elif zoom > cls.MAX_ZOOM:
			return cls.MAX_ZOOM

		else:
			return zoom



	def __inc_markers_count(self, lat, lng, tid, amount):
		pipe = self.redis.pipeline()
		for zoom in xrange(start=self.MIN_ZOOM, stop=self.MAX_ZOOM+1):
			x, y = self.__segment_xy_from_lat_lng(lat, lng, zoom)
			digest = self.__segment_digest(tid, x, y, zoom)
			pipe.hincrby(self.REDIS_HASH_KEY, digest, amount)

		pipe.execute()