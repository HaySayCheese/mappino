from django.dispatch import Signal


record_published = Signal(providing_args=['tid', 'hid'])
record_updated = Signal(providing_args=['tid', 'hid'])