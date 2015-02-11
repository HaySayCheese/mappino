from django.dispatch import receiver

from core.markers_handler.models import SegmentsIndex
from core.publications import models_signals



@receiver(models_signals.before_publish)
def add_publication_marker(sender, **kwargs):
    tid = kwargs['tid']
    hid = kwargs['hid']
    for_sale = kwargs.get('for_sale', False)
    for_rent = kwargs.get('for_rent', False)

    SegmentsIndex.add_record(tid, hid, for_sale, for_rent)



@receiver(models_signals.before_unpublish)
@receiver(models_signals.moved_to_trash)
@receiver(models_signals.deleted_permanent)
def remove_publication_marker(sender, **kwargs):
    tid = kwargs['tid']
    hid = kwargs['hid']
    for_sale = kwargs.get('for_sale', False)
    for_rent = kwargs.get('for_rent', False)

    SegmentsIndex.remove_record(tid, hid, for_sale, for_rent)