#coding=utf-8
from collective.exceptions import InvalidArgument
from core.markers_servers.grids import Grid
from core.publications.constants import HEAD_MODELS


class MPSManager(object): # MPS = Markers Per Segment
	def __init__(self):
		self.grid = Grid()
		self.estimate_count = self.grid.estimate_count  # Трансляція функції з об’єкта в об’єкт
														# для економії одного виклику функції і трошки коду :)


	def add_publication(self, tid, hid):
		lat, lng = self.publication_lat_lng(tid, hid)
		return self.grid.add_marker(lat, lng, tid)


	def remove_publication(self, tid, hid):
		lat, lng = self.publication_lat_lng(tid, hid)
		return self.grid.add_marker(lat, lng, tid)


	@staticmethod
	def publication_lat_lng(tid, hid):
		model = HEAD_MODELS[tid]

		try:
			p = model.objects.filter(id=hid).only(
				'degree_lat', 'degree_lng', 'pos_lat', 'pos_lng')[:1][0]
		except IndexError:
			raise InvalidArgument('Object with such hid does not exist.')


		lat = float('{0}.{1}'.format(p.segment_lat, p.pos_lat))
		lng = float('{0}.{1}'.format(p.segment_lng, p.pos_lng))
		return lat, lng