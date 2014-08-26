#coding=utf-8
from django.dispatch.dispatcher import receiver
from core.markers_servers.count_servers import MPSManager

from core.markers_servers.servers import \
	HousesMarkersManager, FlatsMarkersManager, ApartmentsMarkersManager, \
	CottagesMarkersManager, RoomsMarkersManager, TradesMarkersManager, \
	OfficesMarkersManager, WarehousesMarkersManager, BusinessesMarkersManager, \
	CateringsMarkersManager, GaragesMarkersManager, LandsMarkersManager
from core.publications import models_signals
from core.publications.constants import OBJECTS_TYPES


MARKERS_SERVERS = {
	# Жилая недвижимость
	OBJECTS_TYPES.house():      HousesMarkersManager(),
	OBJECTS_TYPES.flat():       FlatsMarkersManager(),
	OBJECTS_TYPES.apartments(): ApartmentsMarkersManager(),
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

MARKERS_PER_SEGMENT_COUNT_MANAGER = MPSManager()


@receiver(models_signals.before_publish)
def add_publication_marker(sender, **kwargs):
	tid = kwargs['tid']
	hid = kwargs['hid']

	MARKERS_SERVERS[tid].add_publication(hid)
	MARKERS_PER_SEGMENT_COUNT_MANAGER.add_publication(tid, hid)


@receiver(models_signals.before_unpublish)
@receiver(models_signals.moved_to_trash)
@receiver(models_signals.deleted_permanent)
def remove_publication_marker(sender, **kwargs):
	tid = kwargs['tid']
	hid = kwargs['hid']

	MARKERS_SERVERS[tid].remove_publication(hid)
	MARKERS_PER_SEGMENT_COUNT_MANAGER.remove_publication(tid, hid)