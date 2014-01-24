#coding=utf-8
from collective.constants import AbstractConstant


class DirtagsColors(AbstractConstant):
	def __init__(self):
		super(DirtagsColors, self).__init__()
		self.set_ids({
			0: '0',
			1: '1',
			2: '2',
			3: '3',
			4: '4',
			5: '5',
			6: '6',
			7: '7',
		})
DIR_TAGS_COLORS = DirtagsColors()