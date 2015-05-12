#coding=utf-8
import time
import datetime

from django.conf import settings
from django.utils.timezone import now

from core import redis_connections


redis = redis_connections['cache']



def static_template_last_modified(*args):
	"""
	Завжди повертає один і той же unix-timestamp, згенерований на етапі першого запуску.
	Якщо раніше збереженого timestamp не виявиться — згенерує новий з now().

	Використовується як заміна etag для статичних шаблонів.
	nginx вирізає etag з відповідей, які підлягають стисканню gzip, тому доводиться використовувати last modified.

	DEBUG:
		в режимі debug завжди повертає now().

	:param *args:
		<ignored>

	:return:
		datetime
	"""

	if settings.DEBUG:
		return now()


	key = 'static_template_last_modified'

	timestamp = redis.get(key)
	if timestamp is None:
		timestamp = int(time.time())
		redis.set(key, timestamp)

	return datetime.datetime.fromtimestamp(int(timestamp))