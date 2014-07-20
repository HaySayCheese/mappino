#coding=utf-8
import json
import urllib2
import xml.etree.ElementTree as ET

from datetime import timedelta
from django.utils.timezone import now

from collective.exceptions import RuntimeException
from core.currencies.constants import CURRENCIES
from mappino.wsgi import redis_connections


redis = redis_connections['cache']


def __grab_bank_api():
	"""
	Зграбить API приватбанку і поверне курси валют.

	:return:
		dict у форматі {'usd': 11.0, ...}
	"""

	currencies = {
		'usd': None,
	    'eur': None,
	}


	def grab():
		root = ET.fromstring(
			urllib2.urlopen("https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5").read())

		for row in root.findall('row'):
			record = row.find('exchangerate')
			ccy = record.attrib['ccy']
			if ccy == 'USD':
				currencies['usd'] = float(record.attrib['buy'])
			elif ccy == 'EUR':
				currencies['eur'] = float(record.attrib['buy'])


		# check
		for key, value in currencies.iteritems():
			if (value is None) or (value <= 0):
				raise RuntimeException('Bank API has responded incorrect.')

		return currencies


	try:
		return grab()
	except RuntimeException:
		return grab()






def __get_currencies():
	"""
	Перегляне кеш redis на наявність поточних курсів.
	Якщо їх там не виявиться — запитає їх в банку, закешує до 6ї години наступного дня і віддасть,
	інакше просто віддасть з кешу.

	:return:
		dict у форматі {'usd': 11.0, ...}
	"""

	key = 'currencies'
	currencies = redis.get(key)

	if currencies is None:
		currencies = __grab_bank_api()
		ttl = (now() - (now() + timedelta(days=1)).replace(hour=6, minute=0, second=0)).seconds
		redis.setex(key, ttl, json.dumps(currencies))
	else:
		currencies = json.loads(currencies)

	return currencies


def convert(price, currency, destination_currency):
	currencies = __get_currencies()
	price = float(price)

	# Приводимо в гривню
	if currency == CURRENCIES.dol():
		price *= currencies['usd']
	elif currency == CURRENCIES.eur():
		price *= currencies['eur']

	# Приводимо в бажану валюту
	if destination_currency == CURRENCIES.uah():
		return price
	elif destination_currency == CURRENCIES.dol():
		return price / currencies['usd']
	elif destination_currency == CURRENCIES.eur():
		return price / currencies['eur']
