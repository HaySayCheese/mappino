#coding=utf-8
from django.conf.urls import patterns, url

from apps.cabinet.api.publications.ajax import Publications, Publication
from apps.cabinet.api.publications.calendar_rent.ajax import CalendarControlView

urlpatterns = patterns('apps.cabinet.api',
    # list
	url(r'^ajax/api/cabinet/publications/$', Publications.as_view()),

	# single
	url(r'^ajax/api/cabinet/publications/(\d+):(\w+)/((permanent/)?)$', Publication.as_view()), # note: optional parameter "permanent"



    # url(r'^ajax/api/cabinet/publications/(\d+):(\w+)/publish/$', Publication.PublishUnpublish.as_view(), {"operation": 'publish'}),
    url(r'^ajax/api/cabinet/publications/(\d+):(\w+)/publish/$', Publication.Publish.as_view()),
    url(r'^ajax/api/cabinet/publications/(\d+):(\w+)/unpublish/$', Publication.Unpublish.as_view()),
    url(r'^ajax/api/cabinet/(\d+): (\w+)/calendar/$', CalendarControlView.as_view()),

        # photos
        url(r'^ajax/api/cabinet/publications/(\d+):(\w+)/photos/$', Publication.UploadPhoto.as_view()),
        url(r'^ajax/api/cabinet/publications/(\d+:\w+)/photos/(\w+)/$', Publication.Photos.as_view()),
        url(r'^ajax/api/cabinet/publications/(\d+:\w+)/photos/(\w+)/title/$', Publication.PhotoTitle.as_view()),


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