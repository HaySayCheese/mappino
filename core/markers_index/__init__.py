# coding=utf-8
from django.apps.config import AppConfig

from core.markers_index.slots import SlotsInitializer


class MarkersIndex(AppConfig):
    name = 'core.markers_index'


    def ready(self):
        segments_index = self.get_model('SegmentsIndex')
        self.slots_initializer = SlotsInitializer(segments_index)
        self.slots_initializer.connect_all()