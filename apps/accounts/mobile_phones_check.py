#coding=utf-8
import random
import string
from collective.http.cookies import set_signed_cookie
from mappino.wsgi import redis_connections


redis = redis_connections[1]


COOKIE_NAME = 'mcheck'
COOKIE_SALT = 'JMH2FWWYa1ogCJR0gW4z'

REDIS_HASH_PREFIX = 'mcheck_'
CODE_FIELD = 'code'
ATTEMPTS_FIELD = 'attempts'
PHONE_FIELD = 'phone'
PASSWORD_FIELD = 'pass'

MAX_ATTEMPTS_COUNT = 3
CODE_TTL = 60*60*2 # 2 hours


def is_number_check_started(request):
	# todo: додати тротлінг iр-адреси
	if COOKIE_NAME in request.COOKIES:
		return True
	else:
		return False


def start_number_check(phone, password, response):
	# generate uid avoiding duplicates
	uid_length = 32
	uid = ''.join(random.choice(string.uppercase + string.lowercase + string.digits) for x in range(uid_length))
	while redis.exists(uid):
		uid = ''.join(random.choice(string.uppercase + string.lowercase + string.digits) for x in range(uid_length))
	key = REDIS_HASH_PREFIX + uid

	pipe = redis.pipeline()
	pipe.hset(key, CODE_FIELD, int(''.join(random.choice(string.digits) for x in range(6))))
	pipe.hset(key, ATTEMPTS_FIELD, 1)
	pipe.hset(key, PHONE_FIELD, phone)
	pipe.hset(key, PASSWORD_FIELD, password)
	pipe.expire(key, CODE_TTL)
	pipe.execute()

	set_signed_cookie(response, COOKIE_NAME, uid, salt=COOKIE_SALT, days_expire=1, http_only=False)

	# send SMS
	# todo: send sms here
	# todo: додати перевірку на дотримання часового інтервалу до повторної SMS
	# todo: додати обмеження на к-сть SMS в день
	# todo: додати обмеження на к-сть SMS на одну ip-адресу.


def check_code(code, request, response):
	uid = request.get_signed_cookie(COOKIE_NAME, salt=COOKIE_SALT)
	key = REDIS_HASH_PREFIX + uid

	if not redis.exists(key):
		response.delete_cookie(COOKIE_NAME)
		raise KeyError('{0} is not in redis database.'.format(key))

	attempts_count = redis.hget(key, ATTEMPTS_FIELD)
	if attempts_count is None:
		response.delete_cookie(COOKIE_NAME)
		raise KeyError('field @attempts is not in hash {0}.'.format(key))

	attempts_count = int(attempts_count)
	if attempts_count >= MAX_ATTEMPTS_COUNT:
		response.delete_cookie(COOKIE_NAME)
		redis.delete(key)
		return False, {'attempts': attempts_count + 1}

	true_code = redis.hget(key, CODE_FIELD)
	if true_code is None:
		response.delete_cookie(COOKIE_NAME)
		redis.delete(key)
		raise KeyError('field @code is not in hash {0}.'.format(key))
	
	if code != true_code:
		redis.hincrby(key, ATTEMPTS_FIELD, 1)
		return False, {'attempts': attempts_count + 1}


	user_data = {
		'phone': redis.hget(key, PHONE_FIELD),
	    'password': redis.hget(key, PASSWORD_FIELD),
	}
	redis.delete(key)
	response.delete_cookie(COOKIE_NAME)
	return True, user_data