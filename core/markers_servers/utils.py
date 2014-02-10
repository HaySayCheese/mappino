#coding=utf-8


class LatLngPoint(object):
	def __init__(self, lat, lng):
		if not lat: raise ValueError('Empty @lat.')
		if not lng: raise ValueError('Empty @lng.')
		self.lat = int(lat)
		self.lng = int(lng)



class DegreePoint(object):
	max_lat =  89
	min_lat = -89
	max_lng =  179
	min_lng = -179

	def __init__(self, lat, lng):
		try:
			self.lat = int(lat)
			self.lng = int(lng)
		except ValueError:
			raise ValueError('Invalid parameters. Conversion to int can not be done.')

		if abs(self.lat) > self.max_lat:
			raise ValueError('Invalid latitude. Abs. value is greater than 90.')
		if abs(self.lng) > self.max_lng:
			raise ValueError('Invalid longitude. Abs. value is greater than 180.')


	def add_lat(self, d):
		self.lat += d
		if self.lat > self.max_lat:
			self.lat = self.max_lat


	def subtract_lat(self, d):
		self.lat -= d
		if self.lat < self.min_lat:
			self.lat = self.min_lat


	def add_lng(self, d):
		while d > self.max_lng:
			d -= self.max_lng

		self.lng += d
		while self.lng > self.max_lng:
			self.lng = self.min_lng + abs(self.max_lng - self.lng) - 1


	def subtract_lng(self, d):
		while d > self.max_lng:
			d -= self.max_lng

		self.lng -= d
		while self.lng < self.min_lng:
			self.lng = self.max_lng - self.min_lng + self.lng + 1



class SegmentPoint(object):
	step = 2
	max = 100 - step
	min = 0


	def __init__(self, lat, lng):
		try:
			self.lat = int(lat)
			self.lng = int(lng)
		except ValueError:
			raise ValueError('Invalid parameters. Conversion to int can not be done.')

		if not (self.min <= self.lat <= self.max):
			raise ValueError('Invalid parameters.')
		if not (self.min <= self.lng <= self.max):
			raise ValueError('Invalid parameters.')

		while self.lat % self.step != 0:
			self.lat -= 1
		while self.lng % self.step != 0:
			self.lng -= 1


	def inc_lat(self):
		"""
		Збільшить широту сегменту на step.
		Поверне True, якщо відбулось переповнення, інакше - поверне False
		"""
		self.lat += self.step
		if self.lat > self.max:
			self.lat = self.min
			return True
		return False


	def dec_lat(self):
		"""
		Зменшить широту сегменту на step.
		Поверне True, якщо відбулось анти-переповнення, інакше - поверне False
		"""
		self.lat -= self.step
		if self.lat < self.min:
			self.lat = self.max
			return True
		return False


	def inc_lng(self):
		"""
		Збільшить довготу сегменту на step.
		Поверне True, якщо відбулось переповнення, інакше - поверне False
		"""
		self.lng += self.step
		if self.lng > self.max:
			self.lng = self.min
			return True
		return False


	def dec_lng(self):
		"""
		Зменшить довготу сегменту на step.
		Поверне True, якщо відбулось анти-переповнення, інакше - поверне False
		"""
		self.lng -= self.step
		if self.lng < self.min:
			self.lng = self.max
			return True
		return False



class DegreeSegmentPoint(object):
	def __init__(self, lat, lng):
		if not '.' in lat:
			raise ValueError('Invalid latitude. "." is absent.')
		if not '.' in lng:
			raise ValueError('Invalid longitude. "." is absent.')

		degree_lat, segment_lat = lat.split('.')
		degree_lng, segment_lng = lng.split('.')

		self.degree = DegreePoint(degree_lat, degree_lng)

		if len(segment_lat) < 2:
			raise ValueError('Invalid latitude. (Shortest than 2)')
		if len(segment_lng) < 2:
			raise ValueError('Invalid longitude. (Shortest than 2)')
		self.segment = SegmentPoint(segment_lat[:2], segment_lng[:2])


	def dec_segment_lat(self):
		if self.segment.dec_lat():
			self.degree.subtract_lat(1)


	def inc_segment_lat(self):
		if self.segment.inc_lat():
			self.degree.add_lat(1)


	def dec_segment_lng(self):
		if self.segment.dec_lng():
			self.degree.subtract_lng(1)


	def inc_segment_lng(self):
		if self.segment.inc_lng():
			self.degree.add_lng(1)