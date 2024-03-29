#coding=utf-8
from decimal import InvalidOperation
from collective.methods.formatters import format_text
from collective.methods.formatters import format_title

from django.db import DatabaseError, IntegrityError

from core.currencies.constants import CURRENCIES
from core.publications.constants import SALE_TRANSACTION_TYPES, MARKET_TYPES, INDIVIDUAL_HEATING_TYPES, HEATING_TYPES, \
    FLOOR_TYPES, OBJECT_CONDITIONS
from core.publications.models import OfficesRentTerms, OfficesBodies, OfficesSaleTerms
from core.publications.objects_constants.trades import TRADE_BUILDING_TYPES




# Оновлює інформацію про офіс.
#
# Поле для оновлення відшукується за префіксом @field.
# Значення, що онволюється (@value) перевіряється лише на коректність з точки зору БД та системи:
# (недопустимі, умисно некоректні значення, такі, що можуть призвести до збоїв системи)
#
# Жодних перевірок щодо правдивості та консистентності введеного значення не здійснюється,
# оскільки, на момет вводу, система може не володіти достатнім контекстом,
# а для його отримання часто необхідно виконати один або декілька додаткових запитів до БД,
# що відобразиться на продуктивності системи в цілому.
#
# Крім цього, користувач може вводити дані не послідовно, пропускаючи деякі поля,
# (напр. завідомо плануючи залишити оголошення в чернетках на деякий термін)
# тоді як перевірка певних полів може залежати від значень інших, пропущених полів.
#
# Перевірку консистентності даних слід виконувати на етапі підготовки оголошення до публікації.

def update_office(h, field, value, tid):
    try:
        # bool
        if field == 'for_sale':
            if (value is True) or (value is False):
                h.for_sale = value
                h.save(force_update=True)
            else:
                raise ValueError()


        # blank or decimal
        elif field == 'sale_price':
            if not value:
                st = OfficesSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
                st.price = None
                st.save(force_update=True)
                return
            else:
                value = round(float(value.replace(',', '.')), 2)
                if value <= 0:
                    raise ValueError()

                st = OfficesSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
                st.price = value
                st.save(force_update=True)

                if int(value) == value:
                    # Якщо після коми лише нулі - повернути ціле значення
                    return "%.0f" % value
                else:
                    # Інакше - округлити до 2х знаків після коми
                    return "%.2f" % value


        # sid
        elif field == 'sale_transaction_sid':
            value = int(value)
            if value not in SALE_TRANSACTION_TYPES.values():
                raise ValueError()

            st = OfficesSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
            st.transaction_sid = value
            st.save(force_update=True)
            return


        # sid
        elif field == 'sale_currency_sid':
            value = int(value)
            if value not in CURRENCIES.values():
                raise ValueError()

            st = OfficesSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
            st.currency_sid = value
            st.save(force_update=True)
            return


        # bool
        elif field == 'sale_is_contract':
            if (value is True) or (value is False):
                st = OfficesSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
                st.is_contract = value
                st.save(force_update=True)
                return
            else:
                raise ValueError()


        # text
        elif field == 'sale_add_terms':
            st = OfficesSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
            if not value:
                st.add_terms = u''
                st.save(force_update=True)
                return
            else:
                value = format_text(value)
                st.add_terms = value
                st.save(force_update=True)
                return value


        # bool
        elif field == 'for_rent':
            if (value is True) or (value is False):
                h.for_rent = value
                h.save(force_update=True)
                return
            else:
                raise ValueError()


        # blank or decimal
        elif field == 'rent_price':
            if not value:
                rt = OfficesRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
                rt.price = None
                rt.save(force_update=True)
                return
            else:
                value = round(float(value.replace(',','.')), 2)
                if value <= 0:
                    raise ValueError()

                rt = OfficesRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
                rt.price = value
                rt.save(force_update=True)

                if int(value) == value:
                    # Якщо після коми лише нулі - повернути ціле значення
                    return "%.0f" % value
                else:
                    # Інакше - округлити до 2х знаків після коми
                    return "%.2f" % value


        # sid
        elif field == 'rent_currency_sid':
            value = int(value)
            if value not in CURRENCIES.values():
                raise ValueError()

            rt = OfficesRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
            rt.currency_sid = value
            rt.save(force_update=True)
            return


        # boolean
        elif field == 'rent_is_contract':
            if (value is True) or (value is False):
                rt = OfficesRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
                rt.is_contract = value
                rt.save(force_update=True)
                return
            else:
                raise ValueError()


        # text
        elif field == 'rent_add_terms':
            rt = OfficesRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
            if not value:
                rt.add_terms = u''
                rt.save(force_update=True)
                return
            else:
                value = format_text(value)
                rt.add_terms = value
                rt.save(force_update=True)
                return value


        # text
        elif field == 'description':
            b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
            if not value:
                b.description = u''
                b.save(force_update=True)
                return
            else:
                value = format_text(value)
                b.description = value
                b.save(force_update=True)
                return value


        # sid
        elif field == 'market_type_sid':
            value = int(value)
            if value not in MARKET_TYPES.values():
                raise ValueError()

            b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
            b.market_type_sid = value
            b.save(force_update=True)
            return


        # sid
        elif field == 'building_type_sid':
            value = int(value)
            if value not in TRADE_BUILDING_TYPES.values():
                raise ValueError()

            b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
            b.building_type_sid = value
            b.save(force_update=True)
            return


        # blank or int
        elif field == 'build_year':
            if not value:
                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.build_year = None
                b.save(force_update=True)
                return
            else:
                value = int(value)
                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.build_year = value
                b.save(force_update=True)
                return


        # sid
        elif field == 'condition_sid':
            value = int(value)
            if value not in OBJECT_CONDITIONS.values():
                raise ValueError()

            b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
            b.condition_sid = value
            b.save(force_update=True)
            return


        # blank or int
        elif field == 'floor':
            if not value:
                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.floor = None
                b.save(force_update=True)
                return
            else:
                value = int(value)
                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.floor = value
                b.save(force_update=True)
                return


        # sid
        elif field == 'floor_type_sid':
            value = int(value)
            if value not in FLOOR_TYPES.values():
                raise ValueError()

            b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
            b.floor_type_sid = value

            # Якщо тип поверху "мансарда" або "цоколь", то ітак зрозуміло,
            # шо це або останній поверх, або нульовий/перший.
            # Немає необхідності зберігати додаткові дані.
            if value in [FLOOR_TYPES.mansard(), FLOOR_TYPES.ground()]:
                b.floor = None

            b.save(force_update=True)
            return


        # blank or int
        elif field == 'floors_count':
            if not value:
                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.floors_count = None
                b.save(force_update=True)
                return
            else:
                value = int(value)
                if value <= 0:
                    raise ValueError()

                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.floors_count = int(value)
                b.save(force_update=True)
                return



        # blank or int
        elif field == 'cabinets_count':
            if not value:
                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.cabinets_count = None
                b.save(force_update=True)
                return
            else:
                value = int(value)
                if value < 0:
                    raise ValueError()

                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.cabinets_count = value
                b.save(force_update=True)
                return


        # blank or float
        elif field == 'total_area':
            if not value:
                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.total_area = None
                b.save(force_update=True)
                return
            else:
                value = round(float(value.replace(',', '.')), 2)
                if value <= 0:
                    raise ValueError()

                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.total_area = value
                b.save(force_update=True)

                if int(value) == value:
                    # Відсікти дробову частину, якщо після коми нулі
                    return "%.0f" % value
                else:
                    # Скоротити / розширити до 2х цифр після коми
                    return "%.2f" % value


        # boolean
        elif field == 'closed_area':
            if (value is True) or (value is False):
                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.closed_area = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # blank or int
        elif field == 'wcs_count':
            if not value:
                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.wcs_count = None
                b.save(force_update=True)
                return
            else:
                value = int(value)
                if value < 0:
                    raise ValueError()

                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.wcs_count = value
                b.save(force_update=True)
                return


        # blank or float
        elif field == 'ceiling_height':
            if not value:
                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.ceiling_height = None
                b.save(force_update=True)
                return
            else:
                value = round(float(value.replace(',', '.')), 2)
                if value <= 0:
                    raise ValueError()

                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.ceiling_height = value
                b.save(force_update=True)

                if int(value) == value:
                    # Відсікти дробову частину, якщо після коми нулі
                    return "%.0f" % value
                else:
                    # скоротити / розширити до 2х цифр після коми
                    return "%.2f" % value


        # sid
        elif field == 'heating_type_sid':
            value = int(value)
            if value not in HEATING_TYPES.values():
                raise ValueError()

            b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
            b.heating_type_sid = value
            b.save(force_update=True)
            return


        # text
        elif field == 'custom_heating_type':
            b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
            if not value:
                b.custom_heating_type = u''
                b.save(force_update=True)
                return
            else:
                value = format_title(value)
                b.custom_heating_type = value
                b.save(force_update=True)
                return value


        # sid
        elif field == 'ind_heating_type_sid':
            value = int(value)
            if value not in INDIVIDUAL_HEATING_TYPES.values():
                raise ValueError()

            b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
            b.ind_heating_type_sid = value
            b.save(force_update=True)
            return


        # text
        elif field == 'custom_ind_heating_type':
            b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
            if not value:
                b.custom_ind_heating_type = u''
                b.save(force_update=True)
                return
            else:
                value = format_title(value)
                b.custom_ind_heating_type = value
                b.save(force_update=True)
                return value


        # boolean
        elif field == 'kitchen':
            if (value is True) or (value is False):
                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.kitchen = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'security_alarm':
            if (value is True) or (value is False):
                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.security_alarm = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'fire_alarm':
            if (value is True) or (value is False):
                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.fire_alarm = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'hot_water':
            if (value is True) or (value is False):
                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.hot_water = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'cold_water':
            if (value is True) or (value is False):
                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.cold_water = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'security':
            if (value is True) or (value is False):
                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.security = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'furniture':
            if (value is True) or (value is False):
                rt = OfficesRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
                rt.furniture = value
                rt.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'conditioner':
            if (value is True) or (value is False):
                rt = OfficesRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
                rt.conditioner = value
                rt.save(force_update=True)
                return
            else:
                raise ValueError()


        # text
        elif field == 'add_equipment':
            rt = OfficesSaleTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
            if not value:
                rt.add_equipment = u''
                rt.save(force_update=True)
                return
            else:
                # todo: додати форматування
                rt.add_equipment = value
                rt.save(force_update=True)
                return


        # text
        elif field == 'add_facilities':
            b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
            if not value:
                b.add_facilities = u''
                b.save(force_update=True)
                return
            else:
                # todo: додати форматування
                b.add_facilities = value
                b.save(force_update=True)
                return


        # boolean
        elif field == 'phone':
            if (value is True) or (value is False):
                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.phone = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'mobile_coverage':
            if (value is True) or (value is False):
                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.mobile_coverage = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'internet':
            if (value is True) or (value is False):
                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.internet = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'cable_tv':
            if (value is True) or (value is False):
                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.cable_tv = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'lan':
            if (value is True) or (value is False):
                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.lan = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # blank or int
        elif field == 'phone_lines_count':
            if not value:
                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.phone_lines_count = None
                b.save(force_update=True)
                return
            else:
                value = int(value)
                if value <= 0:
                    raise ValueError()

                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.phone_lines_count = int(value)
                b.save(force_update=True)
                return


        # boolean
        elif field == 'parking':
            if (value is True) or (value is False):
                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.parking = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'open_air':
            if (value is True) or (value is False):
                b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.open_air = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # text
        elif field == 'add_buildings':
            b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]
            if not value:
                b.add_buildings= None
                b.save(force_update=True)
                return
            else:
                # todo: додати форматування
                b.add_buildings = value
                b.save(force_update=True)
                return


        # text
        elif field == 'lat_lng':
            h.set_lat_lng(value)
            return


        # text
        elif field == 'address':
            b = OfficesBodies.objects.filter(id=h.body_id).only('id')[0]

            if not value:
                b.address = u''
                b.save(force_update=True)
                return
            else:
                # note: адреса не форматується, оскільки не можливо передбачити,
                # як саме користувач її введе.
                b.address = value
                b.save(force_update=True)
                return


        # ...
        # other fields here
        # ...

        else:
            raise ValueError('invalid @field')

    except (DatabaseError, IntegrityError, InvalidOperation, ValueError) as e:
        raise ValueError(u'Field update error. Prefix: {0}. Value = {1}; Message: {2};'.format(
            unicode(field), unicode(value), e.message
        ))