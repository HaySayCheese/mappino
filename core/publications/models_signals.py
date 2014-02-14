from django.dispatch import Signal


house_published = Signal(providing_args=['id'])
# other types here


updated = Signal(providing_args=['tid', 'hid'])