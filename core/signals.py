from django.dispatch import Signal
class PublicationsSignals(object):
    daily_rent_added = Signal(providing_args=['tid','hash_id','date_from','date_to'])
    daily_rent_deleted = Signal(providing_args=['tid','hash_id','date_from','date_to'])



