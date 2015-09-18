# coding=utf-8
from django.apps.config import AppConfig

from core.markers_index.models import SegmentsIndex
from core.publications import signals


class MarkersIndexConfig(AppConfig):
    name = 'core.markers_index'


    def ready(self):
        SignalsInitializer.init()


class SignalsInitializer(object):
    @classmethod
    def init(cls):
        signals.before_publish.connect(cls.__add_publication_marker)

        signals.before_unpublish.connect(cls.__remove_publication_marker)
        signals.moved_to_trash.connect(cls.__remove_publication_marker)
        signals.deleted_permanent.connect(cls.__remove_publication_marker)


    @staticmethod
    def __add_publication_marker(sender, **kwargs):
        tid = kwargs['tid']
        hid = kwargs['hid']
        for_sale = kwargs.get('for_sale', False)
        for_rent = kwargs.get('for_rent', False)

        # Таким чином, навіть якщо оголошення одночасно подається
        # і на продаж і в оренду - воно попаде в 2 індекса одночасно.
        if for_sale:
            SegmentsIndex.add_record(tid, hid, True, False)
        if for_rent:
            SegmentsIndex.add_record(tid, hid, False, True)


    @staticmethod
    def __remove_publication_marker(sender, **kwargs):
        tid = kwargs['tid']
        hid = kwargs['hid']
        for_sale = kwargs.get('for_sale', False)
        for_rent = kwargs.get('for_rent', False)

        # Таким чином, навіть якщо оголошення одночасно подавалось
        # і на продаж і в оренду - воно зникне з 2х індексів одночасно.
        if for_sale:
            SegmentsIndex.remove_record(tid, hid, True, False)
        if for_rent:
            SegmentsIndex.remove_record(tid, hid, False, True)