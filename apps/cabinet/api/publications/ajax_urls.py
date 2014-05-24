from django.conf.urls import patterns, url
from apps.cabinet.api.publications.ajax import UploadPhoto, Photos, PhotoTitle


urlpatterns = patterns('apps.cabinet.api',
    # CRUD
	url(r'^ajax/api/cabinet/publications/$', 'publications.ajax.create'),

	# unpublished
	url(r'^ajax/api/cabinet/publications/unpublished/(\d+:\d+)/$', 'publications.ajax.rud_switch'),
    url(r'^ajax/api/cabinet/publications/unpublished/(\d+:\d+)/publish/$', 'publications.ajax.publish'),

	# published
	url(r'^ajax/api/cabinet/publications/published/(\d+:\d+)/$', 'publications.ajax.rud_switch'), # todo: change me
    url(r'^ajax/api/cabinet/publications/unpublished/(\d+:\d+)/unpublish/$','publications.ajax.unpublish'),



    # briefs
    url(r'^ajax/api/cabinet/publications/counters/$', 'publications.briefs.ajax.counters'),
    url(r'^ajax/api/cabinet/publications/briefs/all/$',
        'publications.briefs.ajax.get', {'section': 'all'}),
    url(r'^ajax/api/cabinet/publications/briefs/published/$',
        'publications.briefs.ajax.get', {'section': 'published'}),
    url(r'^ajax/api/cabinet/publications/briefs/unpublished/$',
        'publications.briefs.ajax.get', {'section': 'unpublished'}),
    url(r'^ajax/api/cabinet/publications/briefs/deleted/$',
        'publications.briefs.ajax.get', {'section': 'deleted'}),
    url(r'^ajax/api/cabinet/publications/briefs/(\d+)/$',
        'publications.briefs.ajax.get', {'section': 'tag'}),

    # photos
    url(r'^ajax/api/cabinet/publications/(\d+:\d+)/photos/$', UploadPhoto.as_view()),
    url(r'^ajax/api/cabinet/publications/(\d+:\d+)/photos/(\d+)/$', Photos.as_view()),
    url(r'^ajax/api/cabinet/publications/(\d+:\d+)/photos/(\d+)/title/$', PhotoTitle.as_view()),
)