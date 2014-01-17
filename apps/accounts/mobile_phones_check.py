#coding=utf-8
import random
import string
from collective.http.cookies import set_cookie, set_signed_cookie
from mappino.wsgi import redis_connections


redis = redis_connections[1]


COOKIE_NAME = 'mcheck'
COOKIE_SALT = 'JMH2FWWYa1ogCJR0gW4z'

CODE_FIELD = 'code'
ATTEMPTS_FIELD = 'attempts'
MAX_ATTEMPTS_COUNT = 3


def is_number_check_started(request):
	# todo: додати тротлінг iр-адреси
	if COOKIE_NAME in request.COOKIES:
		return True
	else:
		return False


def start_number_check(raw_number, http_response):
	# todo: test me
	# generate user id avoiding duplicates
	uid_length = 32
	uid = ''.join(random.choice(string.uppercase + string.lowercase + string.digits) for x in range(uid_length))
	while redis.exists(uid): # todo: перевірити при умові, що такий код вже існує
		uid = ''.join(random.choice(string.uppercase + string.lowercase + string.digits) for x in range(uid_length))

	# save user id in redis
	pipe = redis.pipeline()
	pipe.hset(uid, CODE_FIELD, int(''.join(random.choice(string.digits) for x in range(6))))
	pipe.hset(uid, ATTEMPTS_FIELD, 0)
	pipe.expire(uid, 60*60*3)
	pipe.execute()

	# save cookie
	set_signed_cookie(http_response, COOKIE_NAME, uid, salt=COOKIE_SALT, days_expire=1)

	# send SMS
	# todo: send sms here
	# todo: додати перевірку на дотримання часового інтервалу до повторної SMS
	# todo: додати обмеження на к-сть SMS в день
	# todo: додати обмеження на к-сть SMS на одну ip-адресу.


def check_code(code, request, response):
	# todo: test me
	uid = request.COOKIES[COOKIE_NAME]
	if not redis.exists(uid):
		response.delete_cookie(COOKIE_NAME)
		raise KeyError('{0} is not in redis database.'.format(uid))

	attempts_count = redis.hget(uid, ATTEMPTS_FIELD)
	if attempts_count is None:
		response.delete_cookie(COOKIE_NAME)
		raise KeyError('field @attempts is not in hash {0}.'.format(uid))

	if attempts_count >= MAX_ATTEMPTS_COUNT:
		response.delete_cookie(COOKIE_NAME)
		redis.delete(uid)
		return False

	true_code = redis.hget(uid, CODE_FIELD)
	if true_code is None:
		response.delete_cookie(COOKIE_NAME)
		redis.delete(uid)
		raise KeyError('field @code is not in hash {0}.'.format(uid))
	
	if code != true_code:
		redis.hincrby(uid, ATTEMPTS_FIELD, 1)
		return False

	redis.delete(uid)
	response.delete_cookie(COOKIE_NAME)
	return True