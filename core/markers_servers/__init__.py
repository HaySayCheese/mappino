from django.dispatch.dispatcher import receiver

from core.markers_servers.servers import HousesMarkersServer
from core.publications.models_signals import house_published



__houses_markers_server = HousesMarkersServer()

@receiver(house_published)
def add_house_marker(sender, **kwargs):
	__houses_markers_server.add_publication(kwargs['id'])


def get_house_markers(ne, sw):
	return __houses_markers_server.markers(ne, sw, None)