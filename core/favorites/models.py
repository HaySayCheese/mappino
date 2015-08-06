# coding=utf-8
from core.publications.models import *
from core.favorites.models_abstract import AbstractFavorites
from core.users.models import Users


class FlatsFavorites(AbstractFavorites):
    publication = models.ForeignKey(FlatsHeads)


    class Meta:
        db_table = 'favorites_flats'


class HousesFavorites(AbstractFavorites):
    publication = models.ForeignKey(HousesHeads)


    class Meta:
        db_table = 'favorites_houses'


class RoomsFavorites(AbstractFavorites):
    publication = models.ForeignKey(RoomsHeads)


    class Meta:
        db_table = 'favorites_rooms'


class LandsFavorites(AbstractFavorites):
    publication = models.ForeignKey(LandsHeads)


    class Meta:
        db_table = 'favorites_lands'


class GaragesFavorites(AbstractFavorites):
    publication = models.ForeignKey(GaragesHeads)


    class Meta:
        db_table = 'favorites_garages'


class OfficesFavorites(AbstractFavorites):
    publication = models.ForeignKey(OfficesHeads)


    class Meta:
        db_table = 'favorites_offices'


class TradesFavorites(AbstractFavorites):
    publication = models.ForeignKey(TradesHeads)


    class Meta:
        db_table = 'favorites_trades'


class WarehousesFavorites(AbstractFavorites):
    publication = models.ForeignKey(WarehousesHeads)


    class Meta:
        db_table = 'favorites_warehouses'