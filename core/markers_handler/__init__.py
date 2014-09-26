from django.dispatch import receiver

from core.markers_handler.models import SegmentsIndex
from core.publications import models_signals



@receiver(models_signals.before_publish)
def add_publication_marker(sender, **kwargs):
    tid = kwargs['tid']
    hid = kwargs['hid']
    SegmentsIndex.add_record(tid, hid)



@receiver(models_signals.before_unpublish)
@receiver(models_signals.moved_to_trash)
@receiver(models_signals.deleted_permanent)
def remove_publication_marker(sender, **kwargs):
    tid = kwargs['tid']
    hid = kwargs['hid']
    SegmentsIndex.remove_record(tid, hid)