#coding=utf-8
from django.dispatch import Signal


# todo: додати до всіх сигналів hash_id в аргументи і в місця їх виклику

created = Signal(providing_args=['tid', 'hid'])

before_publish = Signal(providing_args=['tid', 'hid'])
published = Signal(providing_args=['tid', 'hid', 'hash_id'])
record_updated = Signal(providing_args=['tid', 'hid'])

before_unpublish = Signal(providing_args=['tid', 'hid'])
unpublished = Signal(providing_args=['tid', 'hid'])

moved_to_trash = Signal(providing_args=['tid', 'hid'])
deleted_permanent = Signal(providing_args=['tid', 'hid'])