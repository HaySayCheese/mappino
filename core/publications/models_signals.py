from django.dispatch import Signal


before_publish = Signal(providing_args=['tid', 'hid'])
record_updated = Signal(providing_args=['tid', 'hid'])