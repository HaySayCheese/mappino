from django.conf.urls import patterns, url
from apps.main.api.correspondence.ajax import SendMessageFromClient, SendCallRequestFromClient
from apps.main.api.markers.ajax import Markers
from apps.main.api.publications.ajax import DetailedView, Claims
from apps.main.api.realtors_contacts.ajax import RealtorsContacts
# from apps.main.api.realtors_pages.ajax import RealtorsData, RealtorsMarkers


urlpatterns = patterns('apps.main.api',
    # markers output
    url(r'^ajax/api/markers/$', Markers.as_view()),


    # detailed
    url(r'^ajax/api/detailed/publication/(\d+):(\w+)/$', DetailedView.as_view()),
    url(r'^ajax/api/detailed/publication/(\d+:\w+)/contacts/$', RealtorsContacts.as_view()),


    # correspondence
    url(r'^ajax/api/notifications/send-message/(\d+:\w+)/$', SendMessageFromClient.as_view()),
    url(r'^ajax/api/notifications/send-call-request/(\d+:\w+)/$', SendCallRequestFromClient.as_view()),


    # claims
    url(r'^ajax/api/publications/(\d+):(\w+)/claims/$', Claims.List.as_view()),


    # # realtors pages
    # url(r'^ajax/api/realtors-pages/([A-z]+)/data/$', RealtorsData.as_view()),
    # url(r'^ajax/api/realtors-pages/([A-z]+)/markers/(\d+)/$', RealtorsMarkers.as_view()),
)