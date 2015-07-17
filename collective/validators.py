#coding=utf-8
import string
from django.core.exceptions import ValidationError



def validate_mobile_phone_number(number):
	"""
	Validates "number" by several countries formats.
	If at least one country format check will be passed — number is considered as correct.
	"""
	if not number:
		raise ValidationError('Empty phone number.')


	# check for invalid symbols
	valid_symbols = string.digits + '+'
	for symbol in number:
		if not symbol in valid_symbols:
			raise ValidationError('Invalid symbol detected: "{0}". Number: {1}'.format(symbol, number))


	# check for various countries formats
	if __phone_number_is_ua(number):
		return

	# ...
	# other country format check here
	#...

	# no one country format detected
	raise ValidationError('Phone number is not valid: {0}'.format(number))



def __phone_number_is_ua(number):
	if len(number) != 13:
		return False

	if number[:4] != u'+380':
		return False

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
	if number[4:6] not in ua_phone_codes:
		return False
	return True


#...
# other countries format checkers here
#...