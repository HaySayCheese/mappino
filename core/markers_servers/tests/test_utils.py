from unittest import TestCase
from core.markers_servers.utils import DegreePoint, SegmentPoint


class TestDegreePoint(TestCase):
	def test_creation(self):
		with self.assertRaises(ValueError):
			DegreePoint(0, 180)
		with self.assertRaises(ValueError):
			DegreePoint(0, -180)

		for i in xrange(0, 179):
			DegreePoint(0, i)
			DegreePoint(0, -i)

		with self.assertRaises(ValueError):
			DegreePoint(90, 0)
		with self.assertRaises(ValueError):
			DegreePoint(-90, 0)

		for i in xrange(0, 89):
			DegreePoint(i, 0)
			DegreePoint(-i, 0)


	def test_lat_addition(self):
		p = DegreePoint(0, 0)
		p.add_lat(1)
		self.assertEqual(p.lat, 1)

		p = DegreePoint(89, 0)
		p.add_lat(1)
		self.assertEqual(p.lat, 89)

		p = DegreePoint(0, 0)
		p.add_lat(100)
		self.assertEqual(p.lat, 89)


	def test_lat_subtraction(self):
		p = DegreePoint(0, 0)
		p.subtract_lat(1)
		self.assertEqual(p.lat, -1)

		p = DegreePoint(-89, 0)
		p.subtract_lat(1)
		self.assertEqual(p.lat, -89)

		p = DegreePoint(0, 0)
		p.subtract_lat(100)
		self.assertEqual(p.lat, -89)


	def test_lng_addition(self):
		p = DegreePoint(0, 0)
		p.add_lng(1)
		self.assertEqual(p.lng, 1)

		p = DegreePoint(0, 179)
		p.add_lng(1)
		self.assertEqual(p.lng, -179)

		p = DegreePoint(0, -179)
		p.add_lng(1)
		self.assertEqual(p.lng, -178)

		p = DegreePoint(0, -1)
		p.add_lng(1)
		self.assertEqual(p.lng, 0)


	def test_lng_subtraction(self):
		p = DegreePoint(0, 0)
		p.subtract_lng(1)
		self.assertEqual(p.lng, -1)

		p = DegreePoint(0, 179)
		p.subtract_lng(1)
		self.assertEqual(p.lng, 178)

		p = DegreePoint(0, -179)
		p.subtract_lng(1)
		self.assertEqual(p.lng, 179)

		p = DegreePoint(0, -1)
		p.subtract_lng(1)
		self.assertEqual(p.lng, -2)


class TestSegmentPoint(TestCase):
	def test_creation(self):
		self.assertEqual(SegmentPoint.max % SegmentPoint.step, 0)

		with self.assertRaises(ValueError):
			SegmentPoint(100, 0)

		with self.assertRaises(ValueError):
			SegmentPoint(0, 100)

		with self.assertRaises(ValueError):
			SegmentPoint(-1, 0)

		with self.assertRaises(ValueError):
			SegmentPoint(0, -1)


	def test_lat_inc(self):
		s = SegmentPoint(0, 0)
		self.assertEqual(s.inc_lat(), False)
		self.assertEqual(s.lat, s.step)

		s = SegmentPoint(SegmentPoint.max, 0)
		self.assertEqual(s.inc_lat(), True)
		self.assertEqual(s.lat, SegmentPoint.min)


	def test_lat_dec(self):
		s = SegmentPoint(SegmentPoint.max, 0)
		self.assertEqual(s.dec_lat(), False)
		self.assertEqual(s.lat, SegmentPoint.max - SegmentPoint.step)

		s = SegmentPoint(0, 0)
		self.assertEqual(s.dec_lat(), True)
		self.assertEqual(s.lat, s.max)


	def test_lng_inc(self):
		s = SegmentPoint(0, 0)
		self.assertEqual(s.inc_lng(), False)
		self.assertEqual(s.lng, s.step)

		s = SegmentPoint(0, SegmentPoint.max)
		self.assertEqual(s.inc_lng(), True)
		self.assertEqual(s.lng, SegmentPoint.min)


	def test_lng_dec(self):
		s = SegmentPoint(0, SegmentPoint.max)
		self.assertEqual(s.dec_lng(), False)
		self.assertEqual(s.lng, SegmentPoint.max - SegmentPoint.step)

		s = SegmentPoint(0, 0)
		self.assertEqual(s.dec_lng(), True)
		self.assertEqual(s.lng, s.max)



