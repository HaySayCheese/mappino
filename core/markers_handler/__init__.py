#coding=utf-8
from django.dispatch import receiver

from core.markers_handler.models import SegmentsIndex
from core.publications import models_signals
from core.signals import PublicationsSignals

@receiver(models_signals.before_publish)
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


@receiver(models_signals.before_unpublish)
@receiver(models_signals.moved_to_trash)
@receiver(models_signals.deleted_permanent)
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


@receiver(PublicationsSignals.daily_rent_updated)
def update_calendar_rent(sender, **kwargs):
    #todo comments
    kwargs['for_rent'] = True
    remove_publication_marker(sender, **kwargs)
    add_publication_marker(sender, **kwargs)


