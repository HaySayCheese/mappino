from django.dispatch import Signal


before_publish = Signal(providing_args=['tid', 'hid'])
record_updated = Signal(providing_args=['tid', 'hid'])

unpublished = Signal(providing_args=['tid', 'hid'])

moved_to_trash = Signal(providing_args=['tid', 'hid'])
deleted_permanent = Signal(providing_args=['tid', 'hid'])