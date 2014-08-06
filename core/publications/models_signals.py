#coding=utf-8
from django.dispatch import Signal


created = Signal(providing_args=['tid', 'hid', 'hash_id'])

before_publish = Signal(providing_args=['tid', 'hid', 'hash_id'])
published = Signal(providing_args=['tid', 'hid', 'hash_id'])
record_updated = Signal(providing_args=['tid', 'hid', 'hash_id'])

before_unpublish = Signal(providing_args=['tid', 'hid', 'hash_id'])
unpublished = Signal(providing_args=['tid', 'hid', 'hash_id'])

moved_to_trash = Signal(providing_args=['tid', 'hid', 'hash_id'])
deleted_permanent = Signal(providing_args=['tid', 'hid', 'hash_id'])