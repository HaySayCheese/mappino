# coding=utf-8
from core.publications.constants import OBJECTS_TYPES


class FlatBase(object):
    # constants
    tid = OBJECTS_TYPES.flat()


class HouseBase(object):
    # constants
    tid = OBJECTS_TYPES.house()


class RoomBase(object):
    # constants
    tid = OBJECTS_TYPES.room()


class LandBase(object):
    # constants
    tid = OBJECTS_TYPES.land()


class GarageBase(object):
    # constants
    tid = OBJECTS_TYPES.garage()


class OfficeBase(object):
    # constants
    tid = OBJECTS_TYPES.office()


class TradeBase(object):
    # constants
    tid = OBJECTS_TYPES.trade()


class WarehouseBase(object):
    # constants
    tid = OBJECTS_TYPES.warehouse()