from django.core.exceptions import ValidationError
from collective.exceptions import RuntimeException



class TooLargeImage(RuntimeException): pass
class TooSmallImage(RuntimeException): pass
class InvalidImageFormat(RuntimeException): pass



class EmptyAlias(ValidationError): pass
class TooShortAlias(ValidationError): pass
class AliasAlreadyTaken(ValidationError): pass