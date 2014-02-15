#coding=utf-8
#todo: перевірити помилки в словах, які формують індекс
from core.publications.constants import CURRENCIES, SALE_TRANSACTION_TYPES, LIVING_RENT_PERIODS


def sale_terms_index_data(head):
	if not head.for_sale:
		return u''
	terms = head.sale_terms

	currency = u'UAH гривна гривен грн'
	if terms.currency_sid == CURRENCIES.dol():
		currency = u'DOL долларов доллар дол'
	elif terms.currency_sid == CURRENCIES.eur():
		currency = u'EURO EUR евро'

	transaction = u'за все, за весь объект'
	if terms.transaction_sid == SALE_TRANSACTION_TYPES.for_square_meter():
		transaction = u'за метр квадратный'

	is_contract = u''
	if terms.is_contract:
		is_contract = u'цена договорная'

	index_data = u'Продается {price} {currency} {transaction} {is_contract} {add_terms}'.format(
		price = unicode(terms.price) if terms.price else u'',
	    currency = currency,
	    transaction = transaction,
	    is_contract = is_contract,
	    add_terms = terms.add_terms if terms.add_terms is not None else u''
	)
	return index_data



def living_rent_terms_index_data(head):
	if not head.for_rent:
		return u''
	terms = head.rent_terms

	currency = u'UAH гривна гривен грн'
	if terms.currency_sid == CURRENCIES.dol():
		currency = u'DOL долларов доллар дол'
	elif terms.currency_sid == CURRENCIES.eur():
		currency = u'EURO EUR евро'

	is_contract = u''
	if terms.is_contract:
		is_contract = u'цена договорная'

	period = u'Помесячная оренда помесячно'
	if terms.period_sid == LIVING_RENT_PERIODS.daily():
		period = u'Посуточная оренда посуточная оплата посуточно'
	elif terms.period_sid == LIVING_RENT_PERIODS.long_period():
		period = u'Долгосрочная оренда'

	persons_count = u''
	if terms.persons_count is not None:
		persons_count = unicode(terms.persons_count)

	index_data = u'Сдается в аренду {price} {currency} {is_contract} {period} ' \
	             u'{persons_count} {for_family} {foreigners} {smoking} ' \
	             u'{pets} {add_terms}'.format(
		price = unicode(terms.price) if terms.price else u'',
	    currency = currency,
	    is_contract = is_contract,
	    period = period,
	    persons_count = persons_count,
	    for_family = u'подходит семей семъя детьми для детей семейный' if terms.family else u'',
	    foreigners = u'размещение иностранцев иностранцы разрешены' if terms.foreigners else u'',
	    smoking = u'курение разрешено курить курящих' if terms.smoking else u'',
	    pets = u'пытомцы домашние животные' if terms.pets else u'',
	    add_terms = terms.add_terms if terms.add_terms is not None else u''
	)
	return index_data