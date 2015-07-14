from django.dispatch import Signal

#todo move all signals here

class PublicationsSignals(object):
    daily_rent_updated = Signal(providing_args=['tid','hid'])



