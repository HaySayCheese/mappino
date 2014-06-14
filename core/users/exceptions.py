from django.core.exceptions import ValidationError


class EmptyAlias(ValidationError): pass
class TooShortAlias(ValidationError): pass
class AliasAlreadyTaken(ValidationError): pass