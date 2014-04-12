#coding=utf-8
from django.core.exceptions import SuspiciousOperation


class BaseCustomException(Exception):
	"""
	Використовується для скидання виключних ситуацій з кастомних методів.
	Застосовується для уникнення співпадінь з системними виключними ситуаціями.
	"""
	pass

class InvalidValue(BaseCustomException): pass
class DuplicateValue(InvalidValue): pass


class InvalidArgument(InvalidValue): pass
class EmptyArgument(InvalidArgument): pass


class RuntimeException(BaseCustomException): pass


class ResourceThrottled(SuspiciousOperation): pass



class AlreadyExist(Exception):
	pass

class ObjectAlreadyExist(AlreadyExist):
	pass

class RecordAlreadyExists(AlreadyExist):
	pass

class RecordDoesNotExists(Exception):
	pass


class ParseError(Exception):
	pass



class IntervalError(Exception):
	pass



