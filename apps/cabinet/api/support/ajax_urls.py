from django.conf.urls import patterns, url
from core.support.ajax.cabinet import CloseTicket, TicketsView, MessagesView


urlpatterns = patterns('',
	url(r'^ajax/api/cabinet/support/tickets/$', TicketsView.as_view()),
    url(r'^ajax/api/cabinet/support/tickets/(\d+)/close/$', CloseTicket.as_view()),
	url(r'^ajax/api/cabinet/support/tickets/(\d+)/messages/$', MessagesView.as_view()),

    #-- web hooks
    # url(r'^web-hooks/support/agents-answers/$', IncomingAnswer.as_view()),
)