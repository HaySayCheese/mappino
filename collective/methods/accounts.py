#coding=utf-8
from django.contrib.auth import authenticate, login
from django.core.cache import get_cache, InvalidCacheBackendError
from collective.methods.request_data_getters import POST_parameter


class BruteForceException(Exception):
	pass

class InvalidOrInactiveAccount(Exception):
	pass

class NotAllowed(Exception):
	pass




def process_authorisation(request):
	MAX_LOGIN_ATTEMPTS = 5
	SESSION_KEY = 'at_cnt'
	CACHE_KEY   = SESSION_KEY + request.META.get('REMOTE_ADDR')


	def set_login_attempts_count(request, value):
		try:
			cache = get_cache('accounts')
			cache.set(CACHE_KEY, value)
		except InvalidCacheBackendError:
			request.session[SESSION_KEY] = value


	def inc_login_attempts_count(request):
		try:
			cache = get_cache('accounts')
			count = cache.get(CACHE_KEY, None)
		except InvalidCacheBackendError:
			count = request.session.get(SESSION_KEY, None)

		if count is None:
			set_login_attempts_count(request, 1)
		else:
			set_login_attempts_count(request, count + 1)



	def login_attempts_count(request):
		try:
			cache = get_cache('accounts')
			count = cache.get(CACHE_KEY, None)
		except InvalidCacheBackendError:
			count = request.session.get(SESSION_KEY, None)

		if count is None:
			set_login_attempts_count(request, 0)
			return 0
		return count



	# Попередження brute-force шляхом підрахунку кількості спроб авторизації.
	# Якщо кількість спроб перевищує MAX_LOGIN_ATTEMPTS - згенерує виключення BruteForceException
	attempts_count = login_attempts_count(request)
	if attempts_count >= MAX_LOGIN_ATTEMPTS:
		raise BruteForceException


	# Перевірка параметрів
	try:
		username = POST_parameter(request, 'login')
		password = POST_parameter(request, 'password')
	except ValueError:
		raise ValueError('Username or password is invalid or absent.')

	# Авторизація
	user = authenticate(username=username, password=password)
	if (user is None) or (user.is_active == False):
		inc_login_attempts_count(request)
		raise InvalidOrInactiveAccount

	if (not user.is_staff) or (user.is_superuser == False):
		inc_login_attempts_count(request)
		raise NotAllowed

	login(request, user)
	request.session.set_expiry(60 * 60 * 5)
	set_login_attempts_count(request, 0)