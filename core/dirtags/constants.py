#coding=utf-8
from collective.constants import AbstractConstant


class DirtagsColorsIDs(AbstractConstant):
	def __init__(self):
		super(DirtagsColorsIDs, self).__init__()
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
DIRTAGS_COLORS_IDS = DirtagsColorsIDs()