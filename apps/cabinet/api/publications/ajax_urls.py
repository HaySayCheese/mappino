#coding=utf-8
from apps.cabinet.api.publications.ajax import Publications
from django.conf.urls import patterns, url


urlpatterns = patterns('apps.cabinet.api',
	url(r'^ajax/api/cabinet/publications/$', Publications.as_view()),
	url(r'^ajax/api/cabinet/publications/(\d+:\w+)/$', Publications.RUD.as_view()),
    url(r'^ajax/api/cabinet/publications/(\d+:\w+)/delete-permanent/$', Publications.PermanentDelete.as_view()),
    url(r'^ajax/api/cabinet/publications/(\d+:\w+)/publish/$', Publications.Publish.as_view()),
    url(r'^ajax/api/cabinet/publications/(\d+:\w+)/unpublish/$', Publications.Unpublish.as_view()),


	# photos
    url(r'^ajax/api/cabinet/publications/(\d+):(\w+)/photos/$', Publications.UploadPhoto.as_view()),
    url(r'^ajax/api/cabinet/publications/(\d+:\w+)/photos/(\w+)/$', Publications.Photos.as_view()),
    url(r'^ajax/api/cabinet/publications/(\d+:\w+)/photos/(\w+)/title/$', Publications.PhotoTitle.as_view()),


    url(r'^ajax/api/cabinet/publications/counters/$', 'publications.briefs.ajax.counters'),

    # briefs
    url(r'^ajax/api/cabinet/publications/briefs/all/$',
        'publications.briefs.ajax.get', {'section': 'all'}),
    url(r'^ajax/api/cabinet/publications/briefs/published/$',
        'publications.briefs.ajax.get', {'section': 'published'}),
    url(r'^ajax/api/cabinet/publications/briefs/unpublished/$',
        'publications.briefs.ajax.get', {'section': 'unpublished'}),
    url(r'^ajax/api/cabinet/publications/briefs/trash/$',
        'publications.briefs.ajax.get', {'section': 'trash'}),
    url(r'^ajax/api/cabinet/publications/briefs/(\d+)/$',
        'publications.briefs.ajax.get', {'section': 'tag'}),
)