# coding=utf-8
from django.conf.urls import patterns, url, include


urlpatterns = patterns('apps.cabinet',
    # flatpages
    url(r'^cabinet/$', 'views.cabinet'),
    url(r'^cabinet/login/$', 'views.login'),

    # templates
    url(r'', include('apps.cabinet.templates.urls')),

    # API
    url(r'', include('apps.cabinet.api.dirtags.ajax_urls')),
    url(r'', include('apps.cabinet.api.publications.ajax_urls')),
    url(r'', include('apps.cabinet.api.stats.ajax_urls')),
    url(r'', include('apps.cabinet.api.search.ajax_urls')),
    url(r'', include('apps.cabinet.api.support.ajax_urls')),
    url(r'', include('apps.cabinet.api.billing.ajax_urls')),
    url(r'', include('apps.cabinet.api.settings.ajax_urls')),
)