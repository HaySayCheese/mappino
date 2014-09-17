class SerializationError(BaseException): pass
class DeserializationError(BaseException): pass


class TooBigTransaction(Exception): pass