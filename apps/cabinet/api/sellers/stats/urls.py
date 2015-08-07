from django.conf.urls import patterns, url

from apps.cabinet.api.sellers.stats.ajax import Stats

urlpatterns = patterns('',
	url(r'^ajax/api/cabinet/stats/publications/(\d+:\w+)/visits/$', Stats.PublicationsVisits.as_view()),
)