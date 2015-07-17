# coding=utf-8
from django.conf.urls import patterns, url, include


urlpatterns = patterns('apps.cabinet',
    # flatpages
    url(r'^cabinet/$', 'views.cabinet'),

    # templates
    url(r'', include('apps.cabinet.templates.urls')),

    # API
    url(r'', include('apps.cabinet.api.publications.urls')),
    url(r'', include('apps.cabinet.api.stats.urls')),
    url(r'', include('apps.cabinet.api.support.urls')),
    url(r'', include('apps.cabinet.api.settings.urls')),
)