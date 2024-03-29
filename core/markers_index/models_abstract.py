# coding=utf-8
import datetime
import dateutil.parser
import pytz
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Q

from collective.exceptions import InvalidArgument
from core.currencies.constants import CURRENCIES
from core.currencies.currencies_manager import convert as convert_price
from core.publications.constants import \
    HEAD_MODELS, LIVING_RENT_PERIODS, MARKET_TYPES, OBJECTS_TYPES, DAILY_RENT_RESERVATIONS_MODELS


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
    publication_id = models.PositiveIntegerField(db_index=True)
    hash_id = models.TextField()
    photo_thumbnail_url = models.TextField()

    # lat, lng дублюються в індексі щоб уникнути зайвого join-а з таблицею даних по оголошеннях.
    # Аналогічним чином дублюються всі дані, які, так чи інакше, формують видачу по фільтрах,
    # в тому числі в дочірніх індексах.
    lat = models.FloatField()
    lng = models.FloatField()

    class Meta:
        abstract = True

    @classmethod
    def remove(cls, hid, using=None):
        """
        Removes publication with head id == hid.

        :param hid: id of the head record.
        """
        cls.objects.using(using)\
            .filter(publication_id=hid)\
            .delete()

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
            'hid': marker.hash_id,
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
        result = u'{:.0f}'\
            .format(converted_price)\
            .replace(',', ' ')  # форматування на наш лад

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
        if period == 0:
            markers = markers.filter(period_sid=LIVING_RENT_PERIODS.daily())
        else:
            markers = markers.filter(~Q(period_sid=LIVING_RENT_PERIODS.daily()))

        return markers

    @staticmethod  # sid
    def apply_market_type_filter(filters, markers):
        market_type_sid = filters.get(u'm_t_sid')
        if market_type_sid is None:
            # note: filters may not contain market type sid.
            return markers

        elif market_type_sid == MARKET_TYPES.new_building():
            markers = markers.filter(market_type_sid=MARKET_TYPES.new_building())
            return markers

        elif market_type_sid == MARKET_TYPES.secondary_market():
            markers = markers.filter(market_type_sid=MARKET_TYPES.secondary_market())
            return markers

        # note: filters may not contain valid market type sid.
        # in this case this filter should not be applied.
        return markers


class AbstractIndexWithDailyRent(AbstractBaseIndex):
    # WARN: index for this field is added into migration by RunSQL.
    # django does not support indexing in array fields.

    # note: db_index is not useful for querying.
    days_booked = ArrayField(
        base_field=models.PositiveIntegerField(), null=False, default='{}')

    class Meta:
        abstract = True

    @classmethod  # range
    def apply_daily_rent_dates_filter(cls, filters, markers):
        date_enter = filters.get('r_d_min')
        date_leave = filters.get('r_d_max')

        if not date_enter or not date_leave:
            # dates range can't be build
            return markers

        # the input dates should be converted to utc for prefer processing requests from various timezones
        date_enter = dateutil.parser.parse(date_enter).replace(hour=12).astimezone(pytz.utc)
        date_leave = dateutil.parser.parse(date_leave).replace(hour=12).astimezone(pytz.utc)

        dates_should_be_free = cls.generate_optimized_integer_dates_range(date_enter, date_leave)
        markers = markers.exclude(days_booked__contains=dates_should_be_free)

        return markers

    def reload_booked_days(self):
        assert self.tid is not None

        reservations_model = DAILY_RENT_RESERVATIONS_MODELS[self.tid]

        # To achieve the best performance, booked days are stored as int values.
        # Int values takes less space in memory and indexes on them are more efficient.
        # The format for int value is "yyyymmdd".
        days_booked = []

        for period in reservations_model.objects.reserved_periods(self.publication_id):
            days_booked.extend(self.generate_optimized_integer_dates_range(period.date_enter, period.date_leave))

        self.days_booked = list(set(days_booked))
        self.save()

    @staticmethod
    def generate_optimized_integer_dates_range(datetime_from, datetime_to):
        assert datetime_from.tzinfo == pytz.utc
        assert datetime_to.tzinfo == pytz.utc

        dates = []
        current_dt = datetime_from
        while current_dt < datetime_to:
            date_str = '{yyyy:04d}{mm:02d}{dd:02d}'\
                .format(yyyy=current_dt.year, mm=current_dt.month, dd=current_dt.day)

            dates.append(int(date_str))
            current_dt += datetime.timedelta(days=1)

        return dates


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
        markers = cls.apply_market_type_filter(filters, markers)
        markers = cls.apply_price_filter(filters, markers)

        markers = cls.apply_halls_area_filter(filters, markers)
        markers = cls.apply_total_area_filter(filters, markers)
        return markers

    @classmethod
    def brief_queryset(cls):
        queryset = super(AbstractTradesIndex, cls).brief_queryset()
        return queryset.only('total_area')

    @classmethod
    def brief(cls, marker, filters=None):
        brief = super(AbstractTradesIndex, cls).brief(marker, filters)
        brief['title'] = u'Торг. помещение, {:.0f} м².'.format(marker.total_area)   # tr
        brief['d0'] = u'{:.0f}м²'.format(marker.total_area)
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
        # note: offices should not have market type filter because it is not logic.

        markers = cls.apply_price_filter(filters, markers)
        markers = cls.apply_total_area_filter(filters, markers)
        markers = cls.apply_cabinets_count_filter(filters, markers)
        return markers

    @classmethod
    def brief_queryset(cls):
        queryset = super(AbstractOfficesIndex, cls).brief_queryset()
        return queryset.only('total_area')

    @classmethod
    def brief(cls, marker, filters=None):
        brief = super(AbstractOfficesIndex, cls).brief(marker, filters)
        brief['title'] = u'Офис, {:.0f} м².'.format(marker.total_area) # tr
        brief['d0'] = u'{:.0f}м²'.format(marker.total_area)
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
        markers = cls.apply_market_type_filter(filters, markers)
        markers = cls.apply_price_filter(filters, markers)

        markers = cls.apply_halls_area_filter(filters, markers)
        return markers

    @classmethod
    def brief_queryset(cls):
        queryset = super(AbstractWarehousesIndex, cls).brief_queryset()
        return queryset.only('halls_area')

    @classmethod
    def brief(cls, marker, filters=None):
        brief = super(AbstractWarehousesIndex, cls).brief(marker, filters)
        brief['title'] = u'Склад, {:.0f} м².'.format(marker.halls_area) # tr
        brief['d0'] = u'{:.0f}м²'.format(marker.halls_area)
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
        # note: garages should not have market type filter because it is not logic.

        markers = cls.apply_price_filter(filters, markers)
        markers = cls.apply_area_filter(filters, markers)
        return markers

    @classmethod
    def brief_queryset(cls):
        queryset = super(AbstractGaragesIndex, cls).brief_queryset()
        return queryset.only('area')

    @classmethod
    def brief(cls, marker, filters=None):
        brief = super(AbstractGaragesIndex, cls).brief(marker, filters)
        brief['title'] = u'Гараж, {:.0f} м².'.format(marker.area) # tr
        brief['d0'] = u'{:.0f}м²'.format(marker.area)
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
        # note: lands should not have market type filter because it is not logic.

        markers = cls.apply_price_filter(filters, markers)
        markers = cls.apply_area_filter(filters, markers)
        return markers

    @classmethod
    def brief_queryset(cls):
        queryset = super(AbstractLandsIndex, cls).brief_queryset()
        return queryset.only('area')

    @classmethod
    def brief(cls, marker, filters=None):
        brief = super(AbstractLandsIndex, cls).brief(marker, filters)
        brief['title'] = u'Зем. участок, {:.0f} м².'.format(marker.area)    # tr
        brief['d0'] = u'{:.0f}м²'.format(marker.area)
        return brief
