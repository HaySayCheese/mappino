#coding=utf-8


OPERATION_SID_SALE = 0
OPERATION_SID_RENT = 1


def __house_sale_filters(request):
	filters = {
		'for_sale': True
	}

	if 'price_from' in request.GET:
		filters['price_from'] = int(request.GET['price_from'])
	if 'price_to' in request.GET:
		filters['price_to'] = int(request.GET['price_to'])
	if 'currency_sid' in request.GET:
		filters['currency_sid'] = int(request.GET['currency_sid'])


	if 'new_buildings' in request.GET:
		filters['new_buildings'] = True
	if 'secondary_market' in request.GET:
		filters['secondary_market'] = True


	if 'total_area_from' in request.GET:
		filters['total_area_from'] = int(request.GET['total_area_from'])
	if 'total_area_to' in request.GET:
		filters['total_area_to'] = int(request.GET['total_area_to'])


	if 'rooms_count_from' in request.GET:
		filters['rooms_count_from'] = int(request.GET['rooms_count_from'])
	if 'rooms_count_to' in request.GET:
		filters['rooms_count_to'] = int(request.GET['rooms_count_to'])


	if 'floors_count_from' in request.GET:
		filters['floors_count_from'] = int(request.GET['floors_count_from'])
	if 'floors_count_to' in request.GET:
		filters['floors_count_to'] = int(request.GET['floors_count_to'])


	if 'electricity' in request.GET:
		filters['electricity'] = True
	if 'gas' in request.GET:
		filters['gas'] = True
	if 'hot_water' in request.GET:
		filters['hot_water'] = True
	if 'cold_water' in request.GET:
		filters['cold_water'] = True
	if 'sewerage' in request.GET:
		filters['sewerage'] = True
	if 'heating_type_sid' in request.GET:
		filters['heating_type_sid'] = int(request.GET['heating_type_sid'])
	return filters


def __house_rent_filters(request):
	filters = {
		'for_rent': True
	}

	if 'period_sid' in request.GET:
		filters['period_sid'] = int(request.GET['period_sid'])
	if 'price_from' in request.GET:
		filters['price_from'] = int(request.GET['price_from'])
	if 'price_to' in request.GET:
		filters['price_to'] = int(request.GET['price_to'])
	if 'currency_sid' in request.GET:
		filters['currency_sid'] = int(request.GET['currency_sid'])


	if 'persons_count_from' in request.GET:
		filters['persons_count_from'] = int(request.GET['persons_count_from'])
	if 'persons_count_to' in request.GET:
		filters['persons_count_to'] = int(request.GET['persons_count_to'])


	if 'total_area_from' in request.GET:
		filters['total_area_from'] = int(request.GET['total_area_from'])
	if 'total_area_to' in request.GET:
		filters['total_area_to'] = int(request.GET['total_area_to'])


	if 'family' in request.GET:
		filters['family'] = True
	if 'foreigners' in request.GET:
		filters['foreigners'] = True


	if 'electricity' in request.GET:
		filters['electricity'] = True
	if 'gas' in request.GET:
		filters['gas'] = True
	if 'hot_water' in request.GET:
		filters['hot_water'] = True
	if 'cold_water' in request.GET:
		filters['cold_water'] = True
	return filters


def __flats_sale_filters(request):
	filters = {
		'for_sale': True
	}

	if 'price_from' in request.GET:
		filters['price_from'] = int(request.GET['price_from'])
	if 'price_to' in request.GET:
		filters['price_to'] = int(request.GET['price_to'])
	if 'currency_sid' in request.GET:
		filters['currency_sid'] = int(request.GET['currency_sid'])


	if 'new_buildings' in request.GET:
		filters['new_buildings'] = True
	if 'secondary_market' in request.GET:
		filters['secondary_market'] = True


	if 'rooms_count_from' in request.GET:
		filters['rooms_count_from'] = int(request.GET['rooms_count_from'])
	if 'rooms_count_to' in request.GET:
		filters['rooms_count_to'] = int(request.GET['rooms_count_to'])


	if 'total_area_from' in request.GET:
		filters['total_area_from'] = int(request.GET['total_area_from'])
	if 'total_area_to' in request.GET:
		filters['total_area_to'] = int(request.GET['total_area_to'])


	if 'floor_from' in request.GET:
		filters['floor_from'] = int(request.GET['floor_from'])
	if 'floor_to' in request.GET:
		filters['floor_to'] = int(request.GET['floor_to'])
	if 'mansard' in request.GET:
		filters['mansard'] = True
	if 'ground' in request.GET:
		filters['ground'] = True


	if 'planning_sid' in request.GET: # планировка комнат
		filters['planning_sid'] = int(request.GET['planning_sid'])


	if 'lift' in request.GET:
		filters['lift'] = True
	if 'electricity' in request.GET:
		filters['electricity'] = True
	if 'gas' in request.GET:
		filters['gas'] = True
	if 'hot_water' in request.GET:
		filters['hot_water'] = True
	if 'cold_water' in request.GET:
		filters['cold_water'] = True
	if 'heating_type_sid' in request.GET:
		filters['heating_type_sid'] = int(request.GET['heating_type_sid'])
	return filters


def __flat_rent_filters(request):
	filters = {
		'for_rent': True
	}

	if 'period_sid' in request.GET:
		filters['period_sid'] = int(request.GET['period_sid'])
	if 'price_from' in request.GET:
		filters['price_from'] = int(request.GET['price_from'])
	if 'price_to' in request.GET:
		filters['price_to'] = int(request.GET['price_to'])
	if 'currency_sid' in request.GET:
		filters['currency_sid'] = int(request.GET['currency_sid'])


	if 'total_area_from' in request.GET:
		filters['total_area_from'] = int(request.GET['total_area_from'])
	if 'total_area_to' in request.GET:
		filters['total_area_to'] = int(request.GET['total_area_to'])


	if 'floor_from' in request.GET:
		filters['floor_from'] = int(request.GET['floor_from'])
	if 'floor_to' in request.GET:
		filters['floor_to'] = int(request.GET['floor_to'])
	if 'mansard' in request.GET:
		filters['mansard'] = True
	if 'ground' in request.GET:
		filters['ground'] = True


	if 'persons_count_from' in request.GET:
		filters['persons_count_from'] = int(request.GET['persons_count_from'])
	if 'persons_count_to' in request.GET:
		filters['persons_count_to'] = int(request.GET['persons_count_to'])


	if 'family' in request.GET:
		filters['family'] = True
	if 'foreigners' in request.GET:
		filters['foreigners'] = True


	if 'lift' in request.GET:
		filters['lift'] = True
	if 'electricity' in request.GET:
		filters['electricity'] = True
	if 'gas' in request.GET:
		filters['gas'] = True
	if 'hot_water' in request.GET:
		filters['hot_water'] = True
	if 'cold_water' in request.GET:
		filters['cold_water'] = True
	return filters


# def __apartments_sale_filters(request):
# 	filters = {
# 		'for_sale': True
# 	}
#
# 	if 'price_from' in request.GET:
# 		filters['price_from'] = int(request.GET['price_from'])
# 	if 'price_to' in request.GET:
# 		filters['price_to'] = int(request.GET['price_to'])
# 	if 'currency_sid' in request.GET:
# 		filters['currency_sid'] = int(request.GET['currency_sid'])
#
#
# 	if 'new_buildings' in request.GET:
# 		filters['new_buildings'] = True
# 	if 'secondary_market' in request.GET:
# 		filters['secondary_market'] = True
#
#
# 	if 'rooms_count_from' in request.GET:
# 		filters['rooms_count_from'] = int(request.GET['rooms_count_from'])
# 	if 'rooms_count_to' in request.GET:
# 		filters['rooms_count_to'] = int(request.GET['rooms_count_to'])
#
#
# 	if 'mansard' in request.GET:
# 		filters['mansard'] = True
# 	if 'ground' in request.GET:
# 		filters['ground'] = True
#
#
# 	if 'total_area_from' in request.GET:
# 		filters['total_area_from'] = int(request.GET['total_area_from'])
# 	if 'total_area_to' in request.GET:
# 		filters['total_area_to'] = int(request.GET['total_area_to'])
#
#
# 	if 'floor_from' in request.GET:
# 		filters['floor_from'] = int(request.GET['floor_from'])
# 	if 'floor_to' in request.GET:
# 		filters['floor_to'] = int(request.GET['floor_to'])
#
#
# 	if 'planning_sid' in request.GET: # планировка комнат
# 		filters['planning_sid'] = int(request.GET['planning_sid'])
#
#
# 	if 'lift' in request.GET:
# 		filters['lift'] = True
# 	if 'electricity' in request.GET:
# 		filters['electricity'] = True
# 	if 'gas' in request.GET:
# 		filters['gas'] = True
# 	if 'hot_water' in request.GET:
# 		filters['hot_water'] = True
# 	if 'cold_water' in request.GET:
# 		filters['cold_water'] = True
# 	if 'heating_type_sid' in request.GET:
# 		filters['heating_type_sid'] = int(request.GET['heating_type_sid'])
# 	return filters
#
#
# def __apartments_rent_filters(request):
# 	filters = {
# 		'for_rent': True
# 	}
#
# 	if 'period_sid' in request.GET:
# 		filters['period_sid'] = int(request.GET['period_sid'])
# 	if 'price_from' in request.GET:
# 		filters['price_from'] = int(request.GET['price_from'])
# 	if 'price_to' in request.GET:
# 		filters['price_to'] = int(request.GET['price_to'])
# 	if 'currency_sid' in request.GET:
# 		filters['currency_sid'] = int(request.GET['currency_sid'])
#
#
# 	if 'persons_count_from' in request.GET:
# 		filters['persons_count_from'] = int(request.GET['persons_count_from'])
# 	if 'persons_count_to' in request.GET:
# 		filters['persons_count_to'] = int(request.GET['persons_count_to'])
#
#
# 	if 'total_area_from' in request.GET:
# 		filters['total_area_from'] = int(request.GET['total_area_from'])
# 	if 'total_area_to' in request.GET:
# 		filters['total_area_to'] = int(request.GET['total_area_to'])
#
#
# 	if 'floor_from' in request.GET:
# 		filters['floor_from'] = int(request.GET['floor_from'])
# 	if 'floor_to' in request.GET:
# 		filters['floor_to'] = int(request.GET['floor_to'])
#
#
# 	if 'mansard' in request.GET:
# 		filters['mansard'] = True
# 	if 'ground' in request.GET:
# 		filters['ground'] = True
#
#
# 	if 'family' in request.GET:
# 		filters['family'] = True
# 	if 'foreigners' in request.GET:
# 		filters['foreigners'] = True
#
#
# 	if 'lift' in request.GET:
# 		filters['lift'] = True
# 	if 'electricity' in request.GET:
# 		filters['electricity'] = True
# 	if 'gas' in request.GET:
# 		filters['gas'] = True
# 	if 'hot_water' in request.GET:
# 		filters['hot_water'] = True
# 	if 'cold_water' in request.GET:
# 		filters['cold_water'] = True
# 	return filters


# def __cottage_sale_filters(request):
# 	filters = {
# 		'for_sale': True
# 	}
#
# 	if 'price_from' in request.GET:
# 		filters['price_from'] = int(request.GET['price_from'])
# 	if 'price_to' in request.GET:
# 		filters['price_to'] = int(request.GET['price_to'])
# 	if 'currency_sid' in request.GET:
# 		filters['currency_sid'] = int(request.GET['currency_sid'])
#
#
# 	if 'new_buildings' in request.GET:
# 		filters['new_buildings'] = True
# 	if 'secondary_market' in request.GET:
# 		filters['secondary_market'] = True
#
#
# 	if 'rooms_count_from' in request.GET:
# 		filters['rooms_count_from'] = int(request.GET['rooms_count_from'])
# 	if 'rooms_count_to' in request.GET:
# 		filters['rooms_count_to'] = int(request.GET['rooms_count_to'])
#
#
# 	if 'floors_count_from' in request.GET:
# 		filters['floors_count_from'] = int(request.GET['floors_count_from'])
# 	if 'floors_count_to' in request.GET:
# 		filters['floors_count_to'] = int(request.GET['floors_count_to'])
#
#
# 	if 'electricity' in request.GET:
# 		filters['electricity'] = True
# 	if 'gas' in request.GET:
# 		filters['gas'] = True
# 	if 'hot_water' in request.GET:
# 		filters['hot_water'] = True
# 	if 'cold_water' in request.GET:
# 		filters['cold_water'] = True
# 	if 'sewerage' in request.GET:
# 		filters['sewerage'] = True
# 	if 'heating_type_sid' in request.GET:
# 		filters['heating_type_sid'] = int(request.GET['heating_type_sid'])
# 	return filters
#
#
# def __cottage_rent_filters(request):
# 	filters = {
# 		'for_rent': True
# 	}
#
# 	if 'period_sid' in request.GET:
# 		filters['period_sid'] = int(request.GET['period_sid'])
# 	if 'price_from' in request.GET:
# 		filters['price_from'] = int(request.GET['price_from'])
# 	if 'price_to' in request.GET:
# 		filters['price_to'] = int(request.GET['price_to'])
# 	if 'currency_sid' in request.GET:
# 		filters['currency_sid'] = int(request.GET['currency_sid'])
#
#
# 	if 'persons_count_from' in request.GET:
# 		filters['persons_count_from'] = int(request.GET['persons_count_from'])
# 	if 'persons_count_to' in request.GET:
# 		filters['persons_count_to'] = int(request.GET['persons_count_to'])
#
#
# 	if 'family' in request.GET:
# 		filters['family'] = True
# 	if 'foreigners' in request.GET:
# 		filters['foreigners'] = True
#
#
# 	if 'electricity' in request.GET:
# 		filters['electricity'] = True
# 	if 'gas' in request.GET:
# 		filters['gas'] = True
# 	if 'hot_water' in request.GET:
# 		filters['hot_water'] = True
# 	if 'cold_water' in request.GET:
# 		filters['cold_water'] = True
# 	return filters


def __rooms_sale_filters(request):
	filters = {
		'for_sale': True
	}

	if 'price_from' in request.GET:
		filters['price_from'] = int(request.GET['price_from'])
	if 'price_to' in request.GET:
		filters['price_to'] = int(request.GET['price_to'])
	if 'currency_sid' in request.GET:
		filters['currency_sid'] = int(request.GET['currency_sid'])


	if 'new_buildings' in request.GET:
		filters['new_buildings'] = True
	if 'secondary_market' in request.GET:
		filters['secondary_market'] = True


	if 'rooms_count_from' in request.GET:
		filters['rooms_count_from'] = int(request.GET['rooms_count_from'])
	if 'rooms_count_to' in request.GET:
		filters['rooms_count_to'] = int(request.GET['rooms_count_to'])


	if 'total_area_from' in request.GET:
		filters['total_area_from'] = int(request.GET['total_area_from'])
	if 'total_area_to' in request.GET:
		filters['total_area_to'] = int(request.GET['total_area_to'])


	if 'floor_from' in request.GET:
		filters['floor_from'] = int(request.GET['floor_from'])
	if 'floor_to' in request.GET:
		filters['floor_to'] = int(request.GET['floor_to'])


	if 'mansard' in request.GET:
		filters['mansard'] = True
	if 'ground' in request.GET:
		filters['ground'] = True


	if 'planning_sid' in request.GET: # планировка комнат
		filters['planning_sid'] = int(request.GET['planning_sid'])


	if 'lift' in request.GET:
		filters['lift'] = True
	if 'electricity' in request.GET:
		filters['electricity'] = True
	if 'gas' in request.GET:
		filters['gas'] = True
	if 'hot_water' in request.GET:
		filters['hot_water'] = True
	if 'cold_water' in request.GET:
		filters['cold_water'] = True
	if 'heating_type_sid' in request.GET:
		filters['heating_type_sid'] = int(request.GET['heating_type_sid'])
	return filters


def __rooms_rent_filters(request):
	filters = {
		'for_rent': True
	}

	if 'period_sid' in request.GET:
		filters['period_sid'] = int(request.GET['period_sid'])
	if 'price_from' in request.GET:
		filters['price_from'] = int(request.GET['price_from'])
	if 'price_to' in request.GET:
		filters['price_to'] = int(request.GET['price_to'])
	if 'currency_sid' in request.GET:
		filters['currency_sid'] = int(request.GET['currency_sid'])


	if 'persons_count_from' in request.GET:
		filters['persons_count_from'] = int(request.GET['persons_count_from'])
	if 'persons_count_to' in request.GET:
		filters['persons_count_to'] = int(request.GET['persons_count_to'])


	if 'total_area_from' in request.GET:
		filters['total_area_from'] = int(request.GET['total_area_from'])
	if 'total_area_to' in request.GET:
		filters['total_area_to'] = int(request.GET['total_area_to'])


	if 'floor_from' in request.GET:
		filters['floor_from'] = int(request.GET['floor_from'])
	if 'floor_to' in request.GET:
		filters['floor_to'] = int(request.GET['floor_to'])


	if 'mansard' in request.GET:
		filters['mansard'] = True
	if 'ground' in request.GET:
		filters['ground'] = True


	if 'family' in request.GET:
		filters['family'] = True
	if 'foreigners' in request.GET:
		filters['foreigners'] = True


	if 'lift' in request.GET:
		filters['lift'] = True
	if 'electricity' in request.GET:
		filters['electricity'] = True
	if 'gas' in request.GET:
		filters['gas'] = True
	if 'hot_water' in request.GET:
		filters['hot_water'] = True
	if 'cold_water' in request.GET:
		filters['cold_water'] = True
	return filters


def parse_houses_filters(request):
	"""
	Формує об’єкт фільтрів із параметрів, переданих в запиті.
	WARNING:
		Виконує тільки базові перевірки відповідності типів,
		але не перевіряє передані фільтри з точки зору коректності структур даних
		чи взаємопов’язаності. Дані перевірки відводиться функції фільтрування,
		яка в даному випадку виступає інформаційним експертом.
	"""
	operation_sid = int(request.GET['operation_sid']) # required
	if operation_sid == 0:
		return __house_sale_filters(request)
	elif operation_sid == 1:
		return __house_rent_filters(request)
	else:
		raise ValueError('Invalid operation_sid.')


def parse_flats_filters(request):
	"""
	Формує об’єкт фільтрів із параметрів, переданих в запиті.
	WARNING:
		Виконує тільки базові перевірки відповідності типів,
		але не перевіряє передані фільтри з точки зору коректності структур даних
		чи взаємопов’язаності. Дані перевірки відводиться функції фільтрування,
		яка в даному випадку виступає інформаційним експертом.
	"""
	operation_sid = int(request.GET['operation_sid']) # required
	if operation_sid == 0:
		return __flats_sale_filters(request)
	elif operation_sid == 1:
		return __flat_rent_filters(request)
	else:
		raise ValueError('Invalid operation_sid.')


# def parse_apartments_filters(request):
# 	"""
# 	Формує об’єкт фільтрів із параметрів, переданих в запиті.
# 	WARNING:
# 		Виконує тільки базові перевірки відповідності типів,
# 		але не перевіряє передані фільтри з точки зору коректності структур даних
# 		чи взаємопов’язаності. Дані перевірки відводиться функції фільтрування,
# 		яка в даному випадку виступає інформаційним експертом.
# 	"""
# 	operation_sid = int(request.GET['operation_sid']) # required
# 	if operation_sid == 0:
# 		return __apartments_sale_filters(request)
# 	elif operation_sid == 1:
# 		return __apartments_rent_filters(request)
# 	else:
# 		raise ValueError('Invalid operation_sid.')


# def parse_cottages_filters(request):
# 	"""
# 	Формує об’єкт фільтрів із параметрів, переданих в запиті.
# 	WARNING:
# 		Виконує тільки базові перевірки відповідності типів,
# 		але не перевіряє передані фільтри з точки зору коректності структур даних
# 		чи взаємопов’язаності. Дані перевірки відводиться функції фільтрування,
# 		яка в даному випадку виступає інформаційним експертом.
# 	"""
# 	operation_sid = int(request.GET['operation_sid']) # required
# 	if operation_sid == 0:
# 		return __cottage_sale_filters(request)
# 	elif operation_sid == 1:
# 		return __cottage_rent_filters(request)
# 	else:
# 		raise ValueError('Invalid operation_sid.')


def parse_rooms_filters(request):
	"""
	Формує об’єкт фільтрів із параметрів, переданих в запиті.
	WARNING:
		Виконує тільки базові перевірки відповідності типів,
		але не перевіряє передані фільтри з точки зору коректності структур даних
		чи взаємопов’язаності. Дані перевірки відводиться функції фільтрування,
		яка в даному випадку виступає інформаційним експертом.
	"""
	operation_sid = int(request.GET['operation_sid']) # required
	if operation_sid == 0:
		return __rooms_sale_filters(request)
	elif operation_sid == 1:
		return __rooms_rent_filters(request)
	else:
		raise ValueError('Invalid operation_sid.')


def parse_trades_filters(request):
	"""
	Формує об’єкт фільтрів із параметрів, переданих в запиті.
	WARNING:
		Виконує тільки базові перевірки відповідності типів,
		але не перевіряє передані фільтри з точки зору коректності структур даних
		чи взаємопов’язаності. Дані перевірки відводиться функції фільтрування,
		яка в даному випадку виступає інформаційним експертом.
	"""
	filters = {}
	if int(request.GET['operation_sid']) == OPERATION_SID_SALE:
		filters['for_sale'] = True
	if int(request.GET['operation_sid']) == OPERATION_SID_RENT:
		filters['for_rent'] = True


	if 'price_from' in request.GET:
		filters['price_from'] = int(request.GET['price_from'])
	if 'price_to' in request.GET:
		filters['price_to'] = int(request.GET['price_to'])
	if 'currency_sid' in request.GET:
		filters['currency_sid'] = int(request.GET['currency_sid'])


	if 'new_buildings' in request.GET:
		filters['new_buildings'] = True
	if 'secondary_market' in request.GET:
		filters['secondary_market'] = True


	if 'halls_area_from' in request.GET:
		filters['halls_area_from'] = int(request.GET['halls_area_from'])
	if 'halls_area_to' in request.GET:
		filters['halls_area_to'] = int(request.GET['halls_area_to'])


	if 'total_area_from' in request.GET:
		filters['total_area_from'] = int(request.GET['total_area_from'])
	if 'total_area_to' in request.GET:
		filters['total_area_to'] = int(request.GET['total_area_to'])


	if 'building_type_sid' in request.GET: # тип будинку
		filters['building_type_sid'] = int(request.GET['building_type_sid'])


	if 'electricity' in request.GET:
		filters['electricity'] = True
	if 'gas' in request.GET:
		filters['gas'] = True
	if 'hot_water' in request.GET:
		filters['hot_water'] = True
	if 'cold_water' in request.GET:
		filters['cold_water'] = True

	# todo: визначитись чи потрібно це поле у фільтрах
	if 'sewerage' in request.GET:
		filters['sewerage'] = True
	return filters


def parse_offices_filters(request):
	"""
	Формує об’єкт фільтрів із параметрів, переданих в запиті.
	WARNING:
		Виконує тільки базові перевірки відповідності типів,
		але не перевіряє передані фільтри з точки зору коректності структур даних
		чи взаємопов’язаності. Дані перевірки відводиться функції фільтрування,
		яка в даному випадку виступає інформаційним експертом.
	"""
	filters = {}
	if int(request.GET['operation_sid']) == OPERATION_SID_SALE:
		filters['for_sale'] = True
	if int(request.GET['operation_sid']) == OPERATION_SID_RENT:
		filters['for_rent'] = True


	if 'price_from' in request.GET:
		filters['price_from'] = int(request.GET['price_from'])
	if 'price_to' in request.GET:
		filters['price_to'] = int(request.GET['price_to'])
	if 'currency_sid' in request.GET:
		filters['currency_sid'] = int(request.GET['currency_sid'])


	if 'new_buildings' in request.GET:
		filters['new_buildings'] = True
	if 'secondary_market' in request.GET:
		filters['secondary_market'] = True

	if 'total_area_from' in request.GET:
		filters['total_area_from'] = int(request.GET['total_area_from'])
	if 'total_area_to' in request.GET:
		filters['total_area_to'] = int(request.GET['total_area_to'])


	if 'cabinets_count_from' in request.GET:
		filters['cabinets_count_from'] = int(request.GET['cabinets_count_from'])
	if 'cabinets_count_to' in request.GET:
		filters['cabinets_count_to'] = int(request.GET['cabinets_count_to'])


	if 'security' in request.GET:
		filters['security'] = True
	if 'kitchen' in request.GET:
		filters['kitchen'] = True
	if 'hot_water' in request.GET:
		filters['hot_water'] = True
	if 'cold_water' in request.GET:
		filters['cold_water'] = True
	return filters


def parse_warehouses_filters(request):
	"""
	Формує об’єкт фільтрів із параметрів, переданих в запиті.
	WARNING:
		Виконує тільки базові перевірки відповідності типів,
		але не перевіряє передані фільтри з точки зору коректності структур даних
		чи взаємопов’язаності. Дані перевірки відводиться функції фільтрування,
		яка в даному випадку виступає інформаційним експертом.
	"""
	filters = {}
	if int(request.GET['operation_sid']) == OPERATION_SID_SALE:
		filters['for_sale'] = True
	if int(request.GET['operation_sid']) == OPERATION_SID_RENT:
		filters['for_rent'] = True


	if 'price_from' in request.GET:
		filters['price_from'] = int(request.GET['price_from'])
	if 'price_to' in request.GET:
		filters['price_to'] = int(request.GET['price_to'])
	if 'currency_sid' in request.GET:
		filters['currency_sid'] = int(request.GET['currency_sid'])


	if 'new_buildings' in request.GET:
		filters['new_buildings'] = True
	if 'secondary_market' in request.GET:
		filters['secondary_market'] = True


	if 'halls_area_from' in request.GET:
		filters['halls_area_from'] = int(request.GET['halls_area_from'])
	if 'halls_area_to' in request.GET:
		filters['halls_area_to'] = int(request.GET['halls_area_to'])


	if 'electricity' in request.GET:
		filters['electricity'] = True
	if 'gas' in request.GET:
		filters['gas'] = True
	if 'hot_water' in request.GET:
		filters['hot_water'] = True
	if 'cold_water' in request.GET:
		filters['cold_water'] = True
	if 'security_alarm' in request.GET:
		filters['security_alarm'] = True
	if 'fire_alarm' in request.GET:
		filters['fire_alarm'] = True

	# todo: розглянути можливість додання фільтру "охорона"
	#if 'security' in request.GET:
	#	filters['security'] = True
	return filters


def parse_businesses_filters(request):
	"""
	Формує об’єкт фільтрів із параметрів, переданих в запиті.
	WARNING:
		Виконує тільки базові перевірки відповідності типів,
		але не перевіряє передані фільтри з точки зору коректності структур даних
		чи взаємопов’язаності. Дані перевірки відводиться функції фільтрування,
		яка в даному випадку виступає інформаційним експертом.
	"""
	filters = {}
	if int(request.GET['operation_sid']) == OPERATION_SID_SALE:
		filters['for_sale'] = True
	if int(request.GET['operation_sid']) == OPERATION_SID_RENT:
		filters['for_rent'] = True


	if 'price_from' in request.GET:
		filters['price_from'] = int(request.GET['price_from'])
	if 'price_to' in request.GET:
		filters['price_to'] = int(request.GET['price_to'])
	if 'currency_sid' in request.GET:
		filters['currency_sid'] = int(request.GET['currency_sid'])


	if 'new_buildings' in request.GET:
		filters['new_buildings'] = True
	if 'secondary_market' in request.GET:
		filters['secondary_market'] = True
	return filters


def parse_caterings_filters(request):
	"""
	Формує об’єкт фільтрів із параметрів, переданих в запиті.
	WARNING:
		Виконує тільки базові перевірки відповідності типів,
		але не перевіряє передані фільтри з точки зору коректності структур даних
		чи взаємопов’язаності. Дані перевірки відводиться функції фільтрування,
		яка в даному випадку виступає інформаційним експертом.
	"""
	filters = {
		'operation_sid': int(request.GET['operation_sid']) # required
	}

	if 'price_from' in request.GET:
		filters['price_from'] = int(request.GET['price_from'])
	if 'price_to' in request.GET:
		filters['price_to'] = int(request.GET['price_to'])
	if 'currency_sid' in request.GET:
		filters['currency_sid'] = int(request.GET['currency_sid'])


	if 'new_buildings' in request.GET:
		filters['new_buildings'] = True
	if 'secondary_market' in request.GET:
		filters['secondary_market'] = True


	if 'total_area_from' in request.GET:
		filters['total_area_from'] = int(request.GET['total_area_from'])
	if 'total_area_to' in request.GET:
		filters['total_area_to'] = int(request.GET['total_area_to'])


	if 'halls_area_from' in request.GET:
		filters['halls_area_from'] = int(request.GET['halls_area_from'])
	if 'halls_area_to' in request.GET:
		filters['halls_area_to'] = int(request.GET['halls_area_to'])


	if 'halls_count_from' in request.GET:
		filters['halls_count_from'] = int(request.GET['halls_count_from'])
	if 'halls_count_to' in request.GET:
		filters['halls_count_to'] = int(request.GET['halls_count_to'])


	if 'building_type_sid' in request.GET: # тип будинку
		filters['building_type_sid'] = int(request.GET['building_type_sid'])


	if 'electricity' in request.GET:
		filters['electricity'] = True
	if 'gas' in request.GET:
		filters['gas'] = True
	if 'hot_water' in request.GET:
		filters['hot_water'] = True
	if 'cold_water' in request.GET:
		filters['cold_water'] = True
	return filters


def parse_garages_filters(request):
	"""
	Формує об’єкт фільтрів із параметрів, переданих в запиті.
	WARNING:
		Виконує тільки базові перевірки відповідності типів,
		але не перевіряє передані фільтри з точки зору коректності структур даних
		чи взаємопов’язаності. Дані перевірки відводиться функції фільтрування,
		яка в даному випадку виступає інформаційним експертом.
	"""
	filters = {}
	if int(request.GET['operation_sid']) == OPERATION_SID_SALE:
		filters['for_sale'] = True
	if int(request.GET['operation_sid']) == OPERATION_SID_RENT:
		filters['for_rent'] = True


	if 'price_from' in request.GET:
		filters['price_from'] = int(request.GET['price_from'])
	if 'price_to' in request.GET:
		filters['price_to'] = int(request.GET['price_to'])
	if 'currency_sid' in request.GET:
		filters['currency_sid'] = int(request.GET['currency_sid'])


	if 'total_area_from' in request.GET:
		filters['total_area_from'] = int(request.GET['total_area_from'])
	if 'total_area_to' in request.GET:
		filters['total_area_to'] = int(request.GET['total_area_to'])


	if 'ceiling_height_from' in request.GET:
		filters['ceiling_height_from'] = int(request.GET['ceiling_height_from'])
	if 'ceiling_height_to' in request.GET:
		filters['ceiling_height_to'] = int(request.GET['ceiling_height_to'])


	if 'pit' in request.GET:
		filters['pit'] = True
	return filters


def parse_lands_filters(request):
	"""
	Формує об’єкт фільтрів із параметрів, переданих в запиті.
	WARNING:
		Виконує тільки базові перевірки відповідності типів,
		але не перевіряє передані фільтри з точки зору коректності структур даних
		чи взаємопов’язаності. Дані перевірки відводиться функції фільтрування,
		яка в даному випадку виступає інформаційним експертом.
	"""
	filters = {}
	if int(request.GET['operation_sid']) == OPERATION_SID_SALE:
		filters['for_sale'] = True
	if int(request.GET['operation_sid']) == OPERATION_SID_RENT:
		filters['for_rent'] = True


	if 'price_from' in request.GET:
		filters['price_from'] = int(request.GET['price_from'])
	if 'price_to' in request.GET:
		filters['price_to'] = int(request.GET['price_to'])
	if 'currency_sid' in request.GET:
		filters['currency_sid'] = int(request.GET['currency_sid'])


	if 'area_from' in request.GET:
		filters['area_from'] = int(request.GET['area_from'])
	if 'area_to' in request.GET:
		filters['area_to'] = int(request.GET['area_to'])


	if 'electricity' in request.GET:
		filters['electricity'] = True
	if 'gas' in request.GET:
		filters['gas'] = True
	if 'water' in request.GET:
		filters['water'] = True
	if 'sewerage' in request.GET:
		filters['sewerage'] = True
	return filters
