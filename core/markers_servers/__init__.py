from django.dispatch.dispatcher import receiver

from core.markers_servers.servers import HousesMarkersServer
from core.publications.models_signals import house_published



__houses_markers_server = HousesMarkersServer()

@receiver(house_published)
def add_house_marker(sender, **kwargs):
	__houses_markers_server.add_publication(kwargs['id'])