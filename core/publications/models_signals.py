from django.dispatch import Signal


created = Signal(providing_args=['tid', 'hid'])

before_publish = Signal(providing_args=['tid', 'hid'])
record_updated = Signal(providing_args=['tid', 'hid'])

before_unpublish = Signal(providing_args=['tid', 'hid'])
unpublished = Signal(providing_args=['tid', 'hid'])

moved_to_trash = Signal(providing_args=['tid', 'hid'])
deleted_permanent = Signal(providing_args=['tid', 'hid'])