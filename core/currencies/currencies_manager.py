#coding=utf-8
from core.currencies.constants import CURRENCIES


DOL = 9.500
EUR = 13.300

def convert(price, currency, destination_currency):
	price = float(price)

	# Приводимо в гривню
	if currency == CURRENCIES.dol():
		price *= DOL
	elif currency == CURRENCIES.eur():
		price *= EUR

	# Приводимо в бажану валюту
	if destination_currency == CURRENCIES.uah():
		return price
	elif destination_currency == CURRENCIES.dol():
		return price / DOL
	elif destination_currency == CURRENCIES.eur():
		return price / EUR