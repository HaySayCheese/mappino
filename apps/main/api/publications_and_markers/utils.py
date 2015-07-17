# coding=utf-8

#coding=utf-8
import collective.exceptions as exceptions


# constant
class OperationSID(object):
    sale = 0
    rent = 1


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
        operation_sid = int(params['op_sid']) # required
    except KeyError:
        raise exceptions.InvalidArgument('"params" does not contains required param "op_sid".')

    if operation_sid == OperationSID.sale:
        return __house_sale_filters(params)
    elif operation_sid == OperationSID.rent:
        return __house_rent_filters(params)
    else:
        raise exceptions.InvalidArgument('"params" contains invalid required param "op_sid".')


def parse_flats_filters(params):
    """
    Формує об’єкт фільтрів із параметрів, переданих в запиті.
    WARNING:
        Виконує тільки базові перевірки відповідності типів,
        але не перевіряє передані фільтри з точки зору коректності структур даних чи взаємопов’язаності.
        Дані перевірки відводиться функції фільтрування, яка в даному випадку виступає інформаційним експертом.
    """
    try:
        operation_sid = int(params['op_sid']) # required
    except KeyError:
        raise exceptions.InvalidArgument('"params" does not contains required param "op_sid".')


    if operation_sid == OperationSID.sale:
        return __flats_sale_filters(params)
    elif operation_sid == OperationSID.rent:
        return __flat_rent_filters(params)
    else:
        raise exceptions.InvalidArgument('"params" contains invalid required param "op_sid".')


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
        operation_sid = int(params['op_sid']) # required
    except KeyError:
        raise exceptions.InvalidArgument('"params" does not contains required param "op_sid".')

    if operation_sid == OperationSID.sale:
        return __rooms_sale_filters(params)
    elif operation_sid == OperationSID.rent:
        return __rooms_rent_filters(params)
    else:
        raise exceptions.InvalidArgument('"params" contains invalid required param "op_sid".')


def parse_trades_filters(params):
    """
    Формує об’єкт фільтрів із параметрів, переданих в запиті.
    WARNING:
        Виконує тільки базові перевірки відповідності типів,
        але не перевіряє передані фільтри з точки зору коректності структур даних
        чи взаємопов’язаності. Дані перевірки відводиться функції фільтрування,
        яка в даному випадку виступає інформаційним експертом.
    """
    if int(params['op_sid']) == OperationSID.sale:
        params['for_sale'] = True

    elif int(params['op_sid']) == OperationSID.rent:
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
    if int(params['op_sid']) == OperationSID.sale:
        params['for_sale'] = True

    elif int(params['op_sid']) == OperationSID.rent:
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
    if int(params['op_sid']) == OperationSID.sale:
        params['for_sale'] = True
    elif int(params['op_sid']) == OperationSID.rent:
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
    if int(params['op_sid']) == OperationSID.sale:
        filters['for_sale'] = True
    if int(params['op_sid']) == OperationSID.rent:
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
    if int(params['op_sid']) == OperationSID.sale:
        params['for_sale'] = True

    elif int(params['op_sid']) == OperationSID.rent:
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
    if int(params['op_sid']) == OperationSID.sale:
        params['for_sale'] = True

    if int(params['op_sid']) == OperationSID.rent:
        params['for_rent'] = True

    return params


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