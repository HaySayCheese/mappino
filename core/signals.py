from django.dispatch import Signal

from core.markers_handler.models import SegmentsIndex


class PublicationsSignals(object):
    daily_rent_added = Signal(providing_args=['tid','hash_id','date_from','date_to'])
    daily_rent_deleted = Signal(providing_args=['tid','hash_id','date_from','date_to'])


def initialize_all_signals():
    PublicationsSignals.daily_rent_added.connect(SegmentsIndex.add_daily_rent_terms)
    return



