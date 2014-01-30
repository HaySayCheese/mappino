#coding=utf-8
from collective.constants import AbstractConstant


class SaleTypes(AbstractConstant):
	def __init__(self):
		super(SaleTypes, self).__init__()
		self.set_ids({
			'all_house': 0, # весь дім
			'part': 1, # частина дому
		})

	def all_house(self):
		return self.ids['all_house']

	def part(self):
		return self.ids['part']
HOUSE_SALE_TYPES = SaleTypes()
HOUSE_RENT_TYPES = SaleTypes()