#coding=utf-8
class BaseCustomException(Exception):
	"""
	Використовується для скидання виключних ситуацій з кастомних методів.
	Застосовується для уникнення співпадінь з системними виключними ситуаціями.
	"""
	pass

class InvalidArgument(BaseCustomException): pass
class RuntimeException(BaseCustomException): pass



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



