#coding=utf-8
from decimal import InvalidOperation
from collective.methods.formatters import format_text
from collective.methods.formatters import format_title

from django.db import DatabaseError, IntegrityError

from core.currencies.constants import CURRENCIES
from core.publications.constants import SALE_TRANSACTION_TYPES, INDIVIDUAL_HEATING_TYPES, HEATING_TYPES, MARKET_TYPES
from core.publications.models import WarehousesBodies, WarehousesRentTerms, WarehousesSaleTerms




# Оновлює інформацію про склад.
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

def update_warehouse(h, field, value, tid):
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
                st = WarehousesSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
                st.price = None
                st.save(force_update=True)
                return
            else:
                value = round(float(value.replace(',', '.')), 2)
                if value <= 0:
                    raise ValueError()

                st = WarehousesSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
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

            st = WarehousesSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
            st.transaction_sid = value
            st.save(force_update=True)
            return


        # sid
        elif field == 'sale_currency_sid':
            value = int(value)
            if value not in CURRENCIES.values():
                raise ValueError()

            st = WarehousesSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
            st.currency_sid = value
            st.save(force_update=True)
            return


        # bool
        elif field == 'sale_is_contract':
            if (value is True) or (value is False):
                st = WarehousesSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
                st.is_contract = value
                st.save(force_update=True)
                return
            else:
                raise ValueError()


        # text
        elif field == 'sale_add_terms':
            st = WarehousesSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
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
                rt = WarehousesRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
                rt.price = None
                rt.save(force_update=True)
                return
            else:
                value = round(float(value.replace(',','.')), 2)
                if value <= 0:
                    raise ValueError()

                rt = WarehousesRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
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

            rt = WarehousesRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
            rt.currency_sid = value
            rt.save(force_update=True)
            return


        # boolean
        elif field == 'rent_is_contract':
            if (value is True) or (value is False):
                rt = WarehousesRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
                rt.is_contract = value
                rt.save(force_update=True)
                return
            else:
                raise ValueError()


        # text
        elif field == 'rent_add_terms':
            rt = WarehousesRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
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
            b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
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

            b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
            b.market_type_sid = value
            b.save(force_update=True)
            return


        # blank or float
        elif field == 'halls_area':
            if not value:
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.halls_area = None
                b.save(force_update=True)
                return
            else:
                value = round(float(value.replace(',', '.')), 2)
                if value <= 0:
                    raise ValueError()

                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.halls_area = value
                b.save(force_update=True)

                if int(value) == value:
                    # Відсікти дробову частину, якщо після коми нулі
                    return "%.0f" % value
                else:
                    # Скоротити / розширити до 2х цифр після коми
                    return "%.2f" % value


        # boolean
        elif field == 'open_space':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.open_space = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # blank or float
        elif field == 'plot_area':
            if not value:
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.plot_area = None
                b.save(force_update=True)
                return
            else:
                value = round(float(value.replace(',', '.')), 2)
                if value <= 0:
                    raise ValueError()

                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.plot_area = value
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
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.closed_area = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # sid
        elif field == 'heating_type_sid':
            value = int(value)
            if value not in HEATING_TYPES.values():
                raise ValueError()

            b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
            b.heating_type_sid = value
            b.save(force_update=True)
            return


        # text
        elif field == 'custom_heating_type':
            b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
            if not value:
                b.custom_heating_type = u''
                b.save(force_update=True)
                return
            else:
                value = format_title(value)
                b.custom_heating_type = value
                b.save(force_update=True)
                return


        # sid
        elif field == 'ind_heating_type_sid':
            value = int(value)
            if value not in INDIVIDUAL_HEATING_TYPES.values():
                raise ValueError()

            b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
            b.ind_heating_type_sid = value
            b.save(force_update=True)
            return


        # text
        elif field == 'custom_ind_heating_type':
            b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
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
        elif field == 'electricity':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.electricity = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'gas':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.gas = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'security_alarm':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.security_alarm = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'fire_alarm':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.fire_alarm = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'hot_water':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.hot_water = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'cold_water':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.cold_water = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'sewerage':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.sewerage = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'ventilation':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.ventilation = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'security':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.security = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # text
        elif field == 'add_facilities':
            b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
            if not value:
                b.add_facilities = u''
                b.save(force_update=True)
                return
            else:
                value = format_text(value)
                b.add_facilities = value
                b.save(force_update=True)
                return


        # boolean
        elif field == 'phone':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.phone = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'mobile_coverage':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.mobile_coverage = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'internet':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.internet = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'lan':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.lan = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # blank or int
        elif field == 'phone_lines_count':
            if not value:
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.phone_lines_count = None
                b.save(force_update=True)
                return
            else:
                value = int(value)
                if value <= 0:
                    raise ValueError()

                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.phone_lines_count = int(value)
                b.save(force_update=True)
                return


        # boolean
        elif field == 'parking':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.parking = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'offices':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.offices = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'ramp':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.ramp = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'cathead':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.cathead = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'storeroom':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.storeroom = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'wc':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.wc = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # text
        elif field == 'add_buildings':
            b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
            if not value:
                b.add_buildings= None
                b.save(force_update=True)
                return
            else:
                # todo: додати форматування
                b.add_buildings = value
                b.save(force_update=True)
                return


        # boolean
        elif field == 'railway':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.railway = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'asphalt':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.asphalt = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'concrete':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.concrete = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'ground':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.ground = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # text
        elif field == 'add_driveways':
            b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
            if not value:
                b.add_driveways= None
                b.save(force_update=True)
                return
            else:
                value = format_text(value)
                b.add_driveways = value
                b.save(force_update=True)
                return


        # boolean
        elif field == 'transport_stop':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.transport_stop = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'bank':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.bank = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'market':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.market = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'cash_machine':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.cash_machine = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'cafe':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.cafe = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'entertainment':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.entertainment = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'refueling':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.refueling = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'railway_station':
            if (value is True) or (value is False):
                b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.railway_station = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # text
        elif field == 'add_showplaces':
            b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]
            if not value:
                b.add_showplaces= None
                b.save(force_update=True)
                return
            else:
                value = format_text(value)
                b.add_showplaces = value
                b.save(force_update=True)
                return


        # text
        elif field == 'lat_lng':
            h.set_lat_lng(value)
            return


        # text
        elif field == 'address':
            b = WarehousesBodies.objects.filter(id=h.body_id).only('id')[0]

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