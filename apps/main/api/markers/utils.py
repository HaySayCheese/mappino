#coding=utf-8
import exceptions


OPERATION_SID_SALE = 0
OPERATION_SID_RENT = 1


def __house_sale_filters(params):
    filters = {
        'for_sale': True
    }


    try:
        filters['price_from'] = int(params['price_from'])
    except KeyError:
        pass
    try:
        filters['price_to'] = int(params['price_to'])
    except KeyError:
        pass
    try:
        filters['currency_sid'] = int(params['currency_sid'])
    except KeyError:
        pass


    try:
        filters['rooms_count_from'] = int(params['rooms_count_from'])
    except KeyError:
        pass
    try:
        filters['rooms_count_to'] = int(params['rooms_count_to'])
    except KeyError:
        pass


    try:
        filters['floors_count_from'] = int(params['floors_count_from'])
    except KeyError:
        pass
    try:
        filters['floors_count_to'] = int(params['floors_count_to'])
    except KeyError:
        pass


    if 'new_buildings' in params:
        filters['new_buildings'] = True
    if 'secondary_market' in params:
        filters['secondary_market'] = True


    if 'electricity' in params:
        filters['electricity'] = True
    if 'gas' in params:
        filters['gas'] = True
    if 'hot_water' in params:
        filters['hot_water'] = True
    if 'cold_water' in params:
        filters['cold_water'] = True
    if 'sewerage' in params:
        filters['sewerage'] = True
    try:
        filters['heating_type_sid'] = int(params['heating_type_sid'])
    except KeyError:
        pass

    return filters


def __house_rent_filters(params):
    filters = {
        'for_rent': True
    }

    try:
        filters['period_sid'] = int(params['period_sid'])
    except KeyError:
        pass


    try:
        filters['price_from'] = int(params['price_from'])
    except KeyError:
        pass
    try:
        filters['price_to'] = int(params['price_to'])
    except KeyError:
        pass
    try:
        filters['currency_sid'] = int(params['currency_sid'])
    except KeyError:
        pass


    try:
        filters['persons_count_from'] = int(params['persons_count_from'])
    except KeyError:
        pass
    try:
        filters['persons_count_to'] = int(params['persons_count_to'])
    except KeyError:
        pass


    try:
        filters['total_area_from'] = int(params['total_area_from'])
    except KeyError:
        pass
    try:
        filters['total_area_to'] = int(params['total_area_to'])
    except KeyError:
        pass


    if 'family' in params:
        filters['family'] = True
    if 'foreigners' in params:
        filters['foreigners'] = True


    if 'electricity' in params:
        filters['electricity'] = True
    if 'gas' in params:
        filters['gas'] = True
    if 'hot_water' in params:
        filters['hot_water'] = True
    if 'cold_water' in params:
        filters['cold_water'] = True
    return filters


def __flats_sale_filters(params):
    filters = {
        'for_sale': True
    }


    # numeric filters
    try:
        filters['price_from'] = int(params['price_from'])
    except KeyError:
        pass
    try:
        filters['price_to'] = int(params['price_to'])
    except KeyError:
        pass
    try:
        filters['currency_sid'] = int(params['currency_sid'])
    except KeyError:
        pass


    try:
        filters['rooms_count_from'] = int(params['rooms_count_from'])
    except KeyError:
        pass
    try:
        filters['rooms_count_to'] = int(params['rooms_count_to'])
    except KeyError:
        pass


    try:
        filters['total_area_from'] = int(params['total_area_from'])
    except KeyError:
        pass
    try:
        filters['total_area_to'] = int(params['total_area_to'])
    except KeyError:
        pass


    try:
        filters['floor_from'] = int(params['floor_from'])
    except KeyError:
        pass
    try:
        filters['floor_to'] = int(params['floor_to'])
    except KeyError:
        pass


    try:
        filters['planning_sid'] = int(params['planning_sid'])
    except KeyError:
        pass


    # bool parameters goes here
    if 'new_buildings' in params:
        filters['new_buildings'] = True
    if 'secondary_market' in params:
        filters['secondary_market'] = True

    if 'mansard' in params:
        filters['mansard'] = True
    if 'ground' in params:
        filters['ground'] = True

    if 'lift' in params:
        filters['lift'] = True
    if 'electricity' in params:
        filters['electricity'] = True
    if 'gas' in params:
        filters['gas'] = True
    if 'hot_water' in params:
        filters['hot_water'] = True
    if 'cold_water' in params:
        filters['cold_water'] = True

    try:
        filters['heating_type_sid'] = int(params['heating_type_sid'])
    except KeyError:
        pass

    return filters


def __flat_rent_filters(params):
    filters = {
        'for_rent': True
    }

    try:
        filters['period_sid'] = int(params['period_sid'])
    except KeyError:
        pass


    try:
        filters['price_from'] = int(params['price_from'])
    except KeyError:
        pass
    try:
        filters['price_to'] = int(params['price_to'])
    except KeyError:
        pass
    try:
        filters['currency_sid'] = int(params['currency_sid'])
    except KeyError:
        pass


    try:
        filters['total_area_from'] = int(params['total_area_from'])
    except KeyError:
        pass
    try:
        filters['total_area_to'] = int(params['total_area_to'])
    except KeyError:
        pass


    try:
        filters['floor_from'] = int(params['floor_from'])
    except KeyError:
        pass
    try:
        filters['floor_to'] = int(params['floor_to'])
    except KeyError:
        pass


    try:
        filters['persons_count_from'] = int(params['persons_count_from'])
    except KeyError:
        pass
    try:
        filters['persons_count_to'] = int(params['persons_count_to'])
    except KeyError:
        pass


    if 'mansard' in params:
        filters['mansard'] = True
    if 'ground' in params:
        filters['ground'] = True


    if 'family' in params:
        filters['family'] = True
    if 'foreigners' in params:
        filters['foreigners'] = True


    if 'lift' in params:
        filters['lift'] = True
    if 'electricity' in params:
        filters['electricity'] = True
    if 'gas' in params:
        filters['gas'] = True
    if 'hot_water' in params:
        filters['hot_water'] = True
    if 'cold_water' in params:
        filters['cold_water'] = True
    return filters


def __rooms_sale_filters(params):
    filters = {
        'for_sale': True
    }


    try:
        filters['price_from'] = int(params['price_from'])
    except KeyError:
        pass
    try:
        filters['price_to'] = int(params['price_to'])
    except KeyError:
        pass
    try:
        filters['currency_sid'] = int(params['currency_sid'])
    except KeyError:
        pass


    try:
        filters['rooms_count_from'] = int(params['rooms_count_from'])
    except KeyError:
        pass
    try:
        filters['rooms_count_to'] = int(params['rooms_count_to'])
    except KeyError:
        pass


    try:
        filters['total_area_from'] = int(params['total_area_from'])
    except KeyError:
        pass
    try:
        filters['total_area_to'] = int(params['total_area_to'])
    except KeyError:
        pass


    try:
        filters['floor_from'] = int(params['floor_from'])
    except KeyError:
        pass
    try:
        filters['floor_to'] = int(params['floor_to'])
    except KeyError:
        pass


    try:
        filters['planning_sid'] = int(params['planning_sid'])
    except KeyError:
        pass


    if 'new_buildings' in params:
        filters['new_buildings'] = True
    if 'secondary_market' in params:
        filters['secondary_market'] = True


    if 'mansard' in params:
        filters['mansard'] = True
    if 'ground' in params:
        filters['ground'] = True


    if 'lift' in params:
        filters['lift'] = True
    if 'electricity' in params:
        filters['electricity'] = True
    if 'gas' in params:
        filters['gas'] = True
    if 'hot_water' in params:
        filters['hot_water'] = True
    if 'cold_water' in params:
        filters['cold_water'] = True
    try:
        filters['heating_type_sid'] = int(params['heating_type_sid'])
    except KeyError:
        pass

    return filters


def __rooms_rent_filters(params):
    filters = {
        'for_rent': True
    }


    try:
        filters['period_sid'] = int(params['period_sid'])
    except KeyError:
        pass


    try:
        filters['price_from'] = int(params['price_from'])
    except KeyError:
        pass
    try:
        filters['price_to'] = int(params['price_to'])
    except KeyError:
        pass
    try:
        filters['currency_sid'] = int(params['currency_sid'])
    except KeyError:
        pass


    try:
        filters['persons_count_from'] = int(params['persons_count_from'])
    except KeyError:
        pass
    try:
        filters['persons_count_to'] = int(params['persons_count_to'])
    except KeyError:
        pass


    try:
        filters['total_area_from'] = int(params['total_area_from'])
    except KeyError:
        pass
    try:
        filters['total_area_to'] = int(params['total_area_to'])
    except KeyError:
        pass


    if 'floor_from' in params:
        filters['floor_from'] = int(params['floor_from'])
    if 'floor_to' in params:
        filters['floor_to'] = int(params['floor_to'])


    if 'mansard' in params:
        filters['mansard'] = True
    if 'ground' in params:
        filters['ground'] = True


    if 'family' in params:
        filters['family'] = True
    if 'foreigners' in params:
        filters['foreigners'] = True


    if 'lift' in params:
        filters['lift'] = True
    if 'electricity' in params:
        filters['electricity'] = True
    if 'gas' in params:
        filters['gas'] = True
    if 'hot_water' in params:
        filters['hot_water'] = True
    if 'cold_water' in params:
        filters['cold_water'] = True
    return filters


def parse_houses_filters(params):
    """
    Формує об’єкт фільтрів із параметрів, переданих в запиті.
    WARNING:
        Виконує тільки базові перевірки відповідності типів,
        але не перевіряє передані фільтри з точки зору коректності структур даних
        чи взаємопов’язаності. Дані перевірки відводиться функції фільтрування,
        яка в даному випадку виступає інформаційним експертом.
    """
    try:
        operation_sid = int(params['operation_sid']) # required
    except KeyError:
        raise exceptions.InvalidArgument('"params" does not contains required param "operation_sid".')

    if operation_sid == 0:
        return __house_sale_filters(params)
    elif operation_sid == 1:
        return __house_rent_filters(params)
    else:
        raise exceptions.InvalidArgument('"params" contains invalid required param "operation_sid".')


def parse_flats_filters(params):
    """
    Формує об’єкт фільтрів із параметрів, переданих в запиті.
    WARNING:
        Виконує тільки базові перевірки відповідності типів,
        але не перевіряє передані фільтри з точки зору коректності структур даних чи взаємопов’язаності.
        Дані перевірки відводиться функції фільтрування, яка в даному випадку виступає інформаційним експертом.
    """
    try:
        operation_sid = int(params['operation_sid']) # required
    except KeyError:
        raise exceptions.InvalidArgument('"params" does not contains required param "operation_sid".')


    if operation_sid == 0:
        return __flats_sale_filters(params)
    elif operation_sid == 1:
        return __flat_rent_filters(params)
    else:
        raise exceptions.InvalidArgument('"params" contains invalid required param "operation_sid".')


def parse_rooms_filters(params):
    """
    Формує об’єкт фільтрів із параметрів, переданих в запиті.
    WARNING:
        Виконує тільки базові перевірки відповідності типів,
        але не перевіряє передані фільтри з точки зору коректності структур даних
        чи взаємопов’язаності. Дані перевірки відводиться функції фільтрування,
        яка в даному випадку виступає інформаційним експертом.
    """
    try:
        operation_sid = int(params['operation_sid']) # required
    except KeyError:
        raise exceptions.InvalidArgument('"params" does not contains required param "operation_sid".')

    if operation_sid == 0:
        return __rooms_sale_filters(params)
    elif operation_sid == 1:
        return __rooms_rent_filters(params)
    else:
        raise exceptions.InvalidArgument('"params" contains invalid required param "operation_sid".')


def parse_trades_filters(params):
    """
    Формує об’єкт фільтрів із параметрів, переданих в запиті.
    WARNING:
        Виконує тільки базові перевірки відповідності типів,
        але не перевіряє передані фільтри з точки зору коректності структур даних
        чи взаємопов’язаності. Дані перевірки відводиться функції фільтрування,
        яка в даному випадку виступає інформаційним експертом.
    """
    filters = {}
    if int(params['operation_sid']) == OPERATION_SID_SALE:
        filters['for_sale'] = True
    if int(params['operation_sid']) == OPERATION_SID_RENT:
        filters['for_rent'] = True


    if 'price_from' in params:
        filters['price_from'] = int(params['price_from'])
    if 'price_to' in params:
        filters['price_to'] = int(params['price_to'])
    if 'currency_sid' in params:
        filters['currency_sid'] = int(params['currency_sid'])


    if 'new_buildings' in params:
        filters['new_buildings'] = True
    if 'secondary_market' in params:
        filters['secondary_market'] = True


    if 'halls_area_from' in params:
        filters['halls_area_from'] = int(params['halls_area_from'])
    if 'halls_area_to' in params:
        filters['halls_area_to'] = int(params['halls_area_to'])


    if 'total_area_from' in params:
        filters['total_area_from'] = int(params['total_area_from'])
    if 'total_area_to' in params:
        filters['total_area_to'] = int(params['total_area_to'])


    if 'building_type_sid' in params: # тип будинку
        filters['building_type_sid'] = int(params['building_type_sid'])


    if 'electricity' in params:
        filters['electricity'] = True
    if 'gas' in params:
        filters['gas'] = True
    if 'hot_water' in params:
        filters['hot_water'] = True
    if 'cold_water' in params:
        filters['cold_water'] = True

    # todo: визначитись чи потрібно це поле у фільтрах
    if 'sewerage' in params:
        filters['sewerage'] = True
    return filters


def parse_offices_filters(params):
    """
    Формує об’єкт фільтрів із параметрів, переданих в запиті.
    WARNING:
        Виконує тільки базові перевірки відповідності типів,
        але не перевіряє передані фільтри з точки зору коректності структур даних
        чи взаємопов’язаності. Дані перевірки відводиться функції фільтрування,
        яка в даному випадку виступає інформаційним експертом.
    """
    filters = {}
    if int(params['operation_sid']) == OPERATION_SID_SALE:
        filters['for_sale'] = True
    if int(params['operation_sid']) == OPERATION_SID_RENT:
        filters['for_rent'] = True


    if 'price_from' in params:
        filters['price_from'] = int(params['price_from'])
    if 'price_to' in params:
        filters['price_to'] = int(params['price_to'])
    if 'currency_sid' in params:
        filters['currency_sid'] = int(params['currency_sid'])


    if 'new_buildings' in params:
        filters['new_buildings'] = True
    if 'secondary_market' in params:
        filters['secondary_market'] = True

    if 'total_area_from' in params:
        filters['total_area_from'] = int(params['total_area_from'])
    if 'total_area_to' in params:
        filters['total_area_to'] = int(params['total_area_to'])


    if 'cabinets_count_from' in params:
        filters['cabinets_count_from'] = int(params['cabinets_count_from'])
    if 'cabinets_count_to' in params:
        filters['cabinets_count_to'] = int(params['cabinets_count_to'])


    if 'security' in params:
        filters['security'] = True
    if 'kitchen' in params:
        filters['kitchen'] = True
    if 'hot_water' in params:
        filters['hot_water'] = True
    if 'cold_water' in params:
        filters['cold_water'] = True
    return filters


def parse_warehouses_filters(params):
    """
    Формує об’єкт фільтрів із параметрів, переданих в запиті.
    WARNING:
        Виконує тільки базові перевірки відповідності типів,
        але не перевіряє передані фільтри з точки зору коректності структур даних
        чи взаємопов’язаності. Дані перевірки відводиться функції фільтрування,
        яка в даному випадку виступає інформаційним експертом.
    """
    filters = {}
    if int(params['operation_sid']) == OPERATION_SID_SALE:
        filters['for_sale'] = True
    if int(params['operation_sid']) == OPERATION_SID_RENT:
        filters['for_rent'] = True


    if 'price_from' in params:
        filters['price_from'] = int(params['price_from'])
    if 'price_to' in params:
        filters['price_to'] = int(params['price_to'])
    if 'currency_sid' in params:
        filters['currency_sid'] = int(params['currency_sid'])


    if 'new_buildings' in params:
        filters['new_buildings'] = True
    if 'secondary_market' in params:
        filters['secondary_market'] = True


    if 'halls_area_from' in params:
        filters['halls_area_from'] = int(params['halls_area_from'])
    if 'halls_area_to' in params:
        filters['halls_area_to'] = int(params['halls_area_to'])


    if 'electricity' in params:
        filters['electricity'] = True
    if 'gas' in params:
        filters['gas'] = True
    if 'hot_water' in params:
        filters['hot_water'] = True
    if 'cold_water' in params:
        filters['cold_water'] = True
    if 'security_alarm' in params:
        filters['security_alarm'] = True
    if 'fire_alarm' in params:
        filters['fire_alarm'] = True

    # todo: розглянути можливість додання фільтру "охорона"
    #if 'security' in params:
    #	filters['security'] = True
    return filters


def parse_businesses_filters(params):
    """
    Формує об’єкт фільтрів із параметрів, переданих в запиті.
    WARNING:
        Виконує тільки базові перевірки відповідності типів,
        але не перевіряє передані фільтри з точки зору коректності структур даних
        чи взаємопов’язаності. Дані перевірки відводиться функції фільтрування,
        яка в даному випадку виступає інформаційним експертом.
    """
    filters = {}
    if int(params['operation_sid']) == OPERATION_SID_SALE:
        filters['for_sale'] = True
    if int(params['operation_sid']) == OPERATION_SID_RENT:
        filters['for_rent'] = True


    if 'price_from' in params:
        filters['price_from'] = int(params['price_from'])
    if 'price_to' in params:
        filters['price_to'] = int(params['price_to'])
    if 'currency_sid' in params:
        filters['currency_sid'] = int(params['currency_sid'])


    if 'new_buildings' in params:
        filters['new_buildings'] = True
    if 'secondary_market' in params:
        filters['secondary_market'] = True
    return filters


# def parse_caterings_filters(params):
#     """
#     Формує об’єкт фільтрів із параметрів, переданих в запиті.
#     WARNING:
#         Виконує тільки базові перевірки відповідності типів,
#         але не перевіряє передані фільтри з точки зору коректності структур даних
#         чи взаємопов’язаності. Дані перевірки відводиться функції фільтрування,
#         яка в даному випадку виступає інформаційним експертом.
#     """
#     filters = {
#         'operation_sid': int(params['operation_sid']) # required
#     }
#
#     if 'price_from' in params:
#         filters['price_from'] = int(params['price_from'])
#     if 'price_to' in params:
#         filters['price_to'] = int(params['price_to'])
#     if 'currency_sid' in params:
#         filters['currency_sid'] = int(params['currency_sid'])
#
#
#     if 'new_buildings' in params:
#         filters['new_buildings'] = True
#     if 'secondary_market' in params:
#         filters['secondary_market'] = True
#
#
#     if 'total_area_from' in params:
#         filters['total_area_from'] = int(params['total_area_from'])
#     if 'total_area_to' in params:
#         filters['total_area_to'] = int(params['total_area_to'])
#
#
#     if 'halls_area_from' in params:
#         filters['halls_area_from'] = int(params['halls_area_from'])
#     if 'halls_area_to' in params:
#         filters['halls_area_to'] = int(params['halls_area_to'])
#
#
#     if 'halls_count_from' in params:
#         filters['halls_count_from'] = int(params['halls_count_from'])
#     if 'halls_count_to' in params:
#         filters['halls_count_to'] = int(params['halls_count_to'])
#
#
#     if 'building_type_sid' in params: # тип будинку
#         filters['building_type_sid'] = int(params['building_type_sid'])
#
#
#     if 'electricity' in params:
#         filters['electricity'] = True
#     if 'gas' in params:
#         filters['gas'] = True
#     if 'hot_water' in params:
#         filters['hot_water'] = True
#     if 'cold_water' in params:
#         filters['cold_water'] = True
#     return filters


def parse_garages_filters(params):
    """
    Формує об’єкт фільтрів із параметрів, переданих в запиті.
    WARNING:
        Виконує тільки базові перевірки відповідності типів,
        але не перевіряє передані фільтри з точки зору коректності структур даних
        чи взаємопов’язаності. Дані перевірки відводиться функції фільтрування,
        яка в даному випадку виступає інформаційним експертом.
    """
    filters = {}
    if int(params['operation_sid']) == OPERATION_SID_SALE:
        filters['for_sale'] = True
    if int(params['operation_sid']) == OPERATION_SID_RENT:
        filters['for_rent'] = True


    if 'price_from' in params:
        filters['price_from'] = int(params['price_from'])
    if 'price_to' in params:
        filters['price_to'] = int(params['price_to'])
    if 'currency_sid' in params:
        filters['currency_sid'] = int(params['currency_sid'])


    if 'total_area_from' in params:
        filters['total_area_from'] = int(params['total_area_from'])
    if 'total_area_to' in params:
        filters['total_area_to'] = int(params['total_area_to'])


    if 'ceiling_height_from' in params:
        filters['ceiling_height_from'] = int(params['ceiling_height_from'])
    if 'ceiling_height_to' in params:
        filters['ceiling_height_to'] = int(params['ceiling_height_to'])


    if 'pit' in params:
        filters['pit'] = True
    return filters


def parse_lands_filters(params):
    """
    Формує об’єкт фільтрів із параметрів, переданих в запиті.
    WARNING:
        Виконує тільки базові перевірки відповідності типів,
        але не перевіряє передані фільтри з точки зору коректності структур даних
        чи взаємопов’язаності. Дані перевірки відводиться функції фільтрування,
        яка в даному випадку виступає інформаційним експертом.
    """
    filters = {}
    if int(params['operation_sid']) == OPERATION_SID_SALE:
        filters['for_sale'] = True
    if int(params['operation_sid']) == OPERATION_SID_RENT:
        filters['for_rent'] = True


    if 'price_from' in params:
        filters['price_from'] = int(params['price_from'])
    if 'price_to' in params:
        filters['price_to'] = int(params['price_to'])
    if 'currency_sid' in params:
        filters['currency_sid'] = int(params['currency_sid'])


    if 'area_from' in params:
        filters['area_from'] = int(params['area_from'])
    if 'area_to' in params:
        filters['area_to'] = int(params['area_to'])


    if 'electricity' in params:
        filters['electricity'] = True
    if 'gas' in params:
        filters['gas'] = True
    if 'water' in params:
        filters['water'] = True
    if 'sewerage' in params:
        filters['sewerage'] = True
    return filters
