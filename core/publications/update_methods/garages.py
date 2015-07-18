#coding=utf-8
from decimal import InvalidOperation
from collective.methods.formatters import format_text, format_title

from django.db import DatabaseError, IntegrityError

from core.currencies.constants import CURRENCIES
from core.publications.constants import MARKET_TYPES, COMMERCIAL_RENT_PERIODS, SALE_TRANSACTION_TYPES
from core.publications.models import GaragesBodies, GaragesRentTerms, GaragesSaleTerms
from core.publications.objects_constants.garages import GARAGE_DRIVE_WAYS



# Оновлює інформацію про гараж.
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

def update_garage(h, field, value, tid):
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
                st = GaragesSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
                st.price = None
                st.save(force_update=True)
                return
            else:
                value = round(float(value.replace(',', '.')), 2)
                if value <= 0:
                    raise ValueError()

                st = GaragesSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
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

            st = GaragesSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
            st.transaction_sid = value
            st.save(force_update=True)
            return


        # sid
        elif field == 'sale_currency_sid':
            value = int(value)
            if value not in CURRENCIES.values():
                raise ValueError()

            st = GaragesSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
            st.currency_sid = value
            st.save(force_update=True)
            return


        # bool
        elif field == 'sale_is_contract':
            if (value is True) or (value is False):
                st = GaragesSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
                st.is_contract = value
                st.save(force_update=True)
                return
            else:
                raise ValueError()


        # text
        elif field == 'sale_add_terms':
            st = GaragesSaleTerms.objects.filter(id=h.sale_terms_id).only('id')[0]
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


        # sid
        elif field == 'rent_period_sid':
            value = int(value)
            if value not in COMMERCIAL_RENT_PERIODS.values():
                raise ValueError()

            rt = GaragesRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
            rt.period_sid = value
            rt.save(force_update=True)
            return


        # blank or decimal
        elif field == 'rent_price':
            if not value:
                rt = GaragesRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
                rt.price = None
                rt.save(force_update=True)

            else:
                value = round(float(value.replace(',','.')), 2)
                if value <= 0:
                    raise ValueError()

                rt = GaragesRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
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

            rt = GaragesRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
            rt.currency_sid = value
            rt.save(force_update=True)
            return


        # boolean
        elif field == 'rent_is_contract':
            if (value is True) or (value is False):
                rt = GaragesRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
                rt.is_contract = value
                rt.save(force_update=True)
                return
            else:
                raise ValueError()


        # text
        elif field == 'rent_add_terms':
            rt = GaragesRentTerms.objects.filter(id=h.rent_terms_id).only('id')[0]
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
        elif field == 'title':
            b = GaragesBodies.objects.filter(id=h.body_id).only('id')[0]
            if not value:
                b.title = u''
                b.save(force_update=True)
                return
            else:
                value = format_title(value)
                b.title = value
                b.save(force_update=True)
                return value


        # text
        elif field == 'description':
            b = GaragesBodies.objects.filter(id=h.body_id).only('id')[0]
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

            b = GaragesBodies.objects.filter(id=h.body_id).only('id')[0]
            b.market_type_sid = value
            b.save(force_update=True)
            return


        # blank or float
        elif field == 'area':
            if not value:
                b = GaragesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.area = None
                b.save(force_update=True)
                return
            else:
                value = round(float(value.replace(',', '.')), 2)
                if value <= 0:
                    raise ValueError()

                b = GaragesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.area = value
                b.save(force_update=True)

                if int(value) == value:
                    # Відсікти дробову частину, якщо після коми нулі
                    return "%.0f" % value
                else:
                    # Скоротити / розширити до 2х цифр після коми
                    return "%.2f" % value


        # blank or float
        elif field == 'ceiling_height':
            if not value:
                b = GaragesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.ceiling_height = None
                b.save(force_update=True)
                return
            else:
                value = round(float(value.replace(',', '.')), 2)
                if value <= 0:
                    raise ValueError()

                b = GaragesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.ceiling_height = value
                b.save(force_update=True)

                if int(value) == value:
                    # Відсікти дробову частину, якщо після коми нулі
                    return "%.0f" % value
                else:
                    # скоротити / розширити до 2х цифр після коми
                    return "%.2f" % value


        # boolean
        elif field == 'pit':
            if (value is True) or (value is False):
                b = GaragesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.pit = value
                b.save(force_update=True)
                return
            else:
                raise ValueError('Invalid pit value.')


        # sid
        elif field == 'driveways_sid':
            value = int(value)
            if value not in GARAGE_DRIVE_WAYS.values():
                raise ValueError('Invalid driveways sid')

            b = GaragesBodies.objects.filter(id=h.body_id).only('id')[0]
            b.driveways_sid = value
            b.save(force_update=True)
            return


        # boolean
        elif field == 'electricity':
            if (value is True) or (value is False):
                b = GaragesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.electricity = value
                b.save(force_update=True)
                return
            else:
                raise ValueError('Invalid electricity value.')


        # boolean
        elif field == 'gas':
            if (value is True) or (value is False):
                b = GaragesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.gas = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'security_alarm':
            if (value is True) or (value is False):
                b = GaragesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.security_alarm = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'fire_alarm':
            if (value is True) or (value is False):
                b = GaragesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.fire_alarm = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'hot_water':
            if (value is True) or (value is False):
                b = GaragesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.hot_water = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'cold_water':
            if (value is True) or (value is False):
                b = GaragesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.cold_water = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'ventilation':
            if (value is True) or (value is False):
                b = GaragesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.ventilation = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()


        # boolean
        elif field == 'security':
            if (value is True) or (value is False):
                b = GaragesBodies.objects.filter(id=h.body_id).only('id')[0]
                b.security = value
                b.save(force_update=True)
                return
            else:
                raise ValueError()



        # text
        elif field == 'add_facilities':
            b = GaragesBodies.objects.filter(id=h.body_id).only('id')[0]
            if not value:
                b.add_facilities = u''
                b.save(force_update=True)
                return
            else:
                value = format_text(value)
                b.add_facilities = value
                b.save(force_update=True)
                return


        # text
        elif field == 'lat_lng':
            h.set_lat_lng(value)
            return


        # text
        elif field == 'address':
            if not value:
                h.address = u''
                h.save(force_update=True)
                return
            else:
                # note: адреса не форматується, оскільки не можливо передбачити,
                # як саме користувач її введе.
                h.address = value
                h.save(force_update=True)
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