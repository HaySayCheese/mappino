import datetime
from django.conf import settings


def set_cookie(response, key, value, seconds_expire=None):
	if seconds_expire is None:
		seconds_expire = 365 * 24 * 60 * 60 # one year

	expires = datetime.datetime.strftime(
		datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds_expire), "%a, %d-%b-%Y %H:%M:%S GMT")
	response.set_cookie(
		key, value, max_age=seconds_expire, expires=expires,
		domain=settings.SESSION_COOKIE_DOMAIN,
		secure=settings.SESSION_COOKIE_SECURE or None
	)


def set_signed_cookie(response, key, value, salt='', seconds_expire=None, http_only=True):
	if seconds_expire is None:
		seconds_expire = 365 * 24 * 60 * 60 # one year

	expires = datetime.datetime.strftime(
		datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds_expire), "%a, %d-%b-%Y %H:%M:%S GMT")
	response.set_signed_cookie(
		key, value, salt, max_age=seconds_expire, expires=expires,
		domain=settings.SESSION_COOKIE_DOMAIN,
		secure=settings.SESSION_COOKIE_SECURE or None,
		httponly=http_only
	)