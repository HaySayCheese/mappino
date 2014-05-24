from apps.cabinet.api.publications.ajax import Publications
from django.conf.urls import patterns, url


urlpatterns = patterns('apps.cabinet.api',
    # create
	url(r'^ajax/api/cabinet/publications/$', Publications.Create.as_view()),
	url(r'^ajax/api/cabinet/publications/(\d+:\d+)/$', Publications.RUD.as_view()),
    url(r'^ajax/api/cabinet/publications/(\d+:\d+)/publish/$', Publications.Publish.as_view()),
    url(r'^ajax/api/cabinet/publications/(\d+:\d+)/unpublish/$', Publications.Unpublish.as_view()),


	# photos
    url(r'^ajax/api/cabinet/publications/(\d+:\d+)/photos/$', Publications.UploadPhoto.as_view()),
    url(r'^ajax/api/cabinet/publications/(\d+:\d+)/photos/(\d+)/$', Publications.Photos.as_view()),
    url(r'^ajax/api/cabinet/publications/(\d+:\d+)/photos/(\d+)/title/$', Publications.PhotoTitle.as_view()),



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
)