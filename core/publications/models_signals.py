from django.dispatch import Signal


house_published = Signal(providing_args=['id'])