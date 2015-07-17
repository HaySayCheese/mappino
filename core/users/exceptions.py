# coding=utf-8
from django.core.exceptions import ValidationError
from collective.exceptions import RuntimeException


class AvatarExceptions(object):
    class ImageIsTooLarge(RuntimeException): pass
    class ImageIsTooSmall(RuntimeException): pass
    class UnsupportedImageType(RuntimeException): pass
    class ProcessingFailed(RuntimeException): pass


# class EmptyAlias(ValidationError): pass
# class TooShortAlias(ValidationError): pass
# class AliasAlreadyTaken(ValidationError): pass