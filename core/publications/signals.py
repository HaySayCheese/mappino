#coding=utf-8
from django.dispatch import Signal


created = Signal(providing_args=['tid', 'hid', 'hash_id', 'for_sale', 'for_rent'])

before_publish = Signal(providing_args=['tid', 'hid', 'hash_id', 'for_sale', 'for_rent'])
published = Signal(providing_args=['tid', 'hid', 'hash_id', 'for_sale', 'for_rent'])
record_updated = Signal(providing_args=['tid', 'hid', 'hash_id', 'for_sale', 'for_rent'])

before_unpublish = Signal(providing_args=['tid', 'hid', 'hash_id', 'for_sale', 'for_rent'])
unpublished = Signal(providing_args=['tid', 'hid', 'hash_id', 'for_sale', 'for_rent'])

queued = Signal(providing_args=['tid', 'hid', 'hash_id'])

moved_to_trash = Signal(providing_args=['tid', 'hid', 'hash_id', 'for_sale', 'for_rent'])
deleted_permanent = Signal(providing_args=['tid', 'hid', 'hash_id', 'for_sale', 'for_rent'])

before_rejection_by_moderator = Signal(providing_args=['tid', 'hid', 'hash_id', 'for_sale', 'for_rent'])
rejected_by_moderator = Signal(providing_args=['tid', 'hid', 'hash_id', 'for_sale', 'for_rent'])

before_marking_as_outdated = Signal(providing_args=['tid', 'hid', 'hash_id', 'for_sale', 'for_rent'])
after_marking_as_outdated = Signal(providing_args=['tid', 'hid', 'hash_id', 'for_sale', 'for_rent'])


class DailyRentSignals(object):
    booked = Signal(['tid', 'publication_id', 'date_enter', 'date_leave'])
    reservation_canceled = Signal(['tid', 'publication_id', 'date_enter', 'date_leave'])