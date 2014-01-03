#coding=utf-8


class InvalidCode(ValueError): pass
class InvalidCodeLength(InvalidCode): pass
class ForbiddenCode(InvalidCode): pass

def validate_ua_phone_code(code):
	if not isinstance(code, basestring):
		raise InvalidCode('"code" is not a string type.')

	if len(code) != 2:
		raise InvalidCodeLength('"code" length != 2.')

	try:
		int(code)
	except Exception:
		raise InvalidCode('"code" can not be converted to int.')

	ua_phone_codes = [
		'91', # Тримоб
		'99', # MTC
		'95', # MTC
	    '66', # MTC
	    '50', # MTC
	    '39', # Київстар
	    '68', # Київстар
	    '98', # Київстар
	    '97', # Київстар
	    '96', # Київстар
	    '67', # Київстар
	    '94', # Інтертелеком
	    '92', # PEOPLEnet
	    '93', # life :)
	    '63', # life :)
	]
	if code not in ua_phone_codes:
		raise ForbiddenCode('"code" is not in Ukrainian phone codes list.')




class InvalidPhoneNumber(ValueError): pass
class InvalidPhoneNumberLength(InvalidPhoneNumber): pass

def validate_phone_number(number):
	if not isinstance(number, basestring):
		raise InvalidPhoneNumber('number is not a string type')

	if len(number) != 7:
		raise InvalidPhoneNumberLength('number length != 7')

	try:
		int(number)
	except Exception:
		raise InvalidPhoneNumber("number can't be converted to int")




class InvalidPassword(ValueError): pass
class InvalidPasswordLength(InvalidPassword): pass

def validate_password(password, complexity_check_method=None):
	# complexity_check_method - функція, яка як параметр приймає переданий пароль (password),
	# проводоить його тестування на предмет надійності та повертає True у випадку успіху,
	# або False, випадку невідповідного паролю.
	#
	# complexity_check_method може бути відсутнім.

	if not isinstance(password, basestring):
		raise InvalidPassword('"password" is not a string type.')

	if len(password) == 0:
		raise InvalidPasswordLength('"password" is empty.')

	if complexity_check_method is not None:
		if not complexity_check_method(password):
			raise InvalidPassword('Complexity check of the "password" failed.')