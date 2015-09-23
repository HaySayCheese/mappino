# coding=utf-8
from core.publications.models import *
from core.users.favorites.models_abstract import AbstractFavorites
from core.publications.types_bases import *


class FlatsFavorites(FlatBase, AbstractFavorites):
    publication = models.ForeignKey(FlatsHeads)


    class Meta:
        db_table = 'favorites_flats'



class HousesFavorites(HouseBase, AbstractFavorites):
    publication = models.ForeignKey(HousesHeads)


    class Meta:
        db_table = 'favorites_houses'


class RoomsFavorites(RoomBase, AbstractFavorites):
    publication = models.ForeignKey(RoomsHeads)


    class Meta:
        db_table = 'favorites_rooms'



class LandsFavorites(LandBase, AbstractFavorites):
    publication = models.ForeignKey(LandsHeads)


    class Meta:
        db_table = 'favorites_lands'



class GaragesFavorites(GarageBase, AbstractFavorites):
    publication = models.ForeignKey(GaragesHeads)


    class Meta:
        db_table = 'favorites_garages'



class OfficesFavorites(OfficeBase, AbstractFavorites):
    publication = models.ForeignKey(OfficesHeads)


    class Meta:
        db_table = 'favorites_offices'



class TradesFavorites(TradeBase, AbstractFavorites):
    publication = models.ForeignKey(TradesHeads)


    class Meta:
        db_table = 'favorites_trades'



class WarehousesFavorites(WarehouseBase, AbstractFavorites):
    publication = models.ForeignKey(WarehousesHeads)


    class Meta:
        db_table = 'favorites_warehouses'