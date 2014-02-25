#coding=utf-8
from django.dispatch.dispatcher import receiver

from core.markers_servers.servers import HousesMarkersManager, FlatsMarkersManager, ApartmentsMarkersManager, \
	DachasMarkersManager, CottagesMarkersManager, RoomsMarkersManager, TradesMarkersManager, OfficesMarkersManager, \
	WarehousesMarkersManager, BusinessesMarkersManager, CateringsMarkersManager, GaragesMarkersManager, LandsMarkersManager
from core.publications.constants import OBJECTS_TYPES
from core.publications.models_signals import record_published



MARKERS_SERVERS = {
	# Жилая недвижимость
	OBJECTS_TYPES.house():      HousesMarkersManager(),
	OBJECTS_TYPES.flat():       FlatsMarkersManager(),
	OBJECTS_TYPES.apartments(): ApartmentsMarkersManager(),
	OBJECTS_TYPES.dacha():      DachasMarkersManager(),
	OBJECTS_TYPES.cottage():    CottagesMarkersManager(),
	OBJECTS_TYPES.room():       RoomsMarkersManager(),

	# Коммерческая недвижимость
    OBJECTS_TYPES.trade():      TradesMarkersManager(),
    OBJECTS_TYPES.office():     OfficesMarkersManager(),
    OBJECTS_TYPES.warehouse():  WarehousesMarkersManager(),
    OBJECTS_TYPES.business():   BusinessesMarkersManager(),
    OBJECTS_TYPES.catering():   CateringsMarkersManager(),

    # Другая недвижимость
    OBJECTS_TYPES.garage():     GaragesMarkersManager(),
    OBJECTS_TYPES.land():       LandsMarkersManager(),
}


@receiver(record_published)
def add_publication_marker(sender, **kwargs):
	MARKERS_SERVERS[kwargs['tid']].add_publication(kwargs['hid'])