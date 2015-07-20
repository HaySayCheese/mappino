# coding=utf-8
import math

from django.conf import settings
from django.db import models, connections

from djorm_pgarray.fields import BigIntegerArrayField

from collective.exceptions import InvalidArgument
from core.markers_handler.classes import Grid
from core.publications.constants import OBJECTS_TYPES, HEAD_MODELS
from core.markers_handler.abstract_models import \
    AbstractBaseIndex, AbstractTradesIndex, AbstractOfficesIndex, AbstractWarehousesIndex, \
    AbstractGaragesIndex, AbstractLandsIndex


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
    # constants
    tid = OBJECTS_TYPES.house()
    
    # fields
    price = models.FloatField(db_index=True)
    currency_sid = models.PositiveSmallIntegerField()

    market_type_sid = models.PositiveSmallIntegerField(db_index=True)
    total_area = models.FloatField(db_index=True)
    rooms_count = models.PositiveSmallIntegerField(db_index=True)
    floors_count = models.PositiveSmallIntegerField(db_index=True)
    hot_water = models.BooleanField(db_index=True)
    cold_water = models.BooleanField(db_index=True)
    gas = models.BooleanField(db_index=True)
    electricity = models.BooleanField(db_index=True)
    heating_type_sid = models.PositiveSmallIntegerField(db_index=True)


    class Meta:
        db_table = 'index_houses_sale'


    @classmethod
    def add(cls, record, using=None):
        cls.objects.using(using).create(
            publication_id=record.id,
            hash_id=record.hash_id,
            lat=float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
            lng=float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

            price=record.sale_terms.price,

            market_type_sid=record.body.market_type_sid,
            currency_sid=record.sale_terms.currency_sid,
            total_area=record.body.total_area,
            rooms_count=record.body.rooms_count,
            floors_count=record.body.floors_count,
            hot_water=record.body.hot_water,
            cold_water=record.body.cold_water,
            gas=record.body.gas,
            electricity=record.body.electricity,
            heating_type_sid=record.body.heating_type_sid,
        )


    @classmethod
    def min_add_queryset(cls):
        model = HEAD_MODELS[OBJECTS_TYPES.house()]
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
            'body__rooms_count',
            'body__floors_count',
            'body__hot_water',
            'body__cold_water',
            'body__electricity',
            'body__gas',
            'body__heating_type_sid',

            'sale_terms__price',
            'sale_terms__currency_sid'
        )


    @classmethod
    def apply_filters(cls, filters, markers):
        cls.apply_price_filter(filters, markers)

        cls.apply_market_type_filter(filters, markers)
        cls.apply_total_area_filter(filters, markers)
        cls.apply_rooms_count_filter(filters, markers)
        cls.apply_floors_count_filter(filters, markers)
        cls.apply_electricity_filter(filters, markers)
        cls.apply_gas_filter(filters, markers)
        cls.apply_hot_water_filter(filters, markers)
        cls.apply_cold_water_filter(filters, markers)
        cls.apply_heating_type_filter(filters, markers)
        return markers


class HousesRentIndex(AbstractBaseIndex):
    # costants
    tid = OBJECTS_TYPES.house()

    # fields
    price = models.FloatField(db_index=True)
    currency_sid = models.PositiveSmallIntegerField()
    period_sid = models.PositiveSmallIntegerField(db_index=True)
    persons_count = models.PositiveSmallIntegerField(db_index=True)

    market_type_sid = models.PositiveSmallIntegerField(db_index=True)
    total_area = models.FloatField(db_index=True)
    rooms_count = models.PositiveSmallIntegerField(db_index=True)
    floors_count = models.PositiveSmallIntegerField(db_index=True)
    hot_water = models.BooleanField(db_index=True)
    cold_water = models.BooleanField(db_index=True)
    gas = models.BooleanField(db_index=True)
    electricity = models.BooleanField(db_index=True)
    heating_type_sid = models.PositiveSmallIntegerField(db_index=True)


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

            market_type_sid=record.body.market_type_sid,
            total_area=record.body.total_area,
            rooms_count=record.body.rooms_count,
            floors_count=record.body.floors_count,
            hot_water=record.body.hot_water,
            cold_water=record.body.cold_water,
            gas=record.body.gas,
            electricity=record.body.electricity,
            heating_type_sid=record.body.heating_type_sid,
        )


    @classmethod
    def min_add_queryset(cls):
        model = HEAD_MODELS[OBJECTS_TYPES.house()]
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
            'body__rooms_count',
            'body__floors_count',
            'body__hot_water',
            'body__cold_water',
            'body__electricity',
            'body__gas',
            'body__heating_type_sid',

            'rent_terms__period_sid',
            'rent_terms__price',
            'rent_terms__currency_sid',
            'rent_terms__persons_count',
        )


    @classmethod
    def apply_filters(cls, filters, markers):
        cls.apply_price_filter(filters, markers)
        cls.apply_living_rent_period_filter(filters, markers)
        cls.apply_persons_count_filter(filters, markers)

        cls.apply_market_type_filter(filters, markers)
        cls.apply_total_area_filter(filters, markers)
        cls.apply_rooms_count_filter(filters, markers)
        cls.apply_floors_count_filter(filters, markers)
        cls.apply_electricity_filter(filters, markers)
        cls.apply_gas_filter(filters, markers)
        cls.apply_hot_water_filter(filters, markers)
        cls.apply_cold_water_filter(filters, markers)
        cls.apply_heating_type_filter(filters, markers)
        return markers


class RoomsSaleIndex(AbstractBaseIndex):
    # constants
    tid = OBJECTS_TYPES.room()

    # fields
    price = models.FloatField(db_index=True)
    currency_sid = models.PositiveSmallIntegerField()

    market_type_sid = models.PositiveSmallIntegerField(db_index=True)
    area = models.FloatField(db_index=True)
    floor = models.PositiveSmallIntegerField(db_index=True)
    floor_type_sid = models.PositiveSmallIntegerField(db_index=True)
    lift = models.BooleanField(db_index=True)
    hot_water = models.BooleanField(db_index=True)
    cold_water = models.BooleanField(db_index=True)
    gas = models.BooleanField(db_index=True)
    electricity = models.BooleanField(db_index=True)


    class Meta:
        db_table = 'index_rooms_sale'


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
            area=record.body.area,
            floor=record.body.floor,
            floor_type_sid=record.body.floor_type_sid,
            lift=record.body.lift,
            hot_water=record.body.hot_water,
            cold_water=record.body.cold_water,
            electricity=record.body.electricity,
            gas=record.body.gas,
        )


    @classmethod
    def min_add_queryset(cls):
        model = HEAD_MODELS[OBJECTS_TYPES.room()]
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
            'body__area',
            'body__floor',
            'body__floor_type_sid',
            'body__lift',
            'body__hot_water',
            'body__cold_water',
            'body__electricity',
            'body__gas',
        )


    @classmethod
    def apply_filters(cls, filters, markers):
        cls.apply_price_filter(filters, markers)

        cls.apply_market_type_filter(filters, markers)
        cls.apply_area_filter(filters, markers)
        cls.apply_floor_filter(filters, markers)
        cls.apply_electricity_filter(filters, markers)
        cls.apply_gas_filter(filters, markers)
        cls.apply_hot_water_filter(filters, markers)
        cls.apply_cold_water_filter(filters, markers)
        cls.apply_lift_filter(filters, markers)
        return markers


class RoomsRentIndex(AbstractBaseIndex):
    # constants
    tid = OBJECTS_TYPES.room()

    # fields
    price = models.FloatField(db_index=True)
    currency_sid = models.PositiveSmallIntegerField()
    period_sid = models.PositiveSmallIntegerField(db_index=True)
    persons_count = models.PositiveSmallIntegerField(db_index=True)

    market_type_sid = models.PositiveSmallIntegerField(db_index=True)
    area = models.FloatField(db_index=True)
    floor = models.PositiveSmallIntegerField(db_index=True)
    floor_type_sid = models.PositiveSmallIntegerField(db_index=True)
    lift = models.BooleanField(db_index=True)
    hot_water = models.BooleanField(db_index=True)
    cold_water = models.BooleanField(db_index=True)
    gas = models.BooleanField(db_index=True)
    electricity = models.BooleanField(db_index=True)


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

            market_type_sid=record.body.market_type_sid,
            area=record.body.area,
            floor=record.body.floor,
            floor_type_sid=record.body.floor_type_sid,
            lift=record.body.lift,
            hot_water=record.body.hot_water,
            cold_water=record.body.cold_water,
            electricity=record.body.electricity,
            gas=record.body.gas,
        )


    @classmethod
    def min_add_queryset(cls):
        model = HEAD_MODELS[OBJECTS_TYPES.room()]
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
        )


    @classmethod
    def apply_filters(cls, filters, markers):
        cls.apply_living_rent_period_filter(filters, markers)
        cls.apply_price_filter(filters, markers)
        cls.apply_persons_count_filter(filters, markers)

        cls.apply_market_type_filter(filters, markers)
        cls.apply_area_filter(filters, markers)
        cls.apply_floor_filter(filters, markers)
        cls.apply_electricity_filter(filters, markers)
        cls.apply_gas_filter(filters, markers)
        cls.apply_hot_water_filter(filters, markers)
        cls.apply_cold_water_filter(filters, markers)
        cls.apply_lift_filter(filters, markers)
        return markers


# -- commercial real estate
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

            price=record.sale_terms.price,
            currency_sid=record.sale_terms.currency_sid,

            market_type_sid=record.body.market_type_sid,
            halls_area=record.body.total_area,
            total_area=record.body.total_area,
            building_type_sid=record.body.building_type_sid,
            hot_water=record.body.hot_water,
            cold_water=record.body.cold_water,
            gas=record.body.gas,
            electricity=record.body.electricity,
            sewerage=record.body.sewerage,
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

            'sale_terms__price',
            'sale_terms__currency_sid',

            'body__market_type_sid',
            'body__halls_area',
            'body__total_area',
            'body__building_type_sid',
            'body__hot_water',
            'body__cold_water',
            'body__electricity',
            'body__gas',
            'body__sewerage',
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

            price=record.rent_terms.price,
            currency_sid=record.rent_terms.currency_sid,

            market_type_sid=record.body.market_type_sid,
            halls_area=record.body.total_area,
            total_area=record.body.total_area,
            building_type_sid=record.body.building_type_sid,
            hot_water=record.body.hot_water,
            cold_water=record.body.cold_water,
            gas=record.body.gas,
            electricity=record.body.electricity,
            sewerage=record.body.sewerage,
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

            'rent_terms__price',
            'rent_terms__currency_sid',

            'body__market_type_sid',
            'body__halls_area',
            'body__total_area',
            'body__building_type_sid',
            'body__hot_water',
            'body__cold_water',
            'body__electricity',
            'body__gas',
            'body__sewerage',
        )


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

            price=record.sale_terms.price,
            currency_sid=record.sale_terms.currency_sid,

            market_type_sid=record.body.market_type_sid,
            total_area=record.body.total_area,
            cabinets_count=record.body.cabinets_count,
            hot_water=record.body.hot_water,
            cold_water=record.body.cold_water,
            security=record.body.security,
            kitchen=record.body.kitchen,
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

            'sale_terms__price',
            'sale_terms__currency_sid',

            'body__market_type_sid',
            'body__total_area',
            'body__cabinets_count',
            'body__hot_water',
            'body__cold_water',
            'body__security',
            'body__kitchen',
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

            price=record.rent_terms.price,
            currency_sid=record.rent_terms.currency_sid,

            market_type_sid=record.body.market_type_sid,
            total_area=record.body.total_area,
            cabinets_count=record.body.cabinets_count,
            hot_water=record.body.hot_water,
            cold_water=record.body.cold_water,
            security=record.body.security,
            kitchen=record.body.kitchen,
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

            'rent_terms__price',
            'rent_terms__currency_sid',

            'body__market_type_sid',
            'body__total_area',
            'body__cabinets_count',
            'body__hot_water',
            'body__cold_water',
            'body__security',
            'body__kitchen',
        )


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

            price=record.sale_terms.price,
            currency_sid=record.sale_terms.currency_sid,

            market_type_sid=record.body.market_type_sid,
            halls_area=record.body.halls_area,
            hot_water=record.body.hot_water,
            cold_water=record.body.cold_water,
            electricity=record.body.electricity,
            gas=record.body.gas,
            fire_alarm=record.body.fire_alarm,
            security_alarm=record.body.security_alarm,
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

            'sale_terms__price',
            'sale_terms__currency_sid',

            'body__market_type_sid',
            'body__halls_area',
            'body__hot_water',
            'body__cold_water',
            'body__electricity',
            'body__gas',
            'body__fire_alarm',
            'body__security_alarm',
        )


class WarehousesRentIndex(AbstractWarehousesIndex):
    class Meta:
        db_table = 'index_warehouses_rent'


    @classmethod
    def add(cls, record, using=None):
        cls.objects.using(using).create(
            publication_id=record.id,
            hash_id=record.hash_id,
            lat=float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
            lng=float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

            price=record.rent_terms.price,
            currency_sid=record.rent_terms.currency_sid,

            market_type_sid=record.body.market_type_sid,
            halls_area=record.body.halls_area,
            hot_water=record.body.hot_water,
            cold_water=record.body.cold_water,
            electricity=record.body.electricity,
            gas=record.body.gas,
            fire_alarm=record.body.fire_alarm,
            security_alarm=record.body.security_alarm,
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

            'rent_terms__price',
            'rent_terms__currency_sid',

            'body__market_type_sid',
            'body__halls_area',
            'body__hot_water',
            'body__cold_water',
            'body__electricity',
            'body__gas',
            'body__fire_alarm',
            'body__security_alarm',
        )


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

            'sale_terms__price',
            'sale_terms__currency_sid',

            'body__market_type_sid',
            'body__area',
            'body__ceiling_height',
            'body__pit',
        )


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
            area=record.body.area,
            ceiling_height=record.body.ceiling_height,
            pit=record.body.pit,
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

            price=record.rent_terms.price,
            currency_sid=record.rent_terms.currency_sid,

            area=record.body.area,
            ceiling_height=record.body.ceiling_height,
            pit=record.body.pit,
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

            'rent_terms__price',
            'rent_terms__currency_sid',

            'body__area',
            'body__ceiling_height',
            'body__pit',
        )


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

            price=record.sale_terms.price,
            currency_sid=record.sale_terms.currency_sid,

            area=record.body.area,
            water=record.body.water,
            electricity=record.body.electricity,
            gas=record.body.gas,
            sewerage=record.body.sewerage,
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

            'sale_terms__price',
            'sale_terms__currency_sid',

            'body__area',
            'body__water',
            'body__electricity',
            'body__gas',
            'body__sewerage',
        )


class LandsRentIndex(AbstractLandsIndex):
    class Meta:
        db_table = 'index_lands_rent'


    @classmethod
    def add(cls, record, using=None):
        cls.objects.using(using).create(
            publication_id=record.id,
            hash_id=record.hash_id,
            lat=float('{0}.{1}{2}'.format(record.degree_lat, record.segment_lat, record.pos_lat)),
            lng=float('{0}.{1}{2}'.format(record.degree_lng, record.segment_lng, record.pos_lng)),

            price=record.rent_terms.price,
            currency_sid=record.rent_terms.currency_sid,

            area=record.body.area,
            water=record.body.water,
            electricity=record.body.electricity,
            gas=record.body.gas,
            sewerage=record.body.sewerage,
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

            'rent_terms__price',
            'rent_terms__currency_sid',

            'body__area',
            'body__water',
            'body__electricity',
            'body__gas',
            'body__sewerage',
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
        OBJECTS_TYPES.garage(): GaragesSaleIndex,
        OBJECTS_TYPES.land(): LandsSaleIndex,
    }
    commercial_rent_indexes = {
        OBJECTS_TYPES.trade(): TradesRentIndex,
        OBJECTS_TYPES.office(): OfficesRentIndex,
        OBJECTS_TYPES.warehouse(): WarehousesRentIndex,
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
        assert record.degree_lat is not None
        assert record.segment_lat is not None
        assert record.pos_lat is not None
        
        assert record.degree_lng is not None
        assert record.segment_lng is not None
        assert record.pos_lng is not None


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