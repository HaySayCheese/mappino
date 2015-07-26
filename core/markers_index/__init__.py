# coding=utf-8
from django.dispatch import receiver

from core.markers_index.models import SegmentsIndex
from core.publications import signals


@receiver(signals.before_publish)
def add_publication_marker(sender, **kwargs):
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


@receiver(signals.before_unpublish)
@receiver(signals.moved_to_trash)
@receiver(signals.deleted_permanent)
def remove_publication_marker(sender, **kwargs):
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