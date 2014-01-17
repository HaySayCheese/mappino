import datetime
from django.conf import settings


DEFAULT_COOKIE_AGE = 365 * 24 * 60 * 60 # one year


def set_cookie(response, key, value, days_expire=7):
  if days_expire is None:
    max_age = DEFAULT_COOKIE_AGE
  else:
    max_age = days_expire * 24 * 60 * 60

  expires = datetime.datetime.strftime(
	  datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
  response.set_cookie(
	  key, value, max_age=max_age, expires=expires,
	  domain=settings.SESSION_COOKIE_DOMAIN,
	  secure=settings.SESSION_COOKIE_SECURE or None
  )


def set_signed_cookie(response, key, value, salt='', days_expire=7, http_only=True):
  if days_expire is None:
    max_age = DEFAULT_COOKIE_AGE
  else:
    max_age = days_expire * 24 * 60 * 60

  expires = datetime.datetime.strftime(
	  datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
  response.set_signed_cookie(
	  key, value, salt, max_age=max_age, expires=expires,
	  domain=settings.SESSION_COOKIE_DOMAIN,
	  secure=settings.SESSION_COOKIE_SECURE or None,
      httponly=http_only
  )