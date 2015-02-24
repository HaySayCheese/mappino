#coding=utf-8
import exceptions


OPERATION_SID_SALE = 0
OPERATION_SID_RENT = 1


def __house_sale_filters(params):
    params['for_sale'] = True
    return params


def __house_rent_filters(params):
    params['for_rent'] = True
    return params


def __flats_sale_filters(params):
    params['for_sale'] = True
    return params


def __flat_rent_filters(params):
    params['for_rent'] = True
    return params


def __rooms_sale_filters(params):
    params['for_sale'] = True
    return params


def __rooms_rent_filters(params):
    params['for_rent'] = True
    return params


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
    if int(params['operation_sid']) == OPERATION_SID_SALE:
        params['for_sale'] = True

    elif int(params['operation_sid']) == OPERATION_SID_RENT:
        params['for_rent'] = True

    return params


def parse_offices_filters(params):
    """
    Формує об’єкт фільтрів із параметрів, переданих в запиті.
    WARNING:
        Виконує тільки базові перевірки відповідності типів,
        але не перевіряє передані фільтри з точки зору коректності структур даних
        чи взаємопов’язаності. Дані перевірки відводиться функції фільтрування,
        яка в даному випадку виступає інформаційним експертом.
    """
    if int(params['operation_sid']) == OPERATION_SID_SALE:
        params['for_sale'] = True

    elif int(params['operation_sid']) == OPERATION_SID_RENT:
        params['for_rent'] = True

    return params


def parse_warehouses_filters(params):
    """
    Формує об’єкт фільтрів із параметрів, переданих в запиті.
    WARNING:
        Виконує тільки базові перевірки відповідності типів,
        але не перевіряє передані фільтри з точки зору коректності структур даних
        чи взаємопов’язаності. Дані перевірки відводиться функції фільтрування,
        яка в даному випадку виступає інформаційним експертом.
    """
    if int(params['operation_sid']) == OPERATION_SID_SALE:
        params['for_sale'] = True
    elif int(params['operation_sid']) == OPERATION_SID_RENT:
        params['for_rent'] = True

    return params


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


def parse_garages_filters(params):
    """
    Формує об’єкт фільтрів із параметрів, переданих в запиті.
    WARNING:
        Виконує тільки базові перевірки відповідності типів,
        але не перевіряє передані фільтри з точки зору коректності структур даних
        чи взаємопов’язаності. Дані перевірки відводиться функції фільтрування,
        яка в даному випадку виступає інформаційним експертом.
    """
    if int(params['operation_sid']) == OPERATION_SID_SALE:
        params['for_sale'] = True

    elif int(params['operation_sid']) == OPERATION_SID_RENT:
        params['for_rent'] = True

    return params


def parse_lands_filters(params):
    """
    Формує об’єкт фільтрів із параметрів, переданих в запиті.
    WARNING:
        Виконує тільки базові перевірки відповідності типів,
        але не перевіряє передані фільтри з точки зору коректності структур даних
        чи взаємопов’язаності. Дані перевірки відводиться функції фільтрування,
        яка в даному випадку виступає інформаційним експертом.
    """
    if int(params['operation_sid']) == OPERATION_SID_SALE:
        params['for_sale'] = True

    if int(params['operation_sid']) == OPERATION_SID_RENT:
        params['for_rent'] = True

    return params