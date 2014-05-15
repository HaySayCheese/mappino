from apps.cabinet.api.support.ajax import Support
from django.conf.urls import patterns, url


urlpatterns = patterns('',
	url(r'^ajax/api/cabinet/support/tickets/$', Support.Tickets.as_view()),
    url(r'^ajax/api/cabinet/support/tickets/(\d+)/close/$', Support.CloseTicket.as_view()),
	url(r'^ajax/api/cabinet/support/tickets/(\d+)/messages/$', Support.Messages.as_view()),

    #-- web hooks
    # url(r'^web-hooks/support/agents-answers/$', IncomingAnswer.as_view()),
)