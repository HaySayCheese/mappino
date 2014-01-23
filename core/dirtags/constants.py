#coding=utf-8
from collective.constants import AbstractConstant


class DirtagsColors(AbstractConstant):
	def __init__(self):
		super(DirtagsColors, self).__init__()
		self.set_ids({
			'0': '',
			'1': '',
			'2': '',
			'3': '',
			'4': '',
			'5': '',
			'6': '',
			'7': '',
		})
DIR_TAGS_COLORS = DirtagsColors()