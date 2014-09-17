#coding=utf-8
import math


class Grid(object):
	SEGMENTS_PER_VIEWPORT_BY_LAT = 3
	SEGMENTS_PER_VIEWPORT_BY_LNG = 5


	def __init__(self, min_zoom, max_zoom):
		self.min_zoom = min_zoom
		self.max_zoom = max_zoom


	def segments_digests(self, lat, lng):
		result = []
		for zoom in xrange(start=self.min_zoom, stop=self.max_zoom+1):
			x, y = self.segment_xy(lat, lng, zoom)
			result.append(
				(zoom, x, y, )
			)
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
	def segment_xy(cls, lat, lng, zoom):
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
	def normalize_lat_lng(lat, lng):
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


	def normalize_zoom(self, zoom):
		if zoom < self.min_zoom:
			return self.min_zoom

		elif zoom > self.max_zoom:
			return self.max_zoom

		else:
			return zoom