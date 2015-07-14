from apps.cabinet.api.stats.ajax import Stats
from django.conf.urls import patterns, url


urlpatterns = patterns('',
	url(r'^ajax/api/cabinet/stats/publications/(\d+:\w+)/visits/$', Stats.PublicationsVisits.as_view()),
)