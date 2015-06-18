from django.conf.urls import patterns, url


urlpatterns = patterns('apps.cabinet.api',
	url(r'^ajax/api/cabinet/dirtags/$', 'dirtags.ajax.dirtags_handler'),
    url(r'^ajax/api/cabinet/dirtags/(\d+)/$', 'dirtags.ajax.dirtags_handler'),
    url(r'^ajax/api/cabinet/dirtags/(\d+)/add-publication/(\d+:\d+)$', 'dirtags.ajax.dirtags_handler'),
)