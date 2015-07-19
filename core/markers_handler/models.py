# coding=utf-8
import math
from django.conf import settings

from django.db import models, connections
from django.db.models import Q
from djorm_pgarray.fields import BigIntegerArrayField
from collective.exceptions import InvalidArgument
from core.currencies.constants import CURRENCIES
from core.currencies.currencies_manager import convert as convert_price
from core.markers_handler.classes import Grid
from core.publications.constants import \
    OBJECTS_TYPES, MARKET_TYPES, FLOOR_TYPES, HEATING_TYPES, LIVING_RENT_PERIODS, HEAD_MODELS
from core.publications.objects_constants.flats import FLAT_ROOMS_PLANNINGS
from core.publications.objects_constants.trades import TRADE_BUILDING_TYPES


class AbstractBaseIndex(models.Model):
    """
    В даному модулі індекс це — таблиця, яка містить всі необхідні поля для того,
    щоб забезпечити роботу фільтрів, передбачених логікою фронтенда.

    Абсолютна більшість полів даної таблиці індексуються B-Tree індексом (в django за замовчуванням).
    Перенасичення таблиці індексами в даному випадку не розглядається як проблема, оскільки
        * передбачається, що всі похідні таблиці (тобто всі індекси для кожного з типів)
          будуть обслуговуватись окремим сервером PostgreSQL в якому буде вимкнено ACID,
          за рахунок чого, вставка в дані таблиці повинна відбуватись досить швидко.

          Дані в індексі дублюватимуть дані з основних таблиць, тому втрата навіть всього індексу
          не веде до проблем, оскільки індекс в будь-який момент може бути перебудований
          ціної декількох годин процесорного часу.

        * неможливо з необхідним рівнем достовірності спрогнозувати які саме фільтри
          буде використовувати середньо-статистинчий користувач. Як наслідок — для забепечення ефективної
          роботи фільтрів за таких умов слід індексувати кожне поле, по якому може йти вибірка.
          Проактивна оптимізація з метою побудови такої системи, яка швидше працює лише за певного,
          наперед визначеного спектру запитів веде до необгрунтованого ускладення алгоритмів системи в цілому
          і тому в даній задачі не розглядаєаться як потенційне рішення.
    """

    # publication_id умисно не помічено за первинний ключ.
    # Для індекса не критично якщо час-від-часу в ньому виникатимуть дублі записів.
    # Більш критичним є неможливість користувача опублікувати оголошення через потенційно можливий конфлікт
    # із уже існуючим записом в індексі.
    #
    # Така ситуація достатньо вірогідна через те, що довелось змішати чистий sql з django-orm,
    # через що порушився механізм транзакцій (зараз транзакцій як таких немає).
    publication_id = models.PositiveIntegerField()
    hash_id = models.TextField()

    # lat, lng дублюються в індексі щоб уникнути зайвого join-а з таблицею даних по оголошеннях.
    # Аналогічним чином дублюються всі дані, які, так чи інакше, формують видачу по фільтрах,
    # в тому числі в дочірніх індексах.
    lat = models.FloatField()
    lng = models.FloatField()


    class Meta:
        abstract = True


    class Filters(object):
        class RoomsPlanning(object):
            any = 0
            free = 1
            preliminary = 2


    @classmethod
    def remove(cls, hid, using=None):
        cls.objects.using(using).filter(publication_id=hid).delete()


    @classmethod
    def brief_queryset(cls):  # virtual
        """
        :returns:
            minimum queryset needed for marker brief performing.
        """
        return cls.objects.all().only('publication_id', 'hash_id', 'lat', 'lng', 'price', 'currency_sid')


    @classmethod
    def brief(cls, marker, filters=None):
        currency = cls.currency_from_filters(filters)
        price = cls.convert_and_format_price(marker.price, marker.currency_sid, currency)

        return {
            'tid': cls.tid,
            'id': marker.hash_id,
            'price': u'{0} {1}'.format(price, cls.currency_to_str(currency)),
        }


    @classmethod
    def min_add_queryset(cls):  # virtual
        """
        :return:
            Мінімальний QuerySet моделі, до якої прив’язаний індекс.
            Тобто, якщо це FlatsSaleIndex то буде повернуто QuerySet оголошень FlatsHeads,
            якщо HousesRentIndexAbstract - HousesHeads і т.д.

            Також, даний метод вибирає лише ті поля,
            які використовуються під час додавання оголошення в індекс.
            Саме тому даний метод перевизначається у всіх дочірніх індексах,
            щоб була можливість вказувати специфічний набір полів під конкретний індекс.
        """
        raise Exception('Abstract method was called.')


    @classmethod
    def min_remove_queryset(cls):
        model = HEAD_MODELS[cls.tid]
        return model.objects.all().only(
            'id',
            'degree_lat',
            'degree_lng',
            'segment_lat',
            'segment_lng',
            'pos_lat',
            'pos_lng',
        )


    @staticmethod
    def convert_and_format_price(price, base_currency, destination_currency):
        """
        Поверне рядок з ціною price сконвертованою з валюти base_currency у валюту destination_currency.
        Якщо валюти base_currency та destination_currency відмінні — перед результатом буде додано "≈",
        як індикатор того, що ціна в отриманій валюті приблизна.
        """
        converted_price = convert_price(price, base_currency, destination_currency)
        converted_price = int(converted_price)  # копійок в кінці ціни нам не потрібно
        result = u'{0}'.format(converted_price).replace(',', ' ')  # форматування на наш лад

        if base_currency != destination_currency:
            return u'≈' + result
        return result


    @staticmethod
    def currency_to_str(currency):
        if currency == CURRENCIES.dol():
            return u'дол.'
        elif currency == CURRENCIES.uah():
            return u'грн.'
        elif currency == CURRENCIES.eur():
            return u'евро'
        else:
            raise InvalidArgument('Invalid currency.')


    @staticmethod
    def currency_from_filters(filters):
        # Гривня як базова валюта обирається згідно з чинним законодавством,
        # але якщо у фільтрі вказана інша валюта - переформатувати бриф на неї.
        if filters is None:
            return CURRENCIES.uah()

        return int(filters.get('cu_sid', CURRENCIES.uah()))


    # -- filters methods

    @classmethod  # range
    def apply_price_filter(cls, filters, markers):
        currency = cls.currency_from_filters(filters)

        price_min = filters.get('p_min')
        if price_min:
            markers = markers.filter(
                Q(
                    Q(
                        price__gte=convert_price(price_min, currency, CURRENCIES.dol()),
                        currency_sid=CURRENCIES.dol()
                    ) | Q(
                        price__gte=convert_price(price_min, currency, CURRENCIES.eur()),
                        currency_sid=CURRENCIES.eur()
                    ) | Q(
                        price__gte=convert_price(price_min, currency, CURRENCIES.uah()),
                        currency_sid=CURRENCIES.uah()
                    )
                )
            )

        price_max = filters.get('p_max')
        if price_max:
            markers = markers.filter(
                Q(
                    Q(
                        price__lte=convert_price(price_max, currency, CURRENCIES.dol()),
                        currency_sid=CURRENCIES.dol()
                    ) | Q(
                        price__lte=convert_price(price_max, currency, CURRENCIES.eur()),
                        currency_sid=CURRENCIES.eur()
                    ) | Q(
                        price__lte=convert_price(price_max, currency, CURRENCIES.uah()),
                        currency_sid=CURRENCIES.uah()
                    )
                )
            )

        return markers


    @staticmethod  # range
    def apply_area_filter(filters, markers):
        # This filter si similar to the total area.
        # Some objects types has attribute "area" instead of "total_area",
        # so we need method to process them.

        a_min = filters.get('a_min')
        if a_min is not None:
            markers = markers.filter(area__gte=a_min)

        a_max = filters.get('a_max')
        if a_max is not None:
            markers = markers.filter(area__lte=a_max)

        return markers


    @staticmethod  # range
    def apply_total_area_filter(filters, markers):
        # This filter si similar to the total area.
        # Some objects types has attribute "total_area" instead of "area",
        # so we need method to process them.

        ta_min = filters.get('t_a_min')
        if ta_min is not None:
            markers = markers.filter(total_area__gte=ta_min)

        ta_max = filters.get('t_a_max')
        if ta_max is not None:
            markers = markers.filter(total_area__lte=ta_max)

        return markers


    @staticmethod  # range
    def apply_halls_area_filter(filters, markers):
        ha_min = filters.get('h_a_min')
        if ha_min is not None:
            markers = markers.filter(halls_area__gte=ha_min)

        ha_max = filters.get('h_a_max')
        if ha_max is not None:
            markers = markers.filter(halls_area__lte=ha_max)

        return markers


    @staticmethod  # range
    def apply_floor_filter(filters, markers):
        floor_min = filters.get('f_min')
        if floor_min is not None:
            markers = markers.filter(floor__gte=floor_min)

        floor_max = filters.get('f_max')
        if floor_max is not None:
            markers = markers.filter(floor_lte=floor_max)

        if 'msd' in filters and not 'grd' in filters: # grd: ground, msd: mansard
            markers = markers.exclude(floor_type_sid=FLOOR_TYPES.mansard())

        if 'grd' in filters and not 'msd' in filters: # grd: ground, msd: mansard
            markers = markers.exclude(floor_type_sid=FLOOR_TYPES.ground())

        return markers


    @staticmethod  # range
    def apply_floors_count_filter(filters, markers):
        floor_min = filters.get('f_c_min')
        if floor_min is not None:
            markers = markers.filter(floors_count__gte=floor_min)

        floor_max = filters.get('f_c_max')
        if floor_max is not None:
            markers = markers.filter(floors_count__lte=floor_max)

        return markers


    @staticmethod  # range
    def apply_ceiling_height_filter(filters, markers):
        height_min = filters.get('c_h_min')
        if height_min is not None:
            markers = markers.filter(ceiling_height__gte=height_min)

        height_max = filters.get('c_h_max')
        if height_max is not None:
            markers = markers.filter(ceiling_height__lte=height_max)

        return markers


    @staticmethod  # range
    def apply_rooms_count_filter(filters, markers):
        rooms_count_min = filters.get('r_c_min')
        if rooms_count_min is not None:
            markers = markers.filter(rooms_count__gte=rooms_count_min)

        rooms_count_max = filters.get('r_c_max')
        if rooms_count_max is not None:
            markers = markers.filter(rooms_count__lte=rooms_count_max)

        return markers


    @staticmethod  # range
    def apply_persons_count_filter(filters, markers):
        count_min = filters.get('p_c_min')
        if count_min is not None:
            markers = markers.filter(persons_count__gte=count_min)

        count_max = filters.get('p_c_max')
        if count_max is not None:
            markers = markers.filter(persons_count__lte=count_max)

        return markers


    @staticmethod  # range
    def apply_cabinets_count_filter(filters, markers):
        count_min = filters.get('c_c_min')
        if count_min is not None:
            markers = markers.filter(cabinets_count__gte=count_min)

        count_max = filters.get('c_c_max')
        if count_max is not None:
            markers = markers.filter(cabinets_count__gte=count_max)

        return markers


    @staticmethod  # sid
    def apply_living_rent_period_filter(filters, markers):
        period = int(filters.get('pr_sid'))
        if period == 1:
            markers = markers.filter(period_sid=LIVING_RENT_PERIODS.daily())

        elif period == 2:
            markers = markers.filter(period_sid=LIVING_RENT_PERIODS.monthly())

        return markers


    @staticmethod  # sid
    def apply_market_type_filter(filters, markers):
        if 'n_b' in filters and not 's_m' in filters:
            markers = markers.filter(market_type_sid=MARKET_TYPES.new_building())

        elif 's_m' in filters and not 'n_b' in filters:
            markers = markers.filter(market_type_sid=MARKET_TYPES.secondary_market())

        return markers


    @classmethod  # sid
    def apply_rooms_planning_filter(cls, filters, markers):
        rooms_planning_sid = int(filters.get('pl_sid'))

        if rooms_planning_sid == cls.Filters.RoomsPlanning.free:
            markers = markers.filter(rooms_planning_sid=FLAT_ROOMS_PLANNINGS.free())
        elif rooms_planning_sid == cls.Filters.RoomsPlanning.preliminary:
            markers = markers.exclude(rooms_planning_sid=FLAT_ROOMS_PLANNINGS.free()) # note: exclude here!

        return markers


    @staticmethod # sid
    def apply_trade_building_type_filter(filters, markers):
        building_type = int(filters.get('b_t_sid'))

        if building_type == 1:
            markers = markers.filter(building_type_sid=TRADE_BUILDING_TYPES.entertainment())
        elif building_type == 2:
            markers = markers.filter(building_type_sid=TRADE_BUILDING_TYPES.business())
        elif building_type == 3:
            markers = markers.filter(building_type_sid=TRADE_BUILDING_TYPES.separate())

        return markers


    @staticmethod  # sid
    def apply_heating_type_filter(filters, markers):
        heating = int(filters.get('h_t_sid'))

        if heating == 1:
            markers = markers.filter(heating_type_sid=HEATING_TYPES.central())
        elif heating == 2:
            markers = markers.filter(heating_type_sid=HEATING_TYPES.individual())
        elif heating == 3:
            markers = markers.filter(heating_type_sid=HEATING_TYPES.none())

        return markers


    @staticmethod  # bool
    def apply_electricity_filter(filters, markers):
        if 'elt' in filters:
            return markers.filter(electricity=True)
        return markers


    @staticmethod  # bool
    def apply_gas_filter(filters, markers):
        if 'gas' in filters:
            return markers.filter(gas=True)
        return markers


    @staticmethod  # bool
    def apply_hot_water_filter(filters, markers):
        if 'h_w' in filters:
            return markers.filter(hot_water=True)
        return markers


    @staticmethod  # bool
    def apply_cold_water_filter(filters, markers):
        if 'c_w' in filters:
            return markers.filter(cold_water=True)
        return markers


    @staticmethod  # bool
    def apply_water_filter(filters, markers):
        if 'wtr' in filters:
            return markers.filter(water=True)
        return markers


    @staticmethod  # bool
    def apply_sewerage_filter(filters, markers):
        if 'swg' in filters:
            return markers.filter(sewerage=True)
        return markers


    @staticmethod  # bool
    def apply_lift_filter(filters, markers):
        if 'lft' in filters:
            return markers.filter(lift=True)
        return markers


    @staticmethod  # bool
    def apply_family_filter(filters, markers):
        if 'fml' in filters:
            return markers.filter(family=True)
        return markers


    @staticmethod  # bool
    def apply_foreigners_filter(filters, markers):
        if 'frg' in filters:
            return markers.filter(foreigners=True)
        return markers


    @staticmethod  # bool
    def apply_security_filter(filters, markers):
        if 'sct' in filters:
            return markers.filter(security=True)
        return markers


    @staticmethod  # bool
    def apply_kitchen_filter(filters, markers):
        if 'ktn' in filters:
            return markers.filter(kitchen=True)
        return markers


    @staticmethod  # bool
    def apply_fire_alarm_filter(filters, markers):
        if 'f_a' in filters:
            return markers.filter(fire_alarm=True)
        return markers


    @staticmethod  # bool
    def apply_security_alarm_filter(filters, markers):
        if 's_a' in filters:
            return markers.filter(security_alarm=True)
        return markers


    @staticmethod  # bool
    def apply_pit_filter(filters, markers):
        if 'pit' in filters:
            return markers.filter(pit=True)
        return markers



class FlatsSaleIndex(AbstractBaseIndex):
    # constants
    tid = OBJECTS_TYPES.flat()

    price = models.FloatField(db_index=True)
    currency_sid = models.PositiveSmallIntegerField()

    market_type_sid = models.PositiveSmallIntegerField(db_index=True)
    rooms_count = models.PositiveSmallIntegerField(db_index=True)
    rooms_planning_sid = models.PositiveSmallIntegerField(db_index=True)
    total_area = models.FloatField(db_index=True)
    floor = models.PositiveSmallIntegerField(db_index=True)
    floor_type_sid = models.PositiveSmallIntegerField(db_index=True)
    lift = models.BooleanField(db_index=True)
    hot_water = models.BooleanField(db_index=True)
    cold_water = models.BooleanField(db_index=True)
    gas = models.BooleanField(db_index=True)
    electricity = models.BooleanField(db_index=True)
    heating_type_sid = models.PositiveSmallIntegerField(db_index=True)


    class Meta:
        db_table = 'index_flats_sale'


    @classmethod
    def add(cls, record, using=None):
        cls.objects.using(using).create(
            publication_id=record.id,
            hash_id=record.hash_id,
            lat=float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
            lng=float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

            price=record.sale_terms.price,
            currency_sid=record.sale_terms.currency_sid,

            market_type_sid=record.body.market_type_sid,
            rooms_count=record.body.rooms_count,
            rooms_planning_sid=record.body.rooms_planning_sid,
            total_area=record.body.total_area,
            floor=record.body.floor,
            floor_type_sid=record.body.floor_type_sid,
            lift=record.body.lift,
            hot_water=record.body.hot_water,
            cold_water=record.body.cold_water,
            gas=record.body.gas,
            electricity=record.body.electricity,
            heating_type_sid=record.body.heating_type_sid,
        )


    @classmethod
    def brief_queryset(cls):
        return cls.objects.all().only('publication_id', 'hash_id', 'lat', 'lng', 'price', 'currency_sid')


    @classmethod
    def min_add_queryset(cls):
        model = HEAD_MODELS[OBJECTS_TYPES.flat()]
        return model.objects.all().only(
            'id',
            'hash_id',
            'degree_lat',
            'degree_lng',
            'segment_lat',
            'segment_lng',
            'pos_lat',
            'pos_lng',

            'sale_terms__price',
            'sale_terms__currency_sid',

            'body__market_type_sid',
            'body__rooms_count',
            'body__rooms_planning_sid',
            'body__total_area',
            'body__floor',
            'body__floor_type_sid',
            'body__lift',
            'body__hot_water',
            'body__cold_water',
            'body__gas',
            'body__electricity',
            'body__heating_type_sid',
        )


    @classmethod
    def apply_filters(cls, filters, markers):
        cls.apply_price_filter(filters, markers)

        cls.apply_market_type_filter(filters, markers)
        cls.apply_rooms_count_filter(filters, markers)
        cls.apply_rooms_planning_filter(filters, markers)
        cls.apply_total_area_filter(filters, markers)
        cls.apply_floor_filter(filters, markers)
        cls.apply_electricity_filter(filters, markers)
        cls.apply_gas_filter(filters, markers)
        cls.apply_hot_water_filter(filters, markers)
        cls.apply_cold_water_filter(filters, markers)
        cls.apply_lift_filter(filters, markers)
        cls.apply_heating_type_filter(filters, markers)
        return markers



class FlatsRentIndex(AbstractBaseIndex):
    price = models.FloatField(db_index=True)
    currency_sid = models.PositiveSmallIntegerField()
    persons_count = models.PositiveSmallIntegerField(db_index=True)
    period_sid = models.PositiveSmallIntegerField(db_index=True)

    market_type_sid = models.PositiveSmallIntegerField(db_index=True)
    rooms_count = models.PositiveSmallIntegerField(db_index=True)
    rooms_planning_sid = models.PositiveSmallIntegerField(db_index=True)
    total_area = models.FloatField(db_index=True)
    floor = models.PositiveSmallIntegerField(db_index=True)
    floor_type_sid = models.PositiveSmallIntegerField(db_index=True)
    lift = models.BooleanField(db_index=True)
    hot_water = models.BooleanField(db_index=True)
    cold_water = models.BooleanField(db_index=True)
    gas = models.BooleanField(db_index=True)
    electricity = models.BooleanField(db_index=True)
    heating_type_sid = models.PositiveSmallIntegerField(db_index=True)


    # constants
    tid = OBJECTS_TYPES.flat()


    class Meta:
        db_table = 'index_flats_rent'


    @classmethod
    def add(cls, record, using=None):
        cls.objects.using(using).create(
            publication_id=record.id,
            hash_id=record.hash_id,
            lat=float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
            lng=float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

            period_sid=record.rent_terms.period_sid,
            price=record.rent_terms.price,
            currency_sid=record.rent_terms.currency_sid,
            persons_count=record.rent_terms.persons_count,

            market_type_sid=record.body.market_type_sid,
            rooms_count=record.body.rooms_count,
            rooms_planning_sid=record.body.rooms_planning_sid,
            total_area=record.body.total_area,
            floor=record.body.floor,
            floor_type_sid=record.body.floor_type_sid,
            lift=record.body.lift,
            hot_water=record.body.hot_water,
            cold_water=record.body.cold_water,
            gas=record.body.gas,
            electricity=record.body.electricity,
            heating_type_sid=record.body.heating_type_sid,
        )


    @classmethod
    def min_add_queryset(cls):
        model = HEAD_MODELS[OBJECTS_TYPES.flat()]
        return model.objects.all().only(
            'id',
            'hash_id',
            'degree_lat',
            'degree_lng',
            'segment_lat',
            'segment_lng',
            'pos_lat',
            'pos_lng',

            'rent_terms__price',
            'rent_terms__currency_sid',
            'rent_terms__period_sid',
            'rent_terms__persons_count',

            'body__market_type_sid',
            'body__rooms_count',
            'body__rooms_planning_sid',
            'body__total_area',
            'body__floor',
            'body__floor_type_sid',
            'body__lift',
            'body__hot_water',
            'body__cold_water',
            'body__gas',
            'body__electricity',
            'body__heating_type_sid',
        )


    @classmethod
    def apply_filters(cls, filters, markers):
        cls.apply_price_filter(filters, markers)
        cls.apply_living_rent_period_filter(filters, markers)
        cls.apply_persons_count_filter(filters, markers)

        cls.apply_market_type_filter(filters, markers)
        cls.apply_rooms_count_filter(filters, markers)
        cls.apply_rooms_planning_filter(filters, markers)
        cls.apply_total_area_filter(filters, markers)
        cls.apply_floor_filter(filters, markers)
        cls.apply_electricity_filter(filters, markers)
        cls.apply_gas_filter(filters, markers)
        cls.apply_hot_water_filter(filters, markers)
        cls.apply_cold_water_filter(filters, markers)
        cls.apply_lift_filter(filters, markers)
        cls.apply_heating_type_filter(filters, markers)
        return markers


class HousesSaleIndex(AbstractBaseIndex):
    market_type_sid = models.PositiveSmallIntegerField(db_index=True)
    price = models.FloatField(db_index=True)
    currency_sid = models.PositiveSmallIntegerField()
    total_area = models.FloatField(db_index=True)
    rooms_count = models.PositiveSmallIntegerField(db_index=True)
    floors_count = models.PositiveSmallIntegerField(db_index=True)
    hot_water = models.BooleanField(db_index=True)
    cold_water = models.BooleanField(db_index=True)
    gas = models.BooleanField(db_index=True)
    electricity = models.BooleanField(db_index=True)
    sewerage = models.BooleanField(db_index=True)
    heating_type_sid = models.PositiveSmallIntegerField(db_index=True)


    tid = OBJECTS_TYPES.house()


    class Meta:
        db_table = 'index_houses_sale'


    @classmethod
    def add(cls, record, using=None):
        cls.objects.using(using).create(
            publication_id=record.id,
            hash_id=record.hash_id,
            lat=float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
            lng=float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

            market_type_sid=record.body.market_type_sid,
            price=record.sale_terms.price,
            currency_sid=record.sale_terms.currency_sid,
            total_area=record.body.total_area,
            rooms_count=record.body.rooms_count,
            floors_count=record.body.floors_count,
            hot_water=record.body.hot_water,
            cold_water=record.body.cold_water,
            gas=record.body.gas,
            electricity=record.body.electricity,
            sewerage=record.body.sewerage,
            heating_type_sid=record.body.heating_type_sid,
        )


    @classmethod
    def brief_queryset(cls):
        return cls.objects.all().only(
            'publication_id', 'hash_id', 'lat', 'lng', 'price', 'currency_sid', 'total_area')


    @classmethod
    def min_add_queryset(cls):
        model = HEAD_MODELS[OBJECTS_TYPES.house()]
        return model.objects.all().only(
            'degree_lat',
            'degree_lng',
            'segment_lat',
            'segment_lng',
            'pos_lat',
            'pos_lng',

            'id',
            'hash_id',

            'body__market_type_sid',
            'body__total_area',
            'body__rooms_count',
            'body__floors_count',
            'body__hot_water',
            'body__cold_water',
            'body__electricity',
            'body__gas',
            'body__sewerage',
            'body__heating_type_sid',

            'sale_terms__price',
            'sale_terms__currency_sid'
        )


    @classmethod
    def min_remove_queryset(cls):
        model = HEAD_MODELS[cls.tid]
        return model.objects.all().only(
            'id',

            'degree_lat',
            'degree_lng',
            'segment_lat',
            'segment_lng',
            'pos_lat',
            'pos_lng',
        )


    @classmethod
    def apply_filters(cls, filters, markers):
        markers = cls.apply_price_filter(filters, markers)
        markers = cls.apply_market_type_filter(filters, markers)
        markers = cls.apply_total_area_filter(filters, markers)
        markers = cls.apply_rooms_count_filter(filters, markers)
        markers = cls.apply_floors_count_filter(filters, markers)
        markers = cls.apply_electricity_filter(filters, markers)
        markers = cls.apply_gas_filter(filters, markers)
        markers = cls.apply_hot_water_filter(filters, markers)
        markers = cls.apply_cold_water_filter(filters, markers)
        markers = cls.apply_sewerage_filter(filters, markers)
        markers = cls.apply_heating_type_filter(filters, markers)
        return markers


    @classmethod
    def brief(cls, marker, filters=None):
        currency = cls.currency_from_filters(filters)
        price = cls.convert_and_format_price(marker.price, marker.currency_sid, currency)
        total_area = '{0}'.format(marker.total_area).rstrip('0').rstrip('.')

        return {
            'tid': cls.tid,
            'id': marker.hash_id,
            'd0': u'{0} м²'.format(total_area),
            'd1': u'{0} {1}'.format(price, cls.currency_to_str(currency)),
        }



class HousesRentIndex(AbstractBaseIndex):
    period_sid = models.PositiveSmallIntegerField(db_index=True)
    price = models.FloatField(db_index=True)
    currency_sid = models.PositiveSmallIntegerField()

    # houses may not have persons count set
    persons_count = models.PositiveSmallIntegerField(db_index=True, null=True, blank=True)
    total_area = models.FloatField(db_index=True)
    family = models.BooleanField(db_index=True)
    foreigners = models.BooleanField(db_index=True)
    hot_water = models.BooleanField(db_index=True)
    cold_water = models.BooleanField(db_index=True)
    gas = models.BooleanField(db_index=True)
    electricity = models.BooleanField(db_index=True)
    sewerage = models.BooleanField(db_index=True)


    # cosntants
    tid = OBJECTS_TYPES.house()


    class Meta:
        db_table = 'index_houses_rent'


    @classmethod
    def add(cls, record, using=None):
        cls.objects.using(using).create(
            publication_id=record.id,
            hash_id=record.hash_id,
            lat=float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
            lng=float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

            period_sid=record.rent_terms.period_sid,
            price=record.rent_terms.price,
            currency_sid=record.rent_terms.currency_sid,
            persons_count=record.rent_terms.persons_count,
            family=record.rent_terms.family,
            foreigners=record.rent_terms.foreigners,

            total_area=record.body.total_area,
            hot_water=record.body.hot_water,
            cold_water=record.body.cold_water,
            gas=record.body.gas,
            electricity=record.body.electricity,
            sewerage=record.body.sewerage,
        )


    @classmethod
    def brief_queryset(cls):
        return cls.objects.all().only(
            'publication_id', 'hash_id', 'lat', 'lng', 'price', 'currency_sid', 'persons_count')


    @classmethod
    def min_add_queryset(cls):
        model = HEAD_MODELS[OBJECTS_TYPES.house()]
        return model.objects.all().only(
            'degree_lat',
            'degree_lng',
            'segment_lat',
            'segment_lng',
            'pos_lat',
            'pos_lng',

            'id',
            'hash_id',

            'body__total_area',
            'body__hot_water',
            'body__cold_water',
            'body__gas',
            'body__electricity',
            'body__sewerage',

            'rent_terms__period_sid',
            'rent_terms__price',
            'rent_terms__currency_sid',
            'rent_terms__persons_count',
            'rent_terms__family',
            'rent_terms__foreigners',
        )


    @classmethod
    def min_remove_queryset(cls):
        model = HEAD_MODELS[cls.tid]
        return model.objects.all().only(
            'id',

            'degree_lat',
            'degree_lng',
            'segment_lat',
            'segment_lng',
            'pos_lat',
            'pos_lng',
        )


    @classmethod
    def apply_filters(cls, filters, markers):
        markers = cls.apply_price_filter(filters, markers)
        markers = cls.apply_living_rent_period_filter(filters, markers)
        markers = cls.apply_persons_count_filter(filters, markers)
        markers = cls.apply_total_area_filter(filters, markers)
        markers = cls.apply_family_filter(filters, markers)
        markers = cls.apply_foreigners_filter(filters, markers)
        markers = cls.apply_electricity_filter(filters, markers)
        markers = cls.apply_gas_filter(filters, markers)
        markers = cls.apply_hot_water_filter(filters, markers)
        markers = cls.apply_cold_water_filter(filters, markers)
        return markers


    @classmethod
    def brief(cls, marker, filters=None):
        currency = cls.currency_from_filters(filters)
        price = cls.convert_and_format_price(marker.price, marker.currency_sid, currency)

        return {
            'tid': cls.tid,
            'id': marker.hash_id,
            'd0': u'Мест {0}'.format(marker.persons_count),
            'd1': u'{0} {1}'.format(price, cls.currency_to_str(currency)),
        }



class RoomsSaleIndex(AbstractBaseIndex):
    price = models.FloatField(db_index=True)
    currency_sid = models.PositiveSmallIntegerField()
    market_type_sid = models.PositiveSmallIntegerField(db_index=True)
    rooms_count = models.PositiveSmallIntegerField(db_index=True)
    total_area = models.FloatField(db_index=True)
    floor = models.PositiveSmallIntegerField(db_index=True)
    floor_type_sid = models.PositiveSmallIntegerField(db_index=True)
    lift = models.BooleanField(db_index=True)
    hot_water = models.BooleanField(db_index=True)
    cold_water = models.BooleanField(db_index=True)
    gas = models.BooleanField(db_index=True)
    electricity = models.BooleanField(db_index=True)
    heating_type_sid = models.PositiveSmallIntegerField(db_index=True)


    #constants
    tid = OBJECTS_TYPES.room()


    class Meta:
        db_table = 'index_rooms_sale'


    @classmethod
    def add(cls, record, using=None):
        cls.objects.using(using).create(
            publication_id=record.id,
            hash_id=record.hash_id,
            lat=float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
            lng=float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

            market_type_sid=record.body.market_type_sid,
            rooms_count=record.body.rooms_count,
            total_area=record.body.total_area,
            floor=record.body.floor,
            floor_type_sid=record.body.floor_type_sid,
            lift=record.body.lift,
            hot_water=record.body.hot_water,
            cold_water=record.body.cold_water,
            electricity=record.body.electricity,
            gas=record.body.gas,
            heating_type_sid=record.body.heating_type_sid,

            price=record.sale_terms.price,
            currency_sid=record.sale_terms.currency_sid,
        )


    @classmethod
    def brief_queryset(cls):
        return cls.objects.all().only(
            'publication_id', 'hash_id', 'lat', 'lng', 'price', 'currency_sid', 'total_area')


    @classmethod
    def min_add_queryset(cls):
        model = HEAD_MODELS[OBJECTS_TYPES.room()]
        return model.objects.all().only(
            'degree_lat',
            'degree_lng',
            'segment_lat',
            'segment_lng',
            'pos_lat',
            'pos_lng',

            'id',
            'hash_id',

            'body__market_type_sid',
            'body__rooms_count',
            'body__total_area',
            'body__floor',
            'body__floor_type_sid',
            'body__lift',
            'body__hot_water',
            'body__cold_water',
            'body__electricity',
            'body__gas',
            'body__heating_type_sid',

            'sale_terms__price',
            'sale_terms__currency_sid',
        )


    @classmethod
    def min_remove_queryset(cls):
        model = HEAD_MODELS[cls.tid]
        return model.objects.all().only(
            'id',

            'degree_lat',
            'degree_lng',
            'segment_lat',
            'segment_lng',
            'pos_lat',
            'pos_lng',
        )


    @classmethod
    def apply_filters(cls, filters, markers):
        markers = cls.apply_price_filter(filters, markers)
        markers = cls.apply_market_type_filter(filters, markers)
        markers = cls.apply_rooms_count_filter(filters, markers)
        markers = cls.apply_total_area_filter(filters, markers)
        markers = cls.apply_floor_filter(filters, markers)
        markers = cls.apply_electricity_filter(filters, markers)
        markers = cls.apply_gas_filter(filters, markers)
        markers = cls.apply_hot_water_filter(filters, markers)
        markers = cls.apply_cold_water_filter(filters, markers)
        markers = cls.apply_lift_filter(filters, markers)
        markers = cls.apply_heating_type_filter(filters, markers)
        return markers


    @classmethod
    def brief(cls, marker, filters=None):
        currency = cls.currency_from_filters(filters)
        price = cls.convert_and_format_price(marker.price, marker.currency_sid, currency)
        total_area = '{0:.2f}'.format(marker.total_area).rstrip('0').rstrip('.')

        return {
            'tid': cls.tid,
            'id': marker.hash_id,
            'd0': u'Площадь: {0} м²'.format(total_area),
            'd1': u'{0} {1}'.format(price, cls.currency_to_str(currency)),
        }



class RoomsRentIndex(AbstractBaseIndex):
    period_sid = models.PositiveSmallIntegerField(db_index=True)
    price = models.FloatField(db_index=True)
    currency_sid = models.PositiveSmallIntegerField()
    persons_count = models.PositiveSmallIntegerField(db_index=True)
    total_area = models.FloatField(db_index=True)
    floor = models.PositiveSmallIntegerField(db_index=True)
    floor_type_sid = models.PositiveSmallIntegerField(db_index=True)
    family = models.BooleanField(db_index=True)
    foreigners = models.BooleanField(db_index=True)
    lift = models.BooleanField(db_index=True)
    hot_water = models.BooleanField(db_index=True)
    cold_water = models.BooleanField(db_index=True)
    gas = models.BooleanField(db_index=True)
    electricity = models.BooleanField(db_index=True)


    # constants
    tid = OBJECTS_TYPES.room()


    class Meta:
        db_table = 'index_rooms_rent'


    @classmethod
    def add(cls, record, using=None):
        cls.objects.using(using).create(
            publication_id=record.id,
            hash_id=record.hash_id,
            lat=float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
            lng=float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

            period_sid=record.rent_terms.period_sid,
            price=record.rent_terms.price,
            currency_sid=record.rent_terms.currency_sid,
            persons_count=record.rent_terms.persons_count,
            family=record.rent_terms.family,
            foreigners=record.rent_terms.foreigners,

            total_area=record.body.total_area,
            floor=record.body.floor,
            floor_type_sid=record.body.floor_type_sid,
            lift=record.body.lift,
            hot_water=record.body.hot_water,
            cold_water=record.body.cold_water,
            gas=record.body.gas,
            electricity=record.body.electricity,
        )


    @classmethod
    def brief_queryset(cls):
        return cls.objects.all().only(
            'publication_id', 'hash_id', 'lat', 'lng', 'price', 'currency_sid', 'persons_count')


    @classmethod
    def min_add_queryset(cls):
        model = HEAD_MODELS[OBJECTS_TYPES.room()]
        return model.objects.all().only(
            'degree_lat',
            'degree_lng',
            'segment_lat',
            'segment_lng',
            'pos_lat',
            'pos_lng',

            'id',
            'hash_id',

            'body__total_area',
            'body__floor',
            'body__floor_type_sid',
            'body__lift',
            'body__hot_water',
            'body__cold_water',
            'body__gas',
            'body__electricity',

            'rent_terms__period_sid',
            'rent_terms__price',
            'rent_terms__currency_sid',
            'rent_terms__persons_count',
            'rent_terms__family',
            'rent_terms__foreigners',
        )


    @classmethod
    def min_remove_queryset(cls):
        model = HEAD_MODELS[cls.tid]
        return model.objects.all().only(
            'id',

            'degree_lat',
            'degree_lng',
            'segment_lat',
            'segment_lng',
            'pos_lat',
            'pos_lng',
        )


    @classmethod
    def apply_filters(cls, filters, markers):
        markers = cls.apply_living_rent_period_filter(filters, markers)
        markers = cls.apply_price_filter(filters, markers)
        markers = cls.apply_persons_count_filter(filters, markers)
        markers = cls.apply_total_area_filter(filters, markers)
        markers = cls.apply_floor_filter(filters, markers)
        markers = cls.apply_family_filter(filters, markers)
        markers = cls.apply_foreigners_filter(filters, markers)
        markers = cls.apply_electricity_filter(filters, markers)
        markers = cls.apply_gas_filter(filters, markers)
        markers = cls.apply_hot_water_filter(filters, markers)
        markers = cls.apply_cold_water_filter(filters, markers)
        markers = cls.apply_lift_filter(filters, markers)
        return markers


    @classmethod
    def brief(cls, marker, filters=None):
        currency = cls.currency_from_filters(filters)
        price = cls.convert_and_format_price(marker.price, marker.currency_sid, currency)

        return {
            'tid': cls.tid,
            'id': marker.hash_id,
            'd0': u'Мест: {0}'.format(marker.persons_count) if marker.persons_count else 'Мест: не указано',
            'd1': u'{0} {1}'.format(price, cls.currency_to_str(currency)),
        }



# -- commercial real estate
class AbstractTradesIndex(AbstractBaseIndex):
    """
    Sale index and rent index of the trades objects contains the same field and the same logic,
    but must use different tables. For this approach we can't simply create sale index,
    and than inherit rent index from it. (Django will generate inappropriate inheritance scheme).

    So abstract index was developed and both sale and rent indexes was derived from it.
    """
    class Meta:
        abstract = True

    # fields
    price = models.FloatField(db_index=True)
    currency_sid = models.PositiveSmallIntegerField()
    market_type_sid = models.PositiveSmallIntegerField(db_index=True)
    halls_area = models.FloatField(db_index=True)
    total_area = models.FloatField(db_index=True)
    building_type_sid = models.PositiveSmallIntegerField(db_index=True)
    hot_water = models.BooleanField(db_index=True)
    cold_water = models.BooleanField(db_index=True)
    gas = models.BooleanField(db_index=True)
    electricity = models.BooleanField(db_index=True)
    sewerage = models.BooleanField(db_index=True)

    # constants
    tid = OBJECTS_TYPES.trade()


    @classmethod
    def add(cls, record, using=None):
        raise Exception('Abstract method was called. This method should be overwritten.')


    @classmethod
    def min_add_queryset(cls):
        raise Exception('Abstract method was called. This method should be overwritten.')


    @classmethod
    def brief_queryset(cls):
        return cls.objects.all().only(
            'publication_id', 'hash_id', 'lat', 'lng', 'price', 'currency_sid', 'total_area')


    @classmethod
    def min_remove_queryset(cls):
        model = HEAD_MODELS[cls.tid]
        return model.objects.all().only(
            'id',
            'degree_lat',
            'degree_lng',
            'segment_lat',
            'segment_lng',
            'pos_lat',
            'pos_lng',
        )


    @classmethod
    def apply_filters(cls, filters, markers):
        markers = cls.apply_market_type_filter(filters, markers)
        markers = cls.apply_price_filter(filters, markers)
        markers = cls.apply_halls_area_filter(filters, markers)
        markers = cls.apply_total_area_filter(filters, markers)
        markers = cls.apply_trade_building_type_filter(filters, markers)
        markers = cls.apply_electricity_filter(filters, markers)
        markers = cls.apply_gas_filter(filters, markers)
        markers = cls.apply_hot_water_filter(filters, markers)
        markers = cls.apply_cold_water_filter(filters, markers)
        markers = cls.apply_sewerage_filter(filters, markers)
        return markers


    @classmethod
    def brief(cls, marker, filters=None):
        currency = cls.currency_from_filters(filters)
        price = cls.convert_and_format_price(marker.price, marker.currency_sid, currency)
        total_area = '{0}'.format(marker.total_area).rstrip('0').rstrip('.')

        return {
            'tid': cls.tid,
            'id': marker.hash_id,
            'd0': u'{0} м²'.format(total_area),
            'd1': u'{0} {1}'.format(price, cls.currency_to_str(currency)),
        }



class TradesSaleIndex(AbstractTradesIndex):
    class Meta:
        db_table = 'index_trades_sale'


    @classmethod
    def add(cls, record, using=None):
        cls.objects.using(using).create(
            publication_id=record.id,
            hash_id=record.hash_id,
            lat=float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
            lng=float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

            market_type_sid=record.body.market_type_sid,
            halls_area=record.body.total_area,
            total_area=record.body.total_area,
            building_type_sid=record.body.building_type_sid,
            hot_water=record.body.hot_water,
            cold_water=record.body.cold_water,
            gas=record.body.gas,
            electricity=record.body.electricity,
            sewerage=record.body.sewerage,

            price=record.sale_terms.price, # note: sale terms here
            currency_sid=record.sale_terms.currency_sid, # note: sale terms here
        )


    @classmethod
    def min_add_queryset(cls):
        model = HEAD_MODELS[OBJECTS_TYPES.trade()]
        return model.objects.all().only(
            'id',
            'hash_id',
            'degree_lat',
            'degree_lng',
            'segment_lat',
            'segment_lng',
            'pos_lat',
            'pos_lng',

            'body__market_type_sid',
            'body__halls_area',
            'body__total_area',
            'body__building_type_sid',
            'body__hot_water',
            'body__cold_water',
            'body__electricity',
            'body__gas',
            'body__sewerage',

            'sale_terms__price', # note: sale terms here
            'sale_terms__currency_sid', # note: sale terms here
        )



class TradesRentIndex(AbstractTradesIndex):
    class Meta:
        db_table = 'index_trades_rent'


    @classmethod
    def add(cls, record, using=None):
        cls.objects.using(using).create(
            publication_id=record.id,
            hash_id=record.hash_id,
            lat=float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
            lng=float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

            market_type_sid=record.body.market_type_sid,
            halls_area=record.body.total_area,
            total_area=record.body.total_area,
            building_type_sid=record.body.building_type_sid,
            hot_water=record.body.hot_water,
            cold_water=record.body.cold_water,
            gas=record.body.gas,
            electricity=record.body.electricity,
            sewerage=record.body.sewerage,

            price=record.rent_terms.price, # note: rent terms here
            currency_sid=record.rent_terms.currency_sid, # note: rent terms here
        )


    @classmethod
    def min_add_queryset(cls):
        model = HEAD_MODELS[OBJECTS_TYPES.trade()]
        return model.objects.all().only(
            'id',
            'hash_id',
            'degree_lat',
            'degree_lng',
            'segment_lat',
            'segment_lng',
            'pos_lat',
            'pos_lng',

            'body__market_type_sid',
            'body__halls_area',
            'body__total_area',
            'body__building_type_sid',
            'body__hot_water',
            'body__cold_water',
            'body__electricity',
            'body__gas',
            'body__sewerage',

            'rent_terms__price', # note: rent terms here
            'rent_terms__currency_sid', # note: rent terms here
        )



class AbstractOfficesIndex(AbstractBaseIndex):
    """
    Sale index and rent index of the offices contains the same field and the same logic,
    but must use different tables. For this approach we can't simply create sale index,
    and than inherit rent index from it. (Django will generate inappropriate inheritance scheme).

    So abstract index was developed and both sale and rent indexes was derived from it.
    """
    class Meta:
        abstract = True

    # fields
    price = models.FloatField(db_index=True)
    currency_sid = models.PositiveSmallIntegerField()
    market_type_sid = models.PositiveSmallIntegerField(db_index=True)
    total_area = models.FloatField(db_index=True)
    cabinets_count = models.PositiveSmallIntegerField(db_index=True)
    hot_water = models.BooleanField(db_index=True)
    cold_water = models.BooleanField(db_index=True)
    security = models.BooleanField(db_index=True)
    kitchen = models.BooleanField(db_index=True)

    # constants
    tid = OBJECTS_TYPES.office()


    @classmethod
    def add(cls, record, using=None):
        raise Exception('Abstract method was called. This method should be overwritten.')


    @classmethod
    def min_add_queryset(cls):
        raise Exception('Abstract method was called. This method should be overwritten.')


    @classmethod
    def brief_queryset(cls):
        return cls.objects.all().only(
            'publication_id', 'hash_id', 'lat', 'lng', 'price', 'currency_sid', 'total_area')


    @classmethod
    def min_remove_queryset(cls):
        model = HEAD_MODELS[cls.tid]
        return model.objects.all().only(
            'id',
            'degree_lat',
            'degree_lng',
            'segment_lat',
            'segment_lng',
            'pos_lat',
            'pos_lng',
        )


    @classmethod
    def apply_filters(cls, filters, markers):
        markers = cls.apply_market_type_filter(filters, markers)
        markers = cls.apply_price_filter(filters, markers)
        markers = cls.apply_total_area_filter(filters, markers)
        markers = cls.apply_cabinets_count_filter(filters, markers)
        markers = cls.apply_hot_water_filter(filters, markers)
        markers = cls.apply_cold_water_filter(filters, markers)
        markers = cls.apply_kitchen_filter(filters, markers)
        markers = cls.apply_security_filter(filters, markers)
        return markers


    @classmethod
    def brief(cls, marker, filters=None):
        currency = cls.currency_from_filters(filters)
        price = cls.convert_and_format_price(marker.price, marker.currency_sid, currency)
        total_area = '{0}'.format(marker.total_area).rstrip('0').rstrip('.')

        return {
            'tid': cls.tid,
            'id': marker.hash_id,
            'd0': u'{0} м²'.format(total_area),
            'd1': u'{0} {1}'.format(price, cls.currency_to_str(currency)),
        }



class OfficesSaleIndex(AbstractOfficesIndex):
    class Meta:
        db_table = 'index_offices_sale'


    @classmethod
    def add(cls, record, using=None):
        cls.objects.using(using).create(
            publication_id=record.id,
            hash_id=record.hash_id,
            lat=float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
            lng=float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

            market_type_sid=record.body.market_type_sid,
            total_area=record.body.total_area,
            cabinets_count=record.body.cabinets_count,
            hot_water=record.body.hot_water,
            cold_water=record.body.cold_water,
            security=record.body.security,
            kitchen=record.body.kitchen,

            price=record.sale_terms.price, # note: sale terms here
            currency_sid=record.sale_terms.currency_sid, # note: sale terms here
        )


    @classmethod
    def min_add_queryset(cls):
        model = HEAD_MODELS[OBJECTS_TYPES.office()]
        return model.objects.all().only(
            'id',
            'hash_id',
            'degree_lat',
            'degree_lng',
            'segment_lat',
            'segment_lng',
            'pos_lat',
            'pos_lng',
            'body__market_type_sid',
            'body__total_area',
            'body__cabinets_count',
            'body__hot_water',
            'body__cold_water',
            'body__security',
            'body__kitchen',

            'sale_terms__price', # note: sale terms here
            'sale_terms__currency_sid', # note: sale terms here
        )



class OfficesRentIndex(AbstractOfficesIndex):
    class Meta:
        db_table = 'index_offices_rent'


    @classmethod
    def add(cls, record, using=None):
        cls.objects.using(using).create(
            publication_id=record.id,
            hash_id=record.hash_id,
            lat=float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
            lng=float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

            market_type_sid=record.body.market_type_sid,
            total_area=record.body.total_area,
            cabinets_count=record.body.cabinets_count,
            hot_water=record.body.hot_water,
            cold_water=record.body.cold_water,
            security=record.body.security,
            kitchen=record.body.kitchen,

            price=record.rent_terms.price, # note: rent terms here
            currency_sid=record.rent_terms.currency_sid, # note: rent terms here
        )


    @classmethod
    def min_add_queryset(cls):
        model = HEAD_MODELS[OBJECTS_TYPES.office()]
        return model.objects.all().only(
            'id',
            'hash_id',
            'degree_lat',
            'degree_lng',
            'segment_lat',
            'segment_lng',
            'pos_lat',
            'pos_lng',
            'body__market_type_sid',
            'body__total_area',
            'body__cabinets_count',
            'body__hot_water',
            'body__cold_water',
            'body__security',
            'body__kitchen',

            'rent_terms__price', # note: rent terms here
            'rent_terms__currency_sid', # note: rent terms here
        )



class AbstractWarehousesIndex(AbstractBaseIndex):
    """
    Sale index and rent index of the warehouses contains the same field and the same logic,
    but must use different tables. For this approach we can't simply create sale index,
    and than inherit rent index from it. (Django will generate inappropriate inheritance scheme).

    So abstract index was developed and both sale and rent indexes was derived from it.
    """
    class Meta:
        abstract = True

    # fields
    price = models.FloatField(db_index=True)
    currency_sid = models.PositiveSmallIntegerField()
    market_type_sid = models.PositiveSmallIntegerField(db_index=True)
    halls_area = models.FloatField(db_index=True)
    hot_water = models.BooleanField(db_index=True)
    cold_water = models.BooleanField(db_index=True)
    electricity = models.BooleanField(db_index=True)
    gas = models.BooleanField(db_index=True)
    security_alarm = models.BooleanField(db_index=True)
    fire_alarm = models.BooleanField(db_index=True)


    # constants
    tid = OBJECTS_TYPES.warehouse()


    @classmethod
    def add(cls, record, using=None):
        raise Exception('Abstract method was called. This method should be overwritten.')


    @classmethod
    def min_add_queryset(cls):
        raise Exception('Abstract method was called. This method should be overwritten.')


    @classmethod
    def brief_queryset(cls):
        return cls.objects.all().only(
            'publication_id', 'hash_id', 'lat', 'lng', 'price', 'currency_sid', 'halls_area')  # todo: fixme


    @classmethod
    def min_remove_queryset(cls):
        model = HEAD_MODELS[cls.tid]
        return model.objects.all().only(
            'id',
            'degree_lat',
            'degree_lng',
            'segment_lat',
            'segment_lng',
            'pos_lat',
            'pos_lng',
        )


    @classmethod
    def apply_filters(cls, filters, markers):
        markers = cls.apply_market_type_filter(filters, markers)
        markers = cls.apply_price_filter(filters, markers)
        markers = cls.apply_halls_area_filter(filters, markers)
        markers = cls.apply_hot_water_filter(filters, markers)
        markers = cls.apply_cold_water_filter(filters, markers)
        markers = cls.apply_electricity_filter(filters, markers)
        markers = cls.apply_gas_filter(filters, markers)
        markers = cls.apply_fire_alarm_filter(filters, markers)
        markers = cls.apply_security_alarm_filter(filters, markers)
        return markers


    @classmethod
    def brief(cls, marker, filters=None):
        currency = cls.currency_from_filters(filters)
        price = cls.convert_and_format_price(marker.price, marker.currency_sid, currency)
        halls_area = '{0}'.format(marker.halls_area).rstrip('0').rstrip('.')

        return {
            'id': marker.hash_id,
            'd0': u'{0} м²'.format(halls_area),
            'd1': u'{0} {1}'.format(price, cls.currency_to_str(currency)),
        }



class WarehousesSaleIndex(AbstractWarehousesIndex):
    class Meta:
        db_table = 'index_warehouses_sale'


    @classmethod
    def add(cls, record, using=None):
        cls.objects.using(using).create(
            publication_id=record.id,
            hash_id=record.hash_id,
            lat=float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
            lng=float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

            market_type_sid=record.body.market_type_sid,
            halls_area=record.body.halls_area,
            hot_water=record.body.hot_water,
            cold_water=record.body.cold_water,
            electricity=record.body.electricity,
            gas=record.body.gas,
            fire_alarm=record.body.fire_alarm,
            security_alarm=record.body.security_alarm,

            price=record.sale_terms.price, # note: sale terms here
            currency_sid=record.sale_terms.currency_sid, # note: sale terms here
        )


    @classmethod
    def min_add_queryset(cls):
        model = HEAD_MODELS[OBJECTS_TYPES.warehouse()]
        return model.objects.all().only(
            'id',
            'hash_id',
            'degree_lat',
            'degree_lng',
            'segment_lat',
            'segment_lng',
            'pos_lat',
            'pos_lng',

            'body__market_type_sid',
            'body__halls_area',
            'body__hot_water',
            'body__cold_water',
            'body__electricity',
            'body__gas',
            'body__fire_alarm',
            'body__security_alarm',

            'sale_terms__price', # note: sale terms here
            'sale_terms__currency_sid', # note: sale terms here
        )



class WarehousesRentIndex(WarehousesSaleIndex):
    class Meta:
        db_table = 'index_warehouses_rent'


    @classmethod
    def add(cls, record, using=None):
        cls.objects.using(using).create(
            publication_id=record.id,
            hash_id=record.hash_id,
            lat=float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
            lng=float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

            market_type_sid=record.body.market_type_sid,
            halls_area=record.body.halls_area,
            hot_water=record.body.hot_water,
            cold_water=record.body.cold_water,
            electricity=record.body.electricity,
            gas=record.body.gas,
            fire_alarm=record.body.fire_alarm,
            security_alarm=record.body.security_alarm,

            price=record.rent_terms.price, # note: rent terms here
            currency_sid=record.rent_terms.currency_sid, # note: rent terms here
        )


    @classmethod
    def min_add_queryset(cls):
        model = HEAD_MODELS[OBJECTS_TYPES.warehouse()]
        return model.objects.all().only(
            'id',
            'hash_id',
            'degree_lat',
            'degree_lng',
            'segment_lat',
            'segment_lng',
            'pos_lat',
            'pos_lng',

            'body__market_type_sid',
            'body__halls_area',
            'body__hot_water',
            'body__cold_water',
            'body__electricity',
            'body__gas',
            'body__fire_alarm',
            'body__security_alarm',

            'rent_terms__price', # note: rent terms here
            'rent_terms__currency_sid', # note: rent terms here
        )



class AbstractBusinessesIndex(AbstractBaseIndex):
    """
    Sale index and rent index of the businesses contains the same field and the same logic,
    but must use different tables. For this approach we can't simply create sale index,
    and than inherit rent index from it. (Django will generate inappropriate inheritance scheme).

    So abstract index was developed and both sale and rent indexes was derived from it.
    """
    class Meta:
        abstract = True

    # fields
    price = models.FloatField(db_index=True)
    currency_sid = models.PositiveSmallIntegerField()

    # constants
    tid = OBJECTS_TYPES.business()


    @classmethod
    def add(cls, record, using=None):
        raise Exception('Abstract method was called. This method should be overwritten.')


    @classmethod
    def min_add_queryset(cls):
        raise Exception('Abstract method was called. This method should be overwritten.')


    @classmethod
    def brief_queryset(cls):
        return cls.objects.all().only(
            'publication_id', 'hash_id', 'lat', 'lng', 'price', 'currency_sid')


    @classmethod
    def min_remove_queryset(cls):
        model = HEAD_MODELS[cls.tid]
        return model.objects.all().only(
            'id',
            'degree_lat',
            'degree_lng',
            'segment_lat',
            'segment_lng',
            'pos_lat',
            'pos_lng',
        )


    @classmethod
    def apply_filters(cls, filters, markers):
        markers = cls.apply_price_filter(filters, markers)
        return markers


    @classmethod
    def brief(cls, marker, filters=None):
        currency = cls.currency_from_filters(filters)
        price = cls.convert_and_format_price(marker.price, marker.currency_sid, currency)

        return {
            'tid': cls.tid,
            'id': marker.hash_id,
            'd0': u'',
            'd1': u'{0} {1}'.format(price, cls.currency_to_str(currency)),
        }



class BusinessesSaleIndex(AbstractBusinessesIndex):
    class Meta:
        db_table = 'index_businesses_sale'


    @classmethod
    def add(cls, record, using=None):
        cls.objects.using(using).create(
            publication_id=record.id,
            hash_id=record.hash_id,
            lat=float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
            lng=float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

            price=record.sale_terms.price, # note: sale terms here
            currency_sid=record.sale_terms.currency_sid, # note: sale terms here
        )


    @classmethod
    def min_add_queryset(cls):
        model = HEAD_MODELS[OBJECTS_TYPES.business()]
        return model.objects.all().only(
            'degree_lat',
            'degree_lng',
            'segment_lat',
            'segment_lng',
            'pos_lat',
            'pos_lng',

            'id',
            'hash_id',

            'sale_terms__price', # note: sale terms here
            'sale_terms__currency_sid', # note: sale terms here
        )



class BusinessesRentIndex(AbstractBusinessesIndex):
    class Meta:
        db_table = 'index_businesses_rent'


    @classmethod
    def add(cls, record, using=None):
        cls.objects.using(using).create(
            publication_id=record.id,
            hash_id=record.hash_id,
            lat=float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
            lng=float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

            price=record.rent_terms.price, # note: rent terms here
            currency_sid=record.rent_terms.currency_sid, # note: rent terms here
        )


    @classmethod
    def min_add_queryset(cls):
        model = HEAD_MODELS[OBJECTS_TYPES.business()]
        return model.objects.all().only(
            'degree_lat',
            'degree_lng',
            'segment_lat',
            'segment_lng',
            'pos_lat',
            'pos_lng',

            'id',
            'hash_id',

            'rent_terms__price', # note: rent terms here
            'rent_terms__currency_sid', # note: rent terms here
        )



# class CateringsSaleIndex(AbstractBaseIndex):
#     price = models.FloatField(db_index=True)
#     currency_sid = models.PositiveSmallIntegerField()
#     market_type_sid = models.PositiveSmallIntegerField(db_index=True)
#     halls_area = models.FloatField(db_index=True)
#     total_area = models.FloatField(db_index=True)
#     building_type_sid = models.PositiveSmallIntegerField(db_index=True)
#     hot_water = models.BooleanField(db_index=True)
#     cold_water = models.BooleanField(db_index=True)
#     gas = models.BooleanField(db_index=True)
#     electricity = models.BooleanField(db_index=True)
#     sewerage = models.BooleanField(db_index=True)
#
#
#     class Meta:
#         db_table = 'index_caterings_sale'
#
#
#     @classmethod
#     def add(cls, record, using=None):
#         cls.objects.using(using).create(
#             publication_id=record.id,
#             hash_id=record.hash_id,
#             lat=float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
#             lng=float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),
#
#             market_type_sid=record.body.market_type_sid,
#             halls_area=record.body.halls_area,
#             total_area=record.body.total_area,
#             building_type_sid=record.body.building_type_sid,
#             hot_water=record.body.hot_water,
#             cold_water=record.body.cold_water,
#             gas=record.body.gas,
#             electricity=record.body.electricity,
#             sewerage=record.body.sewerage,
#
#             price=record.sale_terms.price,
#             currency_sid=record.sale_terms.currency_sid,
#         )
#
#
#     @classmethod
#     def min_queryset(cls):
#         return cls.objects.all().only(
#             'hash_id', 'lat', 'lng', 'price', 'currency_sid', 'total_area')  # todo: fixme
#
#
#     @classmethod
#     def min_add_queryset(cls):
#         model = HEAD_MODELS[OBJECTS_TYPES.catering()]
#         return model.objects.all().only(
#             'degree_lat',
#             'degree_lng',
#             'segment_lat',
#             'segment_lng',
#             'pos_lat',
#             'pos_lng',
#
#             'id',
#             'hash_id',
#
#             'body__market_type_sid',
#             'body__halls_area',
#             'body__total_area',
#             'body__building_type_sid',
#             'body__hot_water',
#             'body__cold_water',
#             'body__electricity',
#             'body__gas',
#             'body__fire_alarm',
#             'body__security_alarm',
#
#             'sale_terms__price',
#             'sale_terms__currency_sid'
#         )
#
#
#     @classmethod
#     def apply_filters(cls, filters, markers):
#         markers = cls.apply_market_type_filter(filters, markers)
#         markers = cls.apply_price_filter(filters, markers)
#         markers = cls.apply_halls_area_filter(filters, markers)
#         markers = cls.apply_total_area_filter(filters, markers)
#         markers = cls.apply_trade_building_type_filter(filters, markers)
#         markers = cls.apply_electricity_filter(filters, markers)
#         markers = cls.apply_gas_filter(filters, markers)
#         markers = cls.apply_hot_water_filter(filters, markers)
#         markers = cls.apply_cold_water_filter(filters, markers)
#         markers = cls.apply_sewerage_filter(filters, markers)
#         return markers
#
#
#     @classmethod
#     def brief(cls, marker, filters=None):
#         currency = cls.currency_from_filters(filters)
#         price = cls.convert_and_format_price(marker.price, marker.currency_sid, currency)
#         total_area = '{0}'.format(marker.total_area).rstrip('0').rstrip('.')
#
#         return {
#             'id': marker.hash_id,
#             'd0': u'{0} м²'.format(total_area),
#             'd1': u'{0} {1}'.format(price, cls.currency_to_str(currency)),
#         }
#
#
#
# class CateringsRentIndex(CateringsSaleIndex):
#     class Meta:
#         db_table = 'index_caterings_rent'



class AbstractGaragesIndex(AbstractBaseIndex):
    """
    Sale index and rent index of the garages contains the same field and the same logic,
    but must use different tables. For this approach we can't simply create sale index,
    and than inherit rent index from it. (Django will generate inappropriate inheritance scheme).

    So abstract index was developed and both sale and rent indexes was derived from it.
    """
    class Meta:
        abstract = True

    # fields
    price = models.FloatField(db_index=True)
    currency_sid = models.PositiveSmallIntegerField()
    area = models.FloatField(db_index=True)
    ceiling_height = models.FloatField(db_index=True)
    pit = models.BooleanField(db_index=True)

    # constants
    tid = OBJECTS_TYPES.garage()


    @classmethod
    def add(cls, record, using=None):
        raise Exception('Abstract method was called. This method should be overwritten.')


    @classmethod
    def min_add_queryset(cls):
        raise Exception('Abstract method was called. This method should be overwritten.')


    @classmethod
    def brief_queryset(cls):
        return cls.objects.all().only(
            'publication_id', 'hash_id', 'lat', 'lng', 'price', 'currency_sid', 'area')  # todo: fixme


    @classmethod
    def min_remove_queryset(cls):
        model = HEAD_MODELS[cls.tid]
        return model.objects.all().only(
            'id',
            'degree_lat',
            'degree_lng',
            'segment_lat',
            'segment_lng',
            'pos_lat',
            'pos_lng',
        )


    @classmethod
    def apply_filters(cls, filters, markers):
        markers = cls.apply_market_type_filter(filters, markers)
        markers = cls.apply_price_filter(filters, markers)
        markers = cls.apply_area_filter(filters, markers)
        markers = cls.apply_ceiling_height_filter(filters, markers)
        markers = cls.apply_pit_filter(filters, markers)
        return markers


    @classmethod
    def brief(cls, marker, filters=None):
        currency = cls.currency_from_filters(filters)
        price = cls.convert_and_format_price(marker.price, marker.currency_sid, currency)
        area = '{0}'.format(marker.area).rstrip('0').rstrip('.')

        return {
            'tid': cls.tid,
            'id': marker.hash_id,
            'd0': u'{0} м²'.format(area),
            'd1': u'{0} {1}'.format(price, cls.currency_to_str(currency)),
        }



class GaragesSaleIndex(AbstractGaragesIndex):
    class Meta:
        db_table = 'index_garages_sale'


    @classmethod
    def min_add_queryset(cls):
        model = HEAD_MODELS[cls.tid]
        return model.objects.all().only(
            'id',
            'hash_id',
            'degree_lat',
            'degree_lng',
            'segment_lat',
            'segment_lng',
            'pos_lat',
            'pos_lng',

            'body__area',
            'body__ceiling_height',
            'body__pit',

            'sale_terms__price', # note: sale terms here
            'sale_terms__currency_sid', # note: sale terms here
        )


    @classmethod
    def add(cls, record, using=None):
        cls.objects.using(using).create(
            publication_id=record.id,
            hash_id=record.hash_id,
            lat=float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
            lng=float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

            area=record.body.area,
            ceiling_height=record.body.ceiling_height,
            pit=record.body.pit,

            price=record.sale_terms.price, # note: sale terms here
            currency_sid=record.sale_terms.currency_sid, # note: sale terms here
        )



class GaragesRentIndex(AbstractGaragesIndex):
    class Meta:
        db_table = 'index_garages_rent'


    @classmethod
    def add(cls, record, using=None):
        cls.objects.using(using).create(
            publication_id=record.id,
            hash_id=record.hash_id,
            lat=float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
            lng=float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

            area=record.body.area,
            ceiling_height=record.body.ceiling_height,
            pit=record.body.pit,

            price=record.rent_terms.price, # note: sale terms here
            currency_sid=record.rent_terms.currency_sid, # note: sale terms here
        )


    @classmethod
    def min_add_queryset(cls):
        model = HEAD_MODELS[cls.tid]
        return model.objects.all().only(
            'id',
            'hash_id',
            'degree_lat',
            'degree_lng',
            'segment_lat',
            'segment_lng',
            'pos_lat',
            'pos_lng',

            'body__area',
            'body__ceiling_height',
            'body__pit',

            'rent_terms__price', # note: sale terms here
            'rent_terms__currency_sid', # note: sale terms here
        )



class AbstractLandsIndex(AbstractBaseIndex):
    """
    Sale index and rent index of the lands contains the same field and the same logic,
    but must use different tables. For this approach we can't simply create sale index,
    and than inherit rent index from it. (Django will generate inappropriate inheritance scheme).

    So abstract index was developed and both sale and rent indexes was derived from it.
    """
    class Meta:
        abstract = True

    # fields
    price = models.FloatField(db_index=True)
    currency_sid = models.PositiveSmallIntegerField()
    area = models.FloatField(db_index=True)
    water = models.BooleanField(db_index=True)
    electricity = models.BooleanField(db_index=True)
    gas = models.BooleanField(db_index=True)
    sewerage = models.BooleanField(db_index=True)

    # constants
    tid = OBJECTS_TYPES.land()


    @classmethod
    def add(cls, record, using=None):
        raise Exception('Abstract method was called. This method should be overwritten.')


    @classmethod
    def min_add_queryset(cls):
        raise Exception('Abstract method was called. This method should be overwritten.')


    @classmethod
    def brief_queryset(cls):
        return cls.objects.all().only(
            'publication_id', 'hash_id', 'lat', 'lng', 'price', 'currency_sid', 'area')  # todo: fixme


    @classmethod
    def min_remove_queryset(cls):
        model = HEAD_MODELS[cls.tid]
        return model.objects.all().only(
            'id',
            'degree_lat',
            'degree_lng',
            'segment_lat',
            'segment_lng',
            'pos_lat',
            'pos_lng',
        )


    @classmethod
    def apply_filters(cls, filters, markers):
        markers = cls.apply_market_type_filter(filters, markers)
        markers = cls.apply_price_filter(filters, markers)
        markers = cls.apply_area_filter(filters, markers)
        markers = cls.apply_water_filter(filters, markers)
        markers = cls.apply_electricity_filter(filters, markers)
        markers = cls.apply_gas_filter(filters, markers)
        markers = cls.apply_sewerage_filter(filters, markers)
        return markers


    @classmethod
    def brief(cls, marker, filters=None):
        currency = cls.currency_from_filters(filters)
        price = cls.convert_and_format_price(marker.price, marker.currency_sid, currency)
        area = '{0}'.format(marker.area).rstrip('0').rstrip('.')

        return {
            'tid': cls.tid,
            'id': marker.hash_id,
            'd0': u'{0} м²'.format(area),
            'd1': u'{0} {1}'.format(price, cls.currency_to_str(currency)),
        }



class LandsSaleIndex(AbstractLandsIndex):
    class Meta:
        db_table = 'index_lands_sale'


    @classmethod
    def add(cls, record, using=None):
        cls.objects.using(using).create(
            publication_id=record.id,
            hash_id=record.hash_id,
            lat=float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
            lng=float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

            area=record.body.area,
            water=record.body.water,
            electricity=record.body.electricity,
            gas=record.body.gas,
            sewerage=record.body.sewerage,

            price=record.sale_terms.price, # note: sale terms here
            currency_sid=record.sale_terms.currency_sid, # note: sale terms here
        )


    @classmethod
    def min_add_queryset(cls):
        model = HEAD_MODELS[OBJECTS_TYPES.land()]
        return model.objects.all().only(
            'id',
            'hash_id',
            'degree_lat',
            'degree_lng',
            'segment_lat',
            'segment_lng',
            'pos_lat',
            'pos_lng',

            'body__area',
            'body__water',
            'body__electricity',
            'body__gas',
            'body__sewerage',

            'sale_terms__price', # note: sale terms here
            'sale_terms__currency_sid', # note: sale terms here
        )



class LandsRentIndex(LandsSaleIndex):
    class Meta:
        db_table = 'index_lands_rent'


    @classmethod
    def add(cls, record, using=None):
        cls.objects.using(using).create(
            publication_id=record.id,
            hash_id=record.hash_id,
            lat=float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
            lng=float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

            area=record.body.area,
            water=record.body.water,
            electricity=record.body.electricity,
            gas=record.body.gas,
            sewerage=record.body.sewerage,

            price=record.rent_terms.price, # note: rent terms here
            currency_sid=record.rent_terms.currency_sid, # note: rent terms here
        )


    @classmethod
    def min_add_queryset(cls):
        model = HEAD_MODELS[OBJECTS_TYPES.land()]
        return model.objects.all().only(
            'id',
            'hash_id',
            'degree_lat',
            'degree_lng',
            'segment_lat',
            'segment_lng',
            'pos_lat',
            'pos_lng',

            'body__area',
            'body__water',
            'body__electricity',
            'body__gas',
            'body__sewerage',

            'rent_terms__price', # note: rent terms here
            'rent_terms__currency_sid', # note: rent terms here
        )



# -- index handler
class SegmentsIndex(models.Model):
    index_db_name = settings.INDEXES_DATABASE_NAME
    min_zoom = 1
    max_zoom = 15


    # static members
    grid = Grid(min_zoom, max_zoom)

    living_sale_indexes = {
        OBJECTS_TYPES.flat(): FlatsSaleIndex,
        OBJECTS_TYPES.house(): HousesSaleIndex,
        OBJECTS_TYPES.room(): RoomsSaleIndex,
    }
    living_rent_indexes = {
        OBJECTS_TYPES.flat(): FlatsRentIndex,
        OBJECTS_TYPES.house(): HousesRentIndex,
        OBJECTS_TYPES.room(): RoomsRentIndex,
    }
    commercial_sale_indexes = {
        OBJECTS_TYPES.trade(): TradesSaleIndex,
        OBJECTS_TYPES.office(): OfficesSaleIndex,
        OBJECTS_TYPES.warehouse(): WarehousesSaleIndex,
        OBJECTS_TYPES.business(): BusinessesSaleIndex,
        OBJECTS_TYPES.garage(): GaragesSaleIndex,
        OBJECTS_TYPES.land(): LandsSaleIndex,
    }
    commercial_rent_indexes = {
        OBJECTS_TYPES.trade(): TradesRentIndex,
        OBJECTS_TYPES.office(): OfficesRentIndex,
        OBJECTS_TYPES.warehouse(): WarehousesRentIndex,
        OBJECTS_TYPES.business(): BusinessesRentIndex,
        OBJECTS_TYPES.garage(): GaragesRentIndex,
        OBJECTS_TYPES.land(): LandsRentIndex,
    }


    # fields
    tid = models.SmallIntegerField(db_index=True)
    zoom = models.SmallIntegerField(db_index=True)
    x = models.IntegerField(db_index=True)
    y = models.IntegerField(db_index=True)
    ids = BigIntegerArrayField()


    class Meta:
        db_table = 'index_all_segments'


    @classmethod
    def add_record(cls, tid, hid, for_sale, for_rent):
        if for_sale and for_rent:
            raise InvalidArgument('Object can be for_sale or for_rent but not both.')
        else:
            if not for_sale and not for_rent:
                raise InvalidArgument('Object can be for_sale or for_rent')

        if for_sale:
            index = cls.living_sale_indexes.get(tid, cls.commercial_sale_indexes.get(tid))
        else:
            index = cls.living_rent_indexes.get(tid, cls.commercial_rent_indexes.get(tid))

        if index is None:
            return InvalidArgument('No index class for such tid.')


        record = index.min_add_queryset().filter(id=hid)[:1][0]
        lat, lng = cls.record_lat_lng(record)
        lat, lng = cls.grid.normalize_lat_lng(lat, lng)


        # Можливий такий випадок, коли при знятті оголошення з публікації чи видаленні,
        # інформація з індексу не видалилась.
        # Для запобігання дублікату запису в індексі слід видалити всі записи із id=hid.
        index.objects.filter(publication_id=record.id).delete()


        # todo: add transaction here (find a way to combine custom sql and django orm to perform a transaction)
        index.add(record, using=cls.index_db_name)

        cursor = cls.cursor()
        cursor.execute('BEGIN;')
        for zoom, x, y in cls.grid.segments_digests(lat, lng):
            # UPSERT emulation.
            # Query will execute UPDATE if record with such segment digest already exists,
            # otherwise the INSERT will be executed.
            cursor.execute(
                "UPDATE {table}"
                "   SET ids = array_append(ids, '{id}')"
                "   WHERE tid='{tid}' AND zoom='{zoom}' AND x='{x}' AND y='{y}';"

                "INSERT INTO {table} (tid, zoom, x, y, ids)"
                "   (SELECT {tid}, {zoom}, {x}, {y}, '{{ {id} }}'"
                "    WHERE NOT EXISTS ("
                "       SELECT 1 FROM {table} WHERE tid='{tid}' AND zoom='{zoom}' AND x='{x}' AND y='{y}'));"
                .format(
                    table=cls._meta.db_table,
                    id=record.id,
                    tid=record.tid,
                    zoom=zoom,
                    x=x,
                    y=y,
                )
            )
        cursor.execute('END;')
        cursor.close()
        # todo: transaction end


    @classmethod
    def remove_record(cls, tid, hid, for_sale, for_rent):
        if for_sale and for_rent:
            raise InvalidArgument('Object can or for_sale or for_rent but not both.')
        else:
            if not for_sale and not for_rent:
                raise InvalidArgument('Object can be for_sale or for_rent')


        if for_sale:
            index = cls.living_sale_indexes.get(tid, cls.commercial_sale_indexes.get(tid))
        else:
            index = cls.living_rent_indexes.get(tid, cls.commercial_rent_indexes.get(tid))

        if index is None:
            raise InvalidArgument('No index such tid.')


        record = index.min_remove_queryset().filter(id=hid)[:1][0]
        lat, lng = cls.record_lat_lng(record)
        lat, lng = cls.grid.normalize_lat_lng(lat, lng)


        # todo: add transaction here (find a way to combine custom sql and django orm to perform a transaction)
        cursor = cls.cursor()
        cursor.execute('BEGIN;')
        for zoom, x, y in cls.grid.segments_digests(lat, lng):

            # Removing of the id from the index
            query = "UPDATE index_all_segments SET ids=( " \
                    "   SELECT array_remove( " \
                    "       (SELECT ids FROM index_all_segments " \
                    "           WHERE tid='{tid}' AND zoom='{zoom}' AND x='{x}' AND y='{y}' " \
                    "           LIMIT 1" \
                    "       ), {id}::bigint)" \
                    "   )" \
                    "WHERE tid='{tid}' AND zoom='{zoom}' AND x='{x}' AND y='{y}'; " \
                .format(
                    table=cls._meta.db_table,
                    id=record.id,
                    tid=tid,
                    zoom=zoom,
                    x=x,
                    y=y,
                )

            cursor.execute(query)
        cursor.execute('END;')


        # If segment digest contains no more ids - remove it too
        cursor.execute(
            "DELETE FROM {table} WHERE ids = '{{}}';"
                .format(
                    table=cls._meta.db_table,
                ))
        cursor.close()

        index.remove(hid, using=cls.index_db_name)
        # todo: transaction end


    @classmethod
    def estimate_count(cls, tid, ne_segment_x, ne_segment_y, sw_segment_x, sw_segment_y, zoom, filters, excluded_ids_list):
        if 'for_sale' in filters:
            index = cls.living_sale_indexes.get(tid, cls.commercial_sale_indexes.get(tid))
        elif 'for_rent' in filters:
            index = cls.living_rent_indexes.get(tid, cls.commercial_rent_indexes.get(tid))

        if index is None:
            raise InvalidArgument('No index such tid.')


        # Підготувати SQL-запит на вибірку записів, попередньо відфільтрувавши за вхідними умовами.
        # Використовуєтсья спільний для обох методів (markers та estimate_count) спосіб обробки фільтрів
        # на основі django-ORM
        markers = index.apply_filters(filters, index.objects.all())
        markers_query = str(markers.query)

        # Далі, зі сформованого запиту виокремлюємо блок WHERE щоб вставити його в кастомний запит.
        # Django-ORM не дозволяє виконати запит такого типу,
        # а оскільки в ньому використовуються збережувані процедури та sql діалект,
        # то чистий sql в даному випадку є найбільш оптимальним рішенням по швидкодії/легкості імплементації.
        try:
            where = markers_query[markers_query.index('WHERE'):][5:]
        except ValueError:
            where = ''  # no WHERE condition is found

        # WARN: x < {sw_segment_x} повинно бути СТРОГО менше, інакше об’єкти дублюються у видачі.
        # WARN: y > {sw_segment_y} повинно бути СТРОГО більше, інакше об’єкти дублюються у видачі.
        query = "SELECT array_agg(publication_id), x, y FROM {index_table}" \
                "   JOIN {segments_index_table} " \
                "       ON zoom = '{zoom}' AND " \
                "          (x >= {ne_segment_x} AND x < {sw_segment_x}) AND " \
                "          (y <= {ne_segment_y} AND y > {sw_segment_y}) AND " \
                "           tid = {tid} "\
                "   WHERE publication_id = ANY(ids) {where_condition}" \
                "   GROUP BY ids, x, y;" \
            .format(
                index_table=index._meta.db_table,
                segments_index_table=cls._meta.db_table,
                zoom=zoom,
                ne_segment_x=ne_segment_x,
                sw_segment_x=sw_segment_x,
                ne_segment_y=ne_segment_y,
                sw_segment_y=sw_segment_y,
                tid=tid,
                where_condition=' AND ' + where if where else '',
            )

        cursor = cls.cursor()
        cursor.execute(query)
        selected_data = cursor.fetchall()
        cursor.close()


        # intersecting received ids
        filtered_data = list()
        publications_ids = set()
        for ids, x, y in selected_data:
            ids = set(ids) - set(excluded_ids_list)
            filtered_data.append((ids, x, y, )) # note: tuple here
            publications_ids = publications_ids.union(ids)


        step_per_lat = cls.grid.step_on_lat(zoom)
        step_per_lng = cls.grid.step_on_lng(zoom)
        segments = dict()
        for ids, x, y in filtered_data:
            if len(ids) > 0:
                segments.update({
                    '{lat}:{lng}'.format(
                        lat=y * step_per_lat + (step_per_lat / 2) - step_per_lat - 90,  # денормалізація широти
                        lng=x * step_per_lng + (step_per_lng / 2) - step_per_lng - 180,  # денормалізація довготи
                    ): len(ids)
                })

        return segments, publications_ids


    @classmethod
    def markers(cls, tid, ne_segment_x, ne_segment_y, sw_segment_x, sw_segment_y, zoom, filters, excluded_ids_list):
        """
        :param tid: object type id.
        :param ne_segment_x: normalized X coordinate of the north east corner of the viewport.
        :param ne_segment_y: normalized Y coordinate of the north east corner of the viewport.
        :param sw_segment_x: normalized X coordinate of the south west corner of the viewport.
        :param sw_segment_y: normalized Y coordinate of the south west corner of the viewport.
        :param zoom: zoom level. (by default should be 14)

        :param filters:
            dict that contains info about what kind of markers should be included into output.
            For more details see "utils.py" of markers package.

        :param excluded_ids_list:
            list of publications ids that should be excluded from output on current iteration.

        :returns:
            dict with markers briefs and their positions and
            list with all publications ids that was included into briefs, to prevent duplicates on next iteration.
        """

        if 'for_sale' in filters:
            index = cls.living_sale_indexes.get(tid, cls.commercial_sale_indexes.get(tid))
        elif 'for_rent' in filters:
            index = cls.living_rent_indexes.get(tid, cls.commercial_rent_indexes.get(tid))
        else:
            raise RuntimeError('Request must containt filters or for rnet, or for sale.')

        if index is None:
            raise RuntimeError('No index for such tid.')


        # Custom SQL is needed here to call PostgreSQL's stored procedure "unnest(...)"
        # Django ORM doesn't allow to do that.

        # WARN: x < {sw_segment_x} повинно бути СТРОГО менше, інакше об’єкти дублюються у видачі.
        # WARN: y > {sw_segment_y} повинно бути СТРОГО більше, інакше об’єкти дублюються у видачі.
        query = "SELECT DISTINCT unnest(ids), id FROM {table} " \
                "   WHERE tid={tid} AND zoom={zoom} AND " \
                "      (x >= {ne_segment_x} AND x < {sw_segment_x}) AND " \
                "      (y <= {ne_segment_y} AND y > {sw_segment_y});" \
            .format(
                table=cls._meta.db_table,
                tid=tid,
                zoom=zoom,
                ne_segment_x=ne_segment_x,
                sw_segment_x=sw_segment_x,
                ne_segment_y=ne_segment_y,
                sw_segment_y=sw_segment_y,
            )

        cursor = cls.cursor() # note: custom cursor here
        cursor.execute(query)

        in_index_publications_ids = [id for id, _ in cursor.fetchall()]
        cursor.close()


        # Little optimization here:
        # if no ids was received from the index than we do not need to fire additional sql requests
        if not in_index_publications_ids:
            return {}, []


        # dropping publications ids, that was already excluded on previous iterations
        # (conversion to set is needed to prevent duplicated ids into sql query)
        in_index_publications_ids = set(in_index_publications_ids) - set(excluded_ids_list)


        markers = index.brief_queryset().filter(publication_id__in=in_index_publications_ids)
        filtered_markers = index.apply_filters(filters, markers)


        briefs, processed_ids = dict(), list()
        for marker in filtered_markers:
            coordinates = '{lat}:{lng}'.format(lat=marker.lat, lng=marker.lng)
            briefs[coordinates] = index.brief(marker, filters)
            processed_ids.append(marker.publication_id)

        return briefs, processed_ids


    @classmethod
    def cursor(cls):
        """
        NOTE: this method may be used to implement requests routing
              in case when markers indexes are replicated to several hosts.
        :return: database cursor to table with markers indexes.
        """
        return connections[cls.index_db_name].cursor()


    @staticmethod
    def record_lat_lng(record):
        return float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)), \
               float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng))


    @classmethod
    def normalize_viewport_coordinates(cls, ne_lat, ne_lng, sw_lat, sw_lng, zoom):
        ne_lat, ne_lng = cls.grid.normalize_lat_lng(ne_lat, ne_lng)
        sw_lat, sw_lng = cls.grid.normalize_lat_lng(sw_lat, sw_lng)

        # # розширимо сегмент, щоб захопити суміжні області
        ne_lat += 1
        ne_lng -= 1

        sw_lat -= 1
        sw_lng += 1


        # Округляємо передані координати до більшого
        # Справа у тому, що координати передаються у вигляді числа з плаваючою крапкою,
        # і часто мають вигляд хх.ууу, а в індексі всі координати в цілих числах.
        # Якщо не округляти до більшого, то на етапі вибірки координати будуть обрізані до цілого,
        # шляхом відкидання дробової частини. Через це деякі сегменти карти можуть випадати з видачі.
        ne_lat = math.ceil(ne_lat)
        ne_lng = math.floor(ne_lng)

        sw_lat = math.floor(sw_lat)
        sw_lng = math.ceil(sw_lng)


        # На великих масштабах буває так, що координати збігаються,
        # а у вибірці стоїть умова <= && > , і якщо координати однакові, вибірка, логічно, не спрацьовує.
        if ne_lat == sw_lat:
            ne_lat -= 1
            sw_lat += 1

        if ne_lng == sw_lng:
            ne_lng -= 1
            sw_lng += 1


        # Повертаємо координатний прямокутник таким чином, щоб ne точно був на своєму місці.
        # Таким чином уберігаємось від випадків, коли координати передані некоректно,
        # або в залежності від форми Землі сегмент деформується і набирає неправильної форми.
        if ne_lat < sw_lat:
            sw_lat, ne_lat = ne_lat, sw_lat

        if ne_lng > sw_lng:
            sw_lng, ne_lng = ne_lng, sw_lng

        ne_segment_x, ne_segment_y = cls.grid.segment_xy(ne_lat, ne_lng, zoom)
        sw_segment_x, sw_segment_y = cls.grid.segment_xy(sw_lat, sw_lng, zoom)


        # # Заглушка від DDos
        # lng_segments_count = (sw_segment_x - ne_segment_x) // cls.grid.step_on_lng(zoom)
        # if lng_segments_count == 0:
        #     lng_segments_count = 1
        #
        # lat_segments_count = (ne_segment_y - sw_segment_y) // cls.grid.step_on_lat(zoom)
        # if lat_segments_count == 0:
        #     lat_segments_count = 1
        #
        #
        # total_segments_count = lat_segments_count * lng_segments_count
        # if total_segments_count > 128:
        #     raise TooBigTransaction()


        return ne_segment_x, ne_segment_y, \
               sw_segment_x, sw_segment_y