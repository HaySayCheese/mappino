# coding=utf-8
from apps.main.api.publications_and_markers.exceptions import OperationSIDParseError


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
    operation_sid = __get_operation_sid(params)

    if operation_sid == OperationSID.sale:
        return __house_sale_filters(params)

    elif operation_sid == OperationSID.rent:
        return __house_rent_filters(params)

    else:
        raise OperationSIDParseError('"params" contains invalid required param "op_sid".')


def parse_flats_filters(params):
    """
    Формує об’єкт фільтрів із параметрів, переданих в запиті.
    WARNING:
        Виконує тільки базові перевірки відповідності типів,
        але не перевіряє передані фільтри з точки зору коректності структур даних чи взаємопов’язаності.
        Дані перевірки відводиться функції фільтрування, яка в даному випадку виступає інформаційним експертом.
    """
    operation_sid = __get_operation_sid(params)

    if operation_sid == OperationSID.sale:
        return __flats_sale_filters(params)

    elif operation_sid == OperationSID.rent:
        return __flat_rent_filters(params)

    else:
        raise OperationSIDParseError('"params" contains invalid required param "op_sid".')


def parse_rooms_filters(params):
    """
    Формує об’єкт фільтрів із параметрів, переданих в запиті.
    WARNING:
        Виконує тільки базові перевірки відповідності типів,
        але не перевіряє передані фільтри з точки зору коректності структур даних
        чи взаємопов’язаності. Дані перевірки відводиться функції фільтрування,
        яка в даному випадку виступає інформаційним експертом.
    """
    operation_sid = __get_operation_sid(params)

    if operation_sid == OperationSID.sale:
        return __rooms_sale_filters(params)

    elif operation_sid == OperationSID.rent:
        return __rooms_rent_filters(params)

    else:
        raise OperationSIDParseError('"params" contains invalid required param "op_sid".')


def parse_trades_filters(params):
    """
    Формує об’єкт фільтрів із параметрів, переданих в запиті.
    WARNING:
        Виконує тільки базові перевірки відповідності типів,
        але не перевіряє передані фільтри з точки зору коректності структур даних
        чи взаємопов’язаності. Дані перевірки відводиться функції фільтрування,
        яка в даному випадку виступає інформаційним експертом.
    """
    operation_sid = __get_operation_sid(params)

    if operation_sid == OperationSID.sale:
        params['for_sale'] = True

    elif operation_sid == OperationSID.rent:
        params['for_rent'] = True

    else:
        raise OperationSIDParseError('"params" contains invalid required param "op_sid".')

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
    operation_sid = __get_operation_sid(params)

    if operation_sid == OperationSID.sale:
        params['for_sale'] = True

    elif operation_sid == OperationSID.rent:
        params['for_rent'] = True

    else:
        raise OperationSIDParseError('"params" contains invalid required param "op_sid".')

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
    operation_sid = __get_operation_sid(params)

    if operation_sid == OperationSID.sale:
        params['for_sale'] = True

    elif operation_sid == OperationSID.rent:
        params['for_rent'] = True

    else:
        raise OperationSIDParseError('"params" contains invalid required param "op_sid".')

    return params


def parse_garages_filters(params):
    """
    Формує об’єкт фільтрів із параметрів, переданих в запиті.
    WARNING:
        Виконує тільки базові перевірки відповідності типів,
        але не перевіряє передані фільтри з точки зору коректності структур даних
        чи взаємопов’язаності. Дані перевірки відводиться функції фільтрування,
        яка в даному випадку виступає інформаційним експертом.
    """
    operation_sid = __get_operation_sid(params)

    if operation_sid == OperationSID.sale:
        params['for_sale'] = True

    elif operation_sid == OperationSID.rent:
        params['for_rent'] = True

    else:
        raise OperationSIDParseError('"params" contains invalid required param "op_sid".')

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
    operation_sid = __get_operation_sid(params)

    if operation_sid == OperationSID.sale:
        params['for_sale'] = True

    elif operation_sid == OperationSID.rent:
        params['for_rent'] = True

    else:
        raise OperationSIDParseError('"params" contains invalid required param "op_sid".')

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


# system methods
def __get_operation_sid(params):
    try:
        return int(params['op_sid'])
    except (KeyError, ValueError,):
        raise OperationSIDParseError('"params" does not contains required param "op_sid".')
