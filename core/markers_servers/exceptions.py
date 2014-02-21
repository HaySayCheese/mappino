from django.core.exceptions import SuspiciousOperation


class TooBigTransaction(SuspiciousOperation): pass


class SerializationError(SuspiciousOperation): pass
class DeserializationError(SuspiciousOperation): pass