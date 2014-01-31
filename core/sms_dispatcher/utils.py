#coding=utf8
import urllib
from core.sms_dispatcher import LIMITERS, SEND_LOGGER
from core.sms_dispatcher.exceptions import SMSSendingError
from mappino.settings import SMS_GATE_LOGIN, SMS_GATE_PASSWORD


def send_mobile_check_code_sms(number, code, request):
	LIMITERS['registration_per_number'].check_transaction(number, request)
	LIMITERS['registration_per_ip'].check_transaction(number, request)

	message = 'Добро пожаловать на mappino. Ваш код: {0}'.format(code)
	return __send_sms(number, message)


def resend_mobile_check_code_sms(number, code, request):
	LIMITERS['registration_per_number'].check_transaction(number, request)
	LIMITERS['registration_per_ip'].check_transaction(number, request)

	message = 'Ваш проверочный код mappino: {0}'.format(code)
	return __send_sms(number, message)


def __send_sms(number, message):
	if not number:
		raise ValueError('invalid number')
	if not message:
		raise ValueError('invalid code')

	params = urllib.urlencode({
		'login': SMS_GATE_LOGIN,
		'psw': SMS_GATE_PASSWORD,
	    'phones': '+380'+str(number),
	    'mes': message,
	    'charset': 'utf-8'
	})
	response = urllib.urlopen("http://smsc.ru/sys/send.php", params).read()
	log_record = 'SENDED WELL. number: {number}, message: {message}, response: {response}'.format(
		number = number, message = message, response = response)

	if 'OK' in response:
		SEND_LOGGER.info('SENDED WELL. {0}'.format(log_record))
	else:
		SEND_LOGGER.error(log_record)
		raise SMSSendingError()
