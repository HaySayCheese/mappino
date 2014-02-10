from django.core.exceptions import SuspiciousOperation


class TooBigTransaction(SuspiciousOperation): pass