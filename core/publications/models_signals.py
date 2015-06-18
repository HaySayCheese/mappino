#coding=utf-8
from django.dispatch import Signal


created = Signal(providing_args=['tid', 'hid', 'hash_id', 'for_sale', 'for_rent'])

before_publish = Signal(providing_args=['tid', 'hid', 'hash_id', 'for_sale', 'for_rent'])
published = Signal(providing_args=['tid', 'hid', 'hash_id', 'for_sale', 'for_rent'])
record_updated = Signal(providing_args=['tid', 'hid', 'hash_id', 'for_sale', 'for_rent'])

before_unpublish = Signal(providing_args=['tid', 'hid', 'hash_id', 'for_sale', 'for_rent'])
unpublished = Signal(providing_args=['tid', 'hid', 'hash_id', 'for_sale', 'for_rent'])

moved_to_trash = Signal(providing_args=['tid', 'hid', 'hash_id', 'for_sale', 'for_rent'])
deleted_permanent = Signal(providing_args=['tid', 'hid', 'hash_id', 'for_sale', 'for_rent'])