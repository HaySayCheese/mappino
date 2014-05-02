from django.conf.urls import patterns, url
from apps.main.api.correspondence.ajax import SendMessageFromClient, SendCallRequestFromClient
from apps.main.api.realtors_contacts.ajax import RealtorsContacts
from core.publications.ajax.main import DetailedView


urlpatterns = patterns('apps.main.api',
	# markers output
	url(r'^ajax/api/markers/$', 'markers.ajax.markers'),


    # detailed
    url(r'^ajax/api/detailed/publication/(\d+:\d+)/$', DetailedView.as_view()),
    url(r'^ajax/api/detailed/publication/(\d+:\d+)/contacts/$', RealtorsContacts.as_view()),


    # correspondence
    url(r'^ajax/api/notifications/send-message/(\d+:\d+)/$', SendMessageFromClient.as_view()),
    url(r'^ajax/api/notifications/send-call-request/(\d+:\d+)/$', SendCallRequestFromClient.as_view()),
)