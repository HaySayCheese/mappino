# coding=utf-8
from django.conf.urls import patterns, url, include


urlpatterns = patterns('apps.main.views',
    # flatpages
    url(r'^$', 'homepage'),
    url(r'^map/$', 'map'),

    # templates
    url(r'', include('apps.main.templates.urls')),

    # API
    url(r'', include('apps.main.api.publications_and_markers.urls')),
    url(r'', include('apps.main.api.contacts.urls')),
    url(r'', include('apps.main.api.correspondence.urls')),
    url(r'', include('apps.main.api.favorites.urls')),
    url(r'', include('apps.main.api.claims.urls')),
)