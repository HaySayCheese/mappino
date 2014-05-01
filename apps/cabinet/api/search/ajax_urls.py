from django.conf.urls import patterns, url


urlpatterns = patterns('apps.cabinet.api',
	url(r'^ajax/api/cabinet/search/$', 'search.ajax.search'),
)