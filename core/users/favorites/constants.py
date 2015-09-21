# coding=utf-8
from core.users.favorites.models import *


FAVORITES_MODELS = {
    OBJECTS_TYPES.flat(): FlatsFavorites,
    OBJECTS_TYPES.house(): HousesFavorites,
    OBJECTS_TYPES.room(): RoomsFavorites,

    OBJECTS_TYPES.trade(): TradesFavorites,
    OBJECTS_TYPES.office(): OfficesFavorites,
    OBJECTS_TYPES.warehouse(): WarehousesFavorites,

    OBJECTS_TYPES.garage(): GaragesFavorites,
    OBJECTS_TYPES.land(): LandsFavorites,
}