#coding=utf-8
from decimal import InvalidOperation

from django.db import DatabaseError, IntegrityError

from collective.methods.formatters import format_text, format_title
from core.currencies.constants import CURRENCIES
from core.publications.constants import \
    MARKET_TYPES, FLOOR_TYPES, OBJECT_CONDITIONS, HEATING_TYPES, INDIVIDUAL_HEATING_TYPES, LIVING_RENT_PERIODS
from core.publications.models import FlatsBodies, FlatsRentTerms, FlatsSaleTerms
from core.publications.objects_constants.flats import FLAT_ROOMS_PLANNINGS, FLAT_BUILDING_TYPES


# Оновлює інформацію про квартиру.
#
# Поле для оновлення відшукується за префіксом @field.
# Значення, що оноволюється (@value) перевіряється лише на коректність з точки зору БД та системи:
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
#
#
def update_flat(h, field, value, tid):
    try:
        # bool
        if field == 'for_sale':
            if (value is True) or (value is False):
                h.for_sale = value
                h.save(force_update=True)
                return
            else:
                raise ValueError()


        # blank or decimal
        elif field == 'sale_price':
            if not value:
                st = FlatsSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
                st.price = None
                st.save(force_update=True)
                return
            else:
                value = round(float(value.replace(',', '.')), 2)
                if value <= 0:
                    raise ValueError()

                st = FlatsSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
                st.price = value
                st.save(force_update=True)

                if int(value) == value:
                    # Якщо після коми лише нулі - повернути ціле значення
                    return "%.0f" % value
                else:
                    # Інакше - округлити до 2х знаків після коми
                    return "%.2f" % value


        # sid
        elif field == 'sale_currency_sid':
            value = int(value)
            if value not in CURRENCIES.values():
                raise ValueError()

            st = FlatsSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
            st.currency_sid = value
            st.save(force_update=True)
            return


        # bool
        elif field == 'sale_is_contract':
            if (value is True) or (value is False):
                st = FlatsSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
                st.is_contract = value
                st.save(force_update=True)
                return
            else:
                raise ValueError()


        # bool
        elif field == 'for_rent':
            if (value is True) or (value is False):
                h.for_rent = value
                h.save(force_update=True)
                return
            else:
                raise ValueError()


        # sid
        elif field == 'rent_period_sid':
            value = int(value)
            if value not in LIVING_RENT_PERIODS.values():
                raise ValueError()

            rt = FlatsRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
            rt.period_sid = value
            rt.save(force_update=True)
            return


        # blank or int
        elif field == 'rent_persons_count':
            if not value:
                rt = FlatsRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
                rt.persons_count = None
                rt.save(force_update=True)
                return

            else:
                value = int(value)
                if value <= 0:
                    raise ValueError()

                rt = FlatsRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
                rt.persons_count = value
                rt.save(force_update=True)
                return


        # blank or decimal
        elif field == 'rent_price':
            if not value:
                rt = FlatsRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
                rt.price = None
                rt.save(force_update=True)

            else:
                value = round(float(value.replace(',','.')), 2)
                if value <= 0:
                    raise ValueError()

                rt = FlatsRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
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

            rt = FlatsRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
            rt.currency_sid = value
            rt.save(force_update=True)
            return


        # boolean
        elif field == 'rent_is_contract':
            if (value is True) or (value is False):
                rt = FlatsRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
                rt.is_contract = value
                rt.save(force_update=True)
                return
            else:
                raise ValueError()


        # text
        elif field == 'description':
            b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
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

            b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
            b.market_type_sid = value
            b.save(force_update=True)
            return


        # sid
        elif field == 'building_type_sid':
            value = int(value)
            if value not in FLAT_BUILDING_TYPES.values():
                raise ValueError()

            b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
            b.building_type_sid = value
            b.save(force_update=True)
            return


        # sid
        elif field == 'rooms_planning_sid':
            value = int(value)
            if value not in FLAT_ROOMS_PLANNINGS.values():
                raise ValueError()

            b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
            b.rooms_planning_sid = value
            b.save(force_update=True)
            return


        # sid
        elif field == 'condition_sid':
            value = int(value)
            if value not in OBJECT_CONDITIONS.values():
                raise ValueError()

            b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
            b.condition_sid = value
            b.save(force_update=True)
            return


        # blank or int
        elif field == 'floor':
            if not value:
                b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
                b.floor = None
                b.save(force_update=True)
                return
            else:
                value = int(value)
                b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
                b.floor = value

                try:
                    b.save(force_update=True)
                    return

                except DatabaseError:
                    return ''


        # sid
        elif field == 'floor_type_sid':
            value = int(value)
            if value not in FLOOR_TYPES.values():
                raise ValueError()

            b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
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
                b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
                b.floors_count = None
                b.save(force_update=True)
                return
            else:
                value = int(value)
                if value <= 0:
                    raise ValueError()

                b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
                b.floors_count = int(value)
                b.save(force_update=True)
                return


        # blank or float
        elif field == 'total_area':
            if not value:
                b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
                b.total_area = None
                b.save(force_update=True)
                return
            else:
                value = round(float(value.replace(',', '.')), 2)
                if value <= 0:
                    raise ValueError()

                b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
                b.total_area = value
                b.save(force_update=True)

                if int(value) == value:
                    # Відсікти дробову частину, якщо після коми нулі
                    return "%.0f" % value
                else:
                    # Скоротити / розширити до 2х цифр після коми
                    return "%.2f" % value


        # blank or float
        elif field == 'living_area':
            if not value:
                b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
                b.living_area = None
                b.save(force_update=True)
                return
            else:
                value = round(float(value.replace(',', '.')), 2)
                if value <= 0:
                    raise ValueError()

                b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
                b.living_area = value
                b.save(force_update=True)

                if int(value) == value:
                    # Відсікти дробову частину, якщо після коми нулі
                    return "%.0f" % value
                else:
                    # скоротити / розширити до 2х цифр після коми
                    return "%.2f" % value


        # blank or float
        elif field == 'kitchen_area':
            if not value:
                b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
                b.kitchen_area = None
                b.save(force_update=True)
                return
            else:
                value = round(float(value.replace(',', '.')), 2)
                if value <= 0:
                    raise ValueError()

                b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
                b.kitchen_area = value
                b.save(force_update=True)

                if int(value) == value:
                    # Відсікти дробову частину, якщо після коми нулі
                    return "%.0f" % value
                else:
                    # Скоротити / розширити до 2х цифр після коми
                    return "%.2f" % value


        # blank or int
        elif field == 'rooms_count':
            if not value:
                b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
                b.rooms_count = None
                b.save(force_update=True)
                return
            else:
                value = int(value)
                b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
                b.rooms_count = value
                b.save(force_update=True)
                return


        # sid
        elif field == 'heating_type_sid':
            value = int(value)
            if value not in HEATING_TYPES.values():
                raise ValueError()

            b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
            b.heating_type_sid = value
            b.save(force_update=True)
            return


        # text
        elif field == 'custom_heating_type':
            b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
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

            b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
            b.ind_heating_type_sid = value
            b.save(force_update=True)
            return


        # text
        elif field == 'custom_ind_heating_type':
            b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
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
                b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
                b.electricity = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'gas':
            if (value is True) or (value is False):
                b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
                b.gas = value
                b.save(force_update=True)
            else:
                raise ValueError()


        # boolean
        elif field == 'security_alarm':
            if (value is True) or (value is False):
                b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
                b.security_alarm = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'fire_alarm':
            if (value is True) or (value is False):
                b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
                b.fire_alarm = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'hot_water':
            if (value is True) or (value is False):
                b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
                b.hot_water = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'cold_water':
            if (value is True) or (value is False):
                b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
                b.cold_water = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'lift':
            if (value is True) or (value is False):
                b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
                b.lift = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'furniture':
            if (value is True) or (value is False):
                rt = FlatsRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
                rt.furniture = value
                rt.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'washing_machine':
            if (value is True) or (value is False):
                rt = FlatsRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
                rt.washing_machine = value
                rt.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'refrigerator':
            if (value is True) or (value is False):
                rt = FlatsRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
                rt.refrigerator = value
                rt.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'conditioner':
            if (value is True) or (value is False):
                rt = FlatsRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
                rt.conditioner = value
                rt.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'tv':
            if (value is True) or (value is False):
                rt = FlatsRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
                rt.tv = value
                rt.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'home_theater':
            if (value is True) or (value is False):
                rt = FlatsRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
                rt.home_theater = value
                rt.save(force_update=True)
                return
            else:
                raise ValueError()


        # text
        elif field == 'add_facilities':
            b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
            if not value:
                b.add_facilities = u''
                b.save(force_update=True)
                return
            else:
                value = format_text(value)
                b.add_facilities = value
                b.save(force_update=True)
                return value


        # boolean
        elif field == 'phone':
            if (value is True) or (value is False):
                b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
                b.phone = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'mobile_coverage':
            if (value is True) or (value is False):
                b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
                b.mobile_coverage = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'internet':
            if (value is True) or (value is False):
                b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
                b.internet = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'cable_tv':
            if (value is True) or (value is False):
                b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
                b.cable_tv = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'garage':
            if (value is True) or (value is False):
                b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
                b.garage = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'playground':
            if (value is True) or (value is False):
                b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
                b.playground = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # text
        elif field == 'add_buildings':
            b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]
            if not value:
                b.add_buildings= u''
                b.save(force_update=True)
                return
            else:
                value = format_text(value)
                b.add_buildings = value
                b.save(force_update=True)
                return value


        # text
        elif field == 'lat_lng':
            h.set_lat_lng(value)
            return


        # text
        elif field == 'address':
            b = FlatsBodies.objects.filter(id=h.body_id).only('id')[0]

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
            raise ValueError()

    except (DatabaseError, IntegrityError, InvalidOperation, ValueError) as e:
        raise ValueError(u'Field update error. Prefix: {0}. Value = {1}; Message: {2};'.format(
            unicode(field), unicode(value), e.message
        ))