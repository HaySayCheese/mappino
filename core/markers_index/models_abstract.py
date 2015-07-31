# coding=utf-8
from django.db import models
from django.db.models import Q
from collective.exceptions import InvalidArgument
from core.currencies.constants import CURRENCIES
from core.currencies.currencies_manager import convert as convert_price
from core.publications.constants import HEAD_MODELS, FLOOR_TYPES, LIVING_RENT_PERIODS, MARKET_TYPES, HEATING_TYPES, \
    OBJECTS_TYPES
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
    photo_thumbnail_url = models.TextField()

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
    def brief_queryset(cls):
        """
        :returns:
            minimum queryset needed for marker brief performing.
        """
        return cls.objects.all().only(
            'hash_id', 'lat', 'lng', 'photo_thumbnail_url', 'price', 'currency_sid')


    @classmethod
    def brief(cls, marker, filters=None):
        currency = cls.currency_from_filters(filters)
        price = cls.convert_and_format_price(marker.price, marker.currency_sid, currency)

        return {
            'tid': cls.tid,
            'id': marker.hash_id,
            'price': u'{0}{1}'.format(cls.currency_to_str(currency), price),
            'thumbnail_url': marker.photo_thumbnail_url,
        }


    @classmethod
    def min_add_queryset(cls, publication_head_id):  # virtual
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
    def min_remove_queryset(cls, publication_head_id):
        model = HEAD_MODELS[cls.tid]

        return model.objects.\
            filter(id=publication_head_id)\
            .only(
                'id',
                'degree_lat',
                'degree_lng',
                'segment_lat',
                'segment_lng',
                'pos_lat',
                'pos_lng',
            )[:1]


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
            return u'$'
        elif currency == CURRENCIES.eur():
            return u'€'
        elif currency == CURRENCIES.uah():
            return u'₴'
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
        if filters.get('elt') is True:
            return markers.filter(electricity=True)
        return markers


    @staticmethod  # bool
    def apply_gas_filter(filters, markers):
        if filters.get('gas') is True:
            return markers.filter(gas=True)
        return markers


    @staticmethod  # bool
    def apply_hot_water_filter(filters, markers):
        if filters.get('h_w') is True:
            return markers.filter(hot_water=True)
        return markers


    @staticmethod  # bool
    def apply_cold_water_filter(filters, markers):
        if filters.get('c_w') is True:
            return markers.filter(cold_water=True)
        return markers


    @staticmethod  # bool
    def apply_water_filter(filters, markers):
        if filters.get('wtr') is True:
            return markers.filter(water=True)
        return markers


    @staticmethod  # bool
    def apply_sewerage_filter(filters, markers):
        if filters.get('swg') is True:
            return markers.filter(sewerage=True)
        return markers


    @staticmethod  # bool
    def apply_lift_filter(filters, markers):
        if filters.get('lft') is True:
            return markers.filter(lift=True)
        return markers


    @staticmethod  # bool
    def apply_security_filter(filters, markers):
        if filters.get('sct') is True:
            return markers.filter(security=True)
        return markers


    @staticmethod  # bool
    def apply_kitchen_filter(filters, markers):
        if filters.get('ktn') is True:
            return markers.filter(kitchen=True)
        return markers


    @staticmethod  # bool
    def apply_fire_alarm_filter(filters, markers):
        if filters.get('f_a') is True:
            return markers.filter(fire_alarm=True)
        return markers


    @staticmethod  # bool
    def apply_security_alarm_filter(filters, markers):
        if filters.get('s_a') is True:
            return markers.filter(security_alarm=True)
        return markers


    @staticmethod  # bool
    def apply_pit_filter(filters, markers):
        if filters.get('pit') is True:
            return markers.filter(pit=True)
        return markers


class AbstractTradesIndex(AbstractBaseIndex):
    """
    Sale index and rent index of the trades objects contains the same field and the same logic,
    but must use different tables. For this approach we can't simply create sale index,
    and than inherit rent index from it. (Django will generate inappropriate inheritance scheme).

    So abstract index was developed and both sale and rent indexes was derived from it.
    """

    # constants
    tid = OBJECTS_TYPES.trade()

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


    class Meta:
        abstract = True


    @classmethod
    def apply_filters(cls, filters, markers):
        markers = cls.apply_price_filter(filters, markers)

        markers = cls.apply_market_type_filter(filters, markers)
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
    def brief_queryset(cls):
        queryset = super(AbstractTradesIndex, cls).brief_queryset()
        return queryset.only('total_area')


    @classmethod
    def brief(cls, marker, filters=None):
        brief = super(AbstractTradesIndex, cls).brief(marker, filters)
        brief['title'] = u'Торг. помещение, {:.0f} м².'.format(marker.total_area) # tr
        return brief


class AbstractOfficesIndex(AbstractBaseIndex):
    """
    Sale index and rent index of the offices contains the same field and the same logic,
    but must use different tables. For this approach we can't simply create sale index,
    and than inherit rent index from it. (Django will generate inappropriate inheritance scheme).

    So abstract index was developed and both sale and rent indexes was derived from it.
    """

    # constants
    tid = OBJECTS_TYPES.office()

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


    class Meta:
        abstract = True


    @classmethod
    def apply_filters(cls, filters, markers):
        markers = cls.apply_price_filter(filters, markers)

        markers = cls.apply_market_type_filter(filters, markers)
        markers = cls.apply_total_area_filter(filters, markers)
        markers = cls.apply_cabinets_count_filter(filters, markers)
        markers = cls.apply_hot_water_filter(filters, markers)
        markers = cls.apply_cold_water_filter(filters, markers)
        markers = cls.apply_kitchen_filter(filters, markers)
        markers = cls.apply_security_filter(filters, markers)
        return markers


    @classmethod
    def brief_queryset(cls):
        queryset = super(AbstractOfficesIndex, cls).brief_queryset()
        return queryset.only('total_area')


    @classmethod
    def brief(cls, marker, filters=None):
        brief = super(AbstractOfficesIndex, cls).brief(marker, filters)
        brief['title'] = u'Офис, {:.0f} м².'.format(marker.total_area) # tr
        return brief


class AbstractWarehousesIndex(AbstractBaseIndex):
    """
    Sale index and rent index of the warehouses contains the same field and the same logic,
    but must use different tables. For this approach we can't simply create sale index,
    and than inherit rent index from it. (Django will generate inappropriate inheritance scheme).

    So abstract index was developed and both sale and rent indexes was derived from it.
    """
    
    # constants
    tid = OBJECTS_TYPES.warehouse()

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


    class Meta:
        abstract = True


    @classmethod
    def apply_filters(cls, filters, markers):
        markers = cls.apply_price_filter(filters, markers)

        markers = cls.apply_market_type_filter(filters, markers)
        markers = cls.apply_halls_area_filter(filters, markers)
        markers = cls.apply_hot_water_filter(filters, markers)
        markers = cls.apply_cold_water_filter(filters, markers)
        markers = cls.apply_electricity_filter(filters, markers)
        markers = cls.apply_gas_filter(filters, markers)
        markers = cls.apply_fire_alarm_filter(filters, markers)
        markers = cls.apply_security_alarm_filter(filters, markers)
        return markers


    @classmethod
    def brief_queryset(cls):
        queryset = super(AbstractWarehousesIndex, cls).brief_queryset()
        return queryset.only('halls_area')


    @classmethod
    def brief(cls, marker, filters=None):
        brief = super(AbstractWarehousesIndex, cls).brief(marker, filters)
        brief['title'] = u'Склад, {:.0f} м².'.format(marker.halls_area) # tr
        return brief


class AbstractGaragesIndex(AbstractBaseIndex):
    """
    Sale index and rent index of the garages contains the same field and the same logic,
    but must use different tables. For this approach we can't simply create sale index,
    and than inherit rent index from it. (Django will generate inappropriate inheritance scheme).

    So abstract index was developed and both sale and rent indexes was derived from it.
    """

    # constants
    tid = OBJECTS_TYPES.garage()

    # fields
    price = models.FloatField(db_index=True)
    currency_sid = models.PositiveSmallIntegerField()

    area = models.FloatField(db_index=True)
    ceiling_height = models.FloatField(db_index=True)
    pit = models.BooleanField(db_index=True)


    class Meta:
        abstract = True


    @classmethod
    def apply_filters(cls, filters, markers):
        markers = cls.apply_price_filter(filters, markers)

        markers = cls.apply_market_type_filter(filters, markers)
        markers = cls.apply_area_filter(filters, markers)
        markers = cls.apply_ceiling_height_filter(filters, markers)
        markers = cls.apply_pit_filter(filters, markers)
        return markers


    @classmethod
    def brief_queryset(cls):
        queryset = super(AbstractGaragesIndex, cls).brief_queryset()
        return queryset.only('area')


    @classmethod
    def brief(cls, marker, filters=None):
        brief = super(AbstractGaragesIndex, cls).brief(marker, filters)
        brief['title'] = u'Гараж, {:.0f} м².'.format(marker.area) # tr
        return brief


class AbstractLandsIndex(AbstractBaseIndex):
    """
    Sale index and rent index of the lands contains the same field and the same logic,
    but must use different tables. For this approach we can't simply create sale index,
    and than inherit rent index from it. (Django will generate inappropriate inheritance scheme).

    So abstract index was developed and both sale and rent indexes was derived from it.
    """

    # constants
    tid = OBJECTS_TYPES.land()

    # fields
    price = models.FloatField(db_index=True)
    currency_sid = models.PositiveSmallIntegerField()
    
    area = models.FloatField(db_index=True)
    water = models.BooleanField(db_index=True)
    electricity = models.BooleanField(db_index=True)
    gas = models.BooleanField(db_index=True)
    sewerage = models.BooleanField(db_index=True)


    class Meta:
        abstract = True


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
    def brief_queryset(cls):
        queryset = super(AbstractLandsIndex, cls).brief_queryset()
        return queryset.only('area')


    @classmethod
    def brief(cls, marker, filters=None):
        brief = super(AbstractLandsIndex, cls).brief(marker, filters)
        brief['title'] = u'Зем. участок, {:.0f} м².'.format(marker.area) # tr
        return brief