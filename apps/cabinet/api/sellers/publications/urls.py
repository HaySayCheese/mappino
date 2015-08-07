#coding=utf-8
from django.conf.urls import patterns, url

from apps.cabinet.api.sellers.publications.ajax import Publications, Publication, Briefs


urlpatterns = patterns('',
    # list
    url(r'^ajax/api/cabinet/publications/$', Publications.as_view()),

    # single
    url(r'^ajax/api/cabinet/publications/(\d+):(\w+)/(permanent/)?$', Publication.as_view()), # note: optional parameter "permanent"
    url(r'^ajax/api/cabinet/publications/(\d+):(\w+)/publish/$', Publication.PublishUnpublish.as_view(), {'operation': 'publish'}),
    url(r'^ajax/api/cabinet/publications/(\d+):(\w+)/unpublish/$', Publication.PublishUnpublish.as_view(), {'operation': 'unpublish'}),

        # photos
        url(r'^ajax/api/cabinet/publications/(\d+):(\w+)/photos/$', Publication.UploadPhoto.as_view()),
        url(r'^ajax/api/cabinet/publications/(\d+:\w+)/photos/(\w+)/$', Publication.Photos.as_view()),
        url(r'^ajax/api/cabinet/publications/(\d+:\w+)/photos/(\w+)/title/$', Publication.TitlePhoto.as_view()),


    # briefs
    url(r'^ajax/api/cabinet/publications/briefs/all/$', Briefs.as_view(), {'section': 'all'}),
    url(r'^ajax/api/cabinet/publications/briefs/published/$', Briefs.as_view(), {'section': 'published'}),
    url(r'^ajax/api/cabinet/publications/briefs/unpublished/$', Briefs.as_view(), {'section': 'unpublished'}),
    url(r'^ajax/api/cabinet/publications/briefs/trash/$', Briefs.as_view(), {'section': 'trash'}),
)