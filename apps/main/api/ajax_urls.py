from django.conf.urls import patterns, url
from core.correspondence.ajax.main import NewMessage, NewCallRequest
from core.publications.ajax.main import DetailedView


urlpatterns = patterns('apps.main.api',
	# markers output
	url(r'^ajax/api/markers/$', 'markers.ajax.markers'),


    # detailed
    url(r'^ajax/api/detailed/publication/(\d+:\d+)/$', DetailedView.as_view()),


    # correspondence
    url(r'^ajax/api/notifications/send-message/(\d+:\d+)/$', NewMessage.as_view()),
    url(r'^ajax/api/notifications/send-call-request/(\d+:\d+)/$', NewCallRequest.as_view()),
)